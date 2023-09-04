from utils import parentpath
import sys
sys.path.append(parentpath(__file__, 1))
print(parentpath(__file__, 1))

import cv2
import os
from FastAPI.src.streetview.image_downloader import download_image_120x3, concat_images

test_locations = [
    # (lat, lon, alt, name)
    (43.0848006, 141.3491377, 33, 'hokkaido-univ-north-east'),
    (43.081061, 141.333665, 93, 'hokkaido-univ-center'),
    (35.688416, 139.978322, 25, 'funabashi-1'),
    (35.694999, 139.982742, 26, 'funabashi-2'),
    (34.946945, 135.703707, 63, 'mukaihi'),
]

for location in test_locations:
    print(location)
    image_paths = download_image_120x3(location[1], location[0], location[3])
    output_image = concat_images(image_paths)

    # save image
    # 結合した画像は,image_pathsの親ディレクトリに保存する
    download_dir = image_paths[0].split('/')[:-1]
    download_dir = '/'.join(download_dir)
    cv2.imwrite(os.path.join(download_dir, '{}.jpg'.format(location[3])), output_image)
    
    