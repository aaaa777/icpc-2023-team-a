from fastapi import FastAPI
from .streetview.image_downloader import get_images

app = FastAPI()


@app.get('/')
def read_root():
    return {"Hello": "World"}

@app.get('/api/measure_point')
async def download_image(lon: float, lat: float):
    images = get_images(lon, lat)
    return {'images': images}