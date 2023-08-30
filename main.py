from datetime import datetime
import os
import google_streetview.api

API_KEY = ''
download_dir = 'downloads'

def download_image(lon, lat, heading, save_filename='gsv_0.jpg'):
    # create dir named datetime.now()
    requested_at = datetime.now().strftime('%Y-%m-%d.%H-%M-%S-%f')

    # decide filename
    file_dir = '{}/{}'.format(download_dir, requested_at)

    # Define parameters for street view api
    params = [{
        'size': '640x640', # max 640x640 pixels
        # 'location': "46.414382,10.013988",
        'location': "{},{}".format(lon, lat),
        'heading': heading,
        'pitch': '-0.76',
        'fov': '120',
        'key': API_KEY
    }]

    # Create a results object
    results = google_streetview.api.results(params)


    # Download images to directory 'downloads'
    print('downloading image into `{}`'.format(file_dir))
    results.download_links(file_dir)

    return "{}/{}".format(file_dir, 'gsv_0.jpg')

if(__name__ == "__main__"):
    # location = '46.414382,10.013988'
    # location = '36.32252348212603,139.0112780592011' # jp
    location = '13.7037585,100.4664948' # thai
#     location = '46.414382,135.013988'
    lon, lat = location.split(',')
    [download_image(lon, lat, heading) for heading in [0, 120, 240]]