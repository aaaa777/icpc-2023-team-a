from fastapi import FastAPI

from FastAPI.src.vehicle_counting import VehicalCounting
from .streetview.image_downloader import get_images

from pydantic import BaseModel


class area_req(BaseModel) :
    points : list


VC = VehicalCounting("downloads")



app = FastAPI()


@app.get('/')
def read_root():
    return {"Hello": "World"}

@app.get('/api/measure_point')
async def download_image(lon: float, lat: float):
    
    images_path = get_images(lon, lat)
    
    if images_path == None :
        return {"status" : "NOT_FOUND"}
    
    VC.set_folder_path(images_path)
    
    result = VC.Count()
    print(result)
    
    # Calculation section Here
    
    return {
        "status":"OK",
        "CO2": 12345678,
        "unit": "ppm",
    }
    
@app.post('/api/measure_area')
async def handler_multiple_point(area : area_req):
    
    if(area == None):
        return {"status" : "No Parameter",
                "detail" : "No Parameter"}
        
    points = area.points
    
    if points == None:
        return {"status" : "No data",
                "detail" : "No points was sent!!!"}


    image_dirs =  []
    
    for point in points :
        print(point)
        lat = point["lat"]
        lng = point["lng"]
        path = get_images(lng,lat)
        
        if path != None :
            image_dirs.append(path)
        
        
    print(image_dirs)
    
    point_res = []
    
    for dir in image_dirs :
        VC.set_folder_path(dir)
        result = VC.Count()
         
        print(result)
        point_res.append(result)
    
    return {"status":"OK" ,"point_res" : point_res }
