from datetime import datetime
import os
import google_streetview.api

from os.path import join
from dotenv import load_dotenv

load_dotenv(verbose=True)

API_KEY = os.environ.get("API_KEY")
download_dir = 'downloads'


# download a image

def download_image(lon, lat, heading, save_dirname, save_filename):

    # decide filename
    file_dir = '{}/{}'.format(download_dir, save_dirname)

    # Define parameters for street view api
    params = [{
        'size': '640x640', # max 640x640 pixels
        # 'location': "46.414382,10.013988",
        'location': "{},{}".format(lon, lat),
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
    image_pathes = []
    for i, heading in enumerate([0, 120, 240]):
        image_path = "{}_{}.jpg".format(filename_prefix, i)
        image_pathes.append(image_path)
        download_image(lon, lat, heading, save_dirname, image_path)

    return image_pathes

if(__name__ == "__main__"):
    # location = '46.414382,10.013988'
    # location = '36.32252348212603,139.0112780592011' # jp
    # location = '13.7037585,100.4664948' # thai
    location = '43.079734,141.525624'
    lon, lat = location.split(',')

    # create dir named datetime.now()
    requested_at = datetime.now().strftime('%Y-%m-%d.%H-%M-%S-%f')

    # create 
    download_image_120x3(lon, lat, requested_at, "image")