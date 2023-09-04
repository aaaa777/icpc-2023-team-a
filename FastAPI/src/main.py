from fastapi import FastAPI

from .vehicle_counting import VehicleCounting
from .streetview.streetview import GoogleStreetView

app = FastAPI()
GSV = GoogleStreetView()

@app.get('/')
def read_root():
    return {"Hello": "World"}

@app.get('/api/measure_point')
async def get_streetview_image_path(lat: float, lon: float):
    
    stview_image_paths = GSV.get_split_image_paths(lat, lon)
    GSV.show_image(stview_image_paths)
    
    images_path = get_images(lon, lat)
    VC = VehicleCounting(images_path)
    
    result = VC.Count()
    print(result)
    
    # Calculation section Here
    return {'d': stview_image_paths}
