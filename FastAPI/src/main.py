from fastapi import FastAPI

from .vehicle_counting import VehicleCounting
from .streetview.image_downloader import get_images

app = FastAPI()

@app.get('/')
def read_root():
    return {"Hello": "World"}

@app.get('/api/measure_point')
async def download_image(lon: float, lat: float):
    
    images_path = get_images(lon, lat)
    VC = VehicleCounting(images_path)
    
    result = VC.Count()
    print(result)
    
    # Calculation section Here
    
    return {
        "CO2": 12345678,
        "unit": "ppm",
    }