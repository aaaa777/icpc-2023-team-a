from fastapi import FastAPI
from .streetview.image_downloader import get_images

app = FastAPI()

@app.get('/')
def read_root():
    return {"Hello": "World"}

@app.get('/api/measure_point')
async def download_image(lon: float, lat: float):

    # get opencv 360 image
    images = get_images(lon, lat)
    
    # processing image
    """some program/function to process image"""
    
    # result
    # return {'images': images}
    return {
        "CO2": 12345678,
        "unit": "ppm",
    }