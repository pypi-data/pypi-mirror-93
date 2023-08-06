import os
from io import BytesIO
import requests
import urllib.request
import json
from tqdm import tqdm

from PIL import Image, ExifTags

import numpy as np


def bitmap2file(bitmap, is_segmentation_bitmap=True):
    """Convert a label bitmap to a file with the proper format.

    Args:
        bitmap (np.uint32): A numpy array where each unique value represents an instance id.

    Returns:
        object: a file object.
    """

    # TODO: convert bitmap to np.uint32, if it is not already
    if is_segmentation_bitmap:
        bitmap2 = np.copy(bitmap)
        bitmap2 = bitmap2[:, :, None].view(np.uint8)
        bitmap2[:, :, 3] = 255
    else:
        assert False
        
    f = BytesIO()
    Image.fromarray(bitmap2).save(f, 'PNG')
    f.seek(0)
    return f

def get_semantic_bitmap(instance_bitmap, annotations, first_category_id=1):
    """Convert an instance bitmap and annotations dict into a segmentation bitmap.

    Args:
        instance_bitmap (np.uint32): A numpy array where each unique value represents an instance id.
        annotations (dict): An annotations dictionary.
        first_category_id (int, optional): First category id. Defaults to 1.

    Returns:
        np.uint32: a numpy array where each unique value represents a category id.
    """

    instance2semantic = [0] * (max([a['id'] for a in annotations])+1)
    for annotation in annotations:
        instance2semantic[annotation['id']] = annotation['category_id'] + first_category_id
    instance2semantic = np.array(instance2semantic)
        
    semantic_label = instance2semantic[np.array(instance_bitmap, np.uint32)]
    return semantic_label

def export_dataset(dataset, export_format='coco'):
    """Export a dataset to a different format.

    Args:
        dataset (dict): A dataset object, resulting from client.get_dataset().
        export_format (str, optional): The destination format. Defaults to 'coco'.
    """

    from pycocotools import mask
    from skimage.measure import regionprops

    def get_bbox(binary_mask):
        regions = regionprops(np.uint8(binary_mask))
        if len(regions) == 1:
            bbox = regions[0].bbox
            return bbox
        else:
    #         assert False
            return False

    # https://www.immersivelimit.com/tutorials/create-coco-annotations-from-scratch/#coco-dataset-format

    if export_format != 'coco':
        print('Supported export formats: coco')
        return

    info = {
        'description': dataset.release['dataset']['name'],
        # 'url': 'https://segments.ai/test/test',
        'version':  dataset.release['name'],
        # 'year': 2020,
        # 'contributor': 'Segments.ai',
        # 'date_created': '2020/09/01'
    }

    # licenses = [{
    #     'url': 'http://creativecommons.org/licenses/by-nc-sa/2.0/',
    #     'id': 1,
    #     'name': 'Attribution-NonCommercial-ShareAlike License'
    # }]

    categories = dataset.categories
    task_type = dataset.task_type
    # for i, category in enumerate(dataset.project_info['label_taxonomy']):
    #     categories.append({
    #         'id': i+1,
    #         'supercategory': 'object',
    #         'name': category
    #     })

    images = []
    annotations = []

    annotation_id = 1
    for i in tqdm(range(len(dataset))):        
        sample = dataset[i]
    #     print(sample)
        
        image_id = i+1
        images.append({        
            'id': image_id,
            # 'license': 1,
            'file_name': sample['file_name'],
            'height': sample['image'].size[1],
            'width': sample['image'].size[0],
    #         'date_captured': "2013-11-14 17:02:52",
    #         'coco_url': "http://images.cocodataset.org/val2017/000000397133.jpg",
    #         'flickr_url': "http://farm7.staticflickr.com/6116/6255196340_da26cf2c9e_z.jpg",        
        })
        
        for instance in sample['annotations']:
            category_id = instance['category_id']

            annotation = {
                'id': annotation_id,
                'image_id': image_id,
                'category_id': category_id,
            }

            # Segmentation bitmap
            if task_type == 'segmentation-bitmap':                
                instance_mask = np.array(sample['segmentation_bitmap'], np.uint32) == instance['id']
                bbox = get_bbox(instance_mask)
                if not bbox:
                    continue
                    
                y0, x0, y1, x1 = bbox
                # rle = mask.encode(np.asfortranarray(instance_mask))
                rle = mask.encode(np.array(instance_mask[:,:,None], dtype=np.uint8, order='F'))[0] # https://github.com/matterport/Mask_RCNN/issues/387#issuecomment-522671380
        #         instance_mask_crop = instance_mask[y0:y1, x0:x1]
        #         rle = mask.encode(np.asfortranarray(instance_mask_crop))
        #         plt.imshow(instance_mask_crop)
        #         plt.show()
                
                area = int(mask.area(rle))
                rle['counts'] = rle['counts'].decode('ascii')

                annotation.update({
                    'bbox': [x0, y0, x1-x0, y1-y0],
        #             'bbox_mode': BoxMode.XYWH_ABS,
                    'segmentation': rle,
                    'area': area,
                    'iscrowd': 0,
                })

            # Bounding boxes
            elif task_type == 'bboxes':
                points = instance['points']
                x0 = points[0][0]
                y0 = points[0][1]
                x1 = points[1][0]
                y1 = points[1][1]

                annotation.update({
                    'bbox': [x0, y0, x1-x0, y1-y0],
                })

            else:
                assert False

            annotations.append(annotation)
            annotation_id += 1
            
    json_data = {
        'info': info,
        # 'licenses': licenses,
        'categories': categories,
        'images': images,
        'annotations': annotations    
    #     'segment_info': [] # Only in Panoptic annotations
    }

    file_name = '{}_coco.json'.format(os.path.splitext(os.path.basename(dataset.release_file))[0])
    with open(file_name, 'w') as f:
        json.dump(json_data, f)

    print('Exported to {}.'.format(file_name))
    return file_name, dataset.image_dir

def download_and_save_image(url, filename):
    urllib.request.urlretrieve(url, filename)
    return

def download_and_save_segmentation_bitmap(url, filename):
    def extract_segmentation_bitmap(segmentation_bitmap):
        segmentation_bitmap = np.array(segmentation_bitmap)
        segmentation_bitmap[:,:,3] = 0
        segmentation_bitmap = segmentation_bitmap.view(np.uint32).squeeze(2)
        segmentation_bitmap = Image.fromarray(segmentation_bitmap)
        return segmentation_bitmap

    segmentation_bitmap = Image.open(BytesIO(requests.get(url).content))
    segmentation_bitmap = extract_segmentation_bitmap(segmentation_bitmap)
    segmentation_bitmap.save(filename)
    return

def handle_exif_rotation(image):
    try:
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation]=='Orientation':
                break
        exif=dict(image._getexif().items())
        if exif[orientation] == 3:
            image=image.transpose(Image.ROTATE_180)
        elif exif[orientation] == 6:
            image=image.transpose(Image.ROTATE_270)
        elif exif[orientation] == 8:
            image=image.transpose(Image.ROTATE_90)
        return image
    except (AttributeError, KeyError, IndexError):
        return image