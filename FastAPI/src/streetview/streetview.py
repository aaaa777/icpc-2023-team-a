from datetime import datetime
import os
import google_streetview.api
import cv2
import numpy as np

from ..exception.streetview import \
    StreetViewPointNotFound, \
    StreetViewLatitudeOutOfRange, \
    StreetViewLongitudeOutOfRange, \
    StreetViewUnknownError, \
    StreetViewZeroResults

from os.path import join
from dotenv import load_dotenv

if(os.path.exists('.env')):
    load_dotenv(verbose=True)
    API_KEY = os.environ.get("API_KEY")
elif(os.path.exists('FastAPI/.env')):
    load_dotenv("FastAPI/.env", verbose=True)
    API_KEY = os.environ.get("API_KEY")
else:
    API_KEY = ""

IMAGE_DOWNLOAD_DIR = 'downloads'

class GoogleStreetView:
    
    def __init__(self):
        self.key = API_KEY
        self.download_dir = IMAGE_DOWNLOAD_DIR

    # download split images from Google StreetView.
    def download_image(self, lat: float, lon: float, heading: str, save_dirname: str, save_filename : str) -> str:

        if(lat < -90 or lat > 90):
            raise StreetViewLatitudeOutOfRange(lat=lat)
    
        if(lon < -180 or lon > 180):
            raise StreetViewLongitudeOutOfRange(lon=lon)

        # decide filename
        file_dir = '{}/{}'.format(self.download_dir, save_dirname)

        # Define parameters for street view api
        params = [{
            'size': '640x640', # max 640x640 pixels
            # 'location': "46.414382,10.013988",
            'location': "{},{}".format(lat, lon),
            'heading': heading,
            # 'pitch': '-0.76',
            'radius': '10',
            'fov': '120',
            'key': self.key
        }]

        # Create a results object
        results = google_streetview.api.results(params)

        # Get image status
        img_status = results.metadata[0]["status"]
        print("Image Status : " + img_status)

        # Download images to directory 'downloads'
        print('downloading image into `{}`'.format(join(file_dir, save_filename)))
        results.download_links(file_dir)

        # check metadata.json
        #print(results.metadata[0]['status'])
        
        # error handling
        if(results.metadata[0]['status'] == 'ZERO_RESULTS'):
            raise StreetViewZeroResults()
        
        if(results.metadata[0]['status'] == 'NOT_FOUND'):
            raise StreetViewPointNotFound()

        if(results.metadata[0]['status'] != 'OK'):
            raise StreetViewUnknownError(status=results.metadata[0]['status'], error_message=results.metadata[0]['error_message'])

        # rename filename
        os.rename(join(file_dir, 'gsv_0.jpg'), join(file_dir, save_filename))

        return join(file_dir, save_filename)
    
    # do not set filename_prefix 'gsv'
    def get_split_image_paths(self, lat: float, lon: float, filename_prefix: str="image") -> list[str]:
        image_paths = []
        requested_at = datetime.now().strftime('%Y-%m-%d.%H-%M-%S-%f')
        for i, heading in enumerate([0, 120, 240]):
            image_path = "{}_{}.jpg".format(filename_prefix, i)
            image_paths.append(self.download_image(lat, lon, heading, requested_at, image_path))

        return image_paths
    
    def get_image_dir(self, images_paths) -> str:
        return os.path.dirname(images_paths[0])

    # show image
    def show_image(self, image_paths: list[str]):
        images = [cv2.imread(path) for path in image_paths]
        cv2.imshow('', np.concatenate(images, axis=1))
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    # concat images
    def concat_and_save_images(image_paths):
        images = [cv2.imread(path) for path in image_paths]
        output_image = np.concatenate(images, axis=1)
        # save image
        cv2.imwrite(os.path.join(os.path.dirname(image_paths[0]), 'output.jpg'), output_image)

    # concat images
    def concat_images(image_paths):
        images = [cv2.imread(path) for path in image_paths]
        output_image = np.concatenate(images, axis=1)
        return output_image
