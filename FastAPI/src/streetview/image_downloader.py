from datetime import datetime
import os
import google_streetview.api
import cv2
import numpy as np

from os.path import join
from dotenv import load_dotenv

load_dotenv(verbose=True)

API_KEY = os.environ.get("API_KEY")
download_dir = 'downloads'
print(API_KEY)

# download a image

def download_image(lon, lat, heading, save_dirname, save_filename):

    # decide filename
    file_dir = '{}/{}'.format(download_dir, save_dirname)

    # Define parameters for street view api
    params = [{
        'size': '640x640', # max 640x640 pixels
        # 'location': "46.414382,10.013988",
        'location': "{},{}".format(lat, lon),
        'heading': heading,
        # 'pitch': '-0.76',
        'radius': '10000',
        'fov': '120',
        'key': API_KEY
    }]

    # Create a results object
    results = google_streetview.api.results(params)


    # Download images to directory 'downloads'
    print('downloading image into `{}`'.format(join(file_dir, save_filename)))
    results.download_links(file_dir)

    # rename filename
    os.rename(join(file_dir, 'gsv_0.jpg'), join(file_dir, save_filename))

    return join(file_dir, save_filename)

def download_image_120x3(lon, lat, save_dirname, filename_prefix="gsv"):
    image_paths = []
    for i, heading in enumerate([0, 120, 240]):
        image_path = "{}_{}.jpg".format(filename_prefix, i)
        image_paths.append(download_image(lon, lat, heading, save_dirname, image_path))

    return image_paths

# concat images
def concat_images(image_pathes):
    images = [cv2.imread(path) for path in image_paths]
    output_image = np.concatenate(images, axis=1)
    return output_image

def get_images(lon: float, lat: float):
    # ?lat=36.32252348212603&lon=139.0112780592011 # jp
    # ?lat=13.7037585&lon=100.4664948 # thai

    # create dir named datetime.now()
    requested_at = datetime.now().strftime('%Y-%m-%d.%H-%M-%S-%f')

    # download images
    splitted_images = [cv2.imread(path) for path in download_image_120x3(lon, lat, requested_at, "image")]

    # concat images
    output_image = concat_images(splitted_images)

    # check output image
    # cv2.imshow('Merged Image', output_image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    # return result
    return output_image