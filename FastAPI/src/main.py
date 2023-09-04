from fastapi import FastAPI

from FastAPI.src.vehicle_counting import VehicalCounting
from .streetview.image_downloader import get_images
  




app = FastAPI()


@app.get('/')
def read_root():
    return {"Hello": "World"}

@app.get('/api/measure_point')
async def download_image(lon: float, lat: float):
    
    images_path = get_images(lon, lat)
    VC = VehicalCounting(images_path)
    
    result = VC.Count()
    print(result)
    
    # Calculation section Here
    
    return {'images': images_path}