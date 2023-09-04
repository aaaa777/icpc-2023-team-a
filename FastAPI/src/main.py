from fastapi import FastAPI
from .streetview.streetview import GoogleStreetView
from .vehicle_counting import VehicleCounting

app = FastAPI()
GSV = GoogleStreetView()
VC = VehicleCounting()

@app.get('/')
def read_root():
    return {"Hello": "World"}

@app.get('/api/measure_point')
async def get_streetview_image_path(lat: float, lon: float):
    
    stview_image_paths = GSV.get_split_image_paths(lat, lon)
    GSV.show_image(stview_image_paths)
    result = VC.count(stview_image_paths)
    
    # Calculation section Here

    return result
    
    # return {
    #     "CO2": 12345678,
    #     "unit": "ppm",
    # }