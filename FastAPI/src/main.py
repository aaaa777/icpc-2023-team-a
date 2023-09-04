from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from .exception.streetview import \
    StreetViewPointNotFound, \
    StreetViewLatitudeOutOfRange, \
    StreetViewLongitudeOutOfRange, \
    StreetViewUnknownError, \
    StreetViewZeroResults

from .measuring.co2 import CO2Counter

from .vehicle_counting import VehicleCounting
from .streetview.streetview import GoogleStreetView

from pydantic import BaseModel

# /api/measure_area
class area_req(BaseModel) :
    points : list


app = FastAPI()
GSV = GoogleStreetView()
VC = VehicleCounting(None)
CC = CO2Counter()

# download images
app.mount("/downloads", StaticFiles(directory="downloads"), name="static")

# html file
app.mount("/html", StaticFiles(directory="html", html=True), name="html")


@app.get('/')
def read_root():
    return {"Hello": "World"}


# single point
@app.get('/api/measure_point')
async def get_streetview_image_path(lat: float, lon: float):
    
    # try to download image
    try:
        images_paths = GSV.get_split_image_paths(lat, lon)
        images_dir = GSV.get_image_dir(images_paths=images_paths)
        print(images_dir)
        #GSV.show_image(stview_image_paths)
        # images_path = get_images(lon, lat)

    # error handling
    except StreetViewPointNotFound as e:
        raise HTTPException(status_code=404, detail="StreetViewPoint not found")
    
    except StreetViewLatitudeOutOfRange as e:
        raise HTTPException(status_code=400, detail="StreetViewLatitude out of range: {}".format(e.lat))
    
    except StreetViewLongitudeOutOfRange as e:
        raise HTTPException(status_code=400, detail="StreetViewLongitude out of range: {}".format(e.lon))
    
    except StreetViewUnknownError as e:
        raise HTTPException(status_code=500, detail="StreetViewUnknownError: [{status}] {error_message}".format(status=e.status, error_message=e.error_message))
    
    except StreetViewZeroResults as e:
        raise HTTPException(status_code=500, detail="StreetViewZeroResults")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail="Unknown error: {}".format(e))

    # Calculation section Here
    try:
        VC.set_folder_path(images_dir)
        result = VC.Count()
    
    except Exception as e:
        raise HTTPException(status_code=500, detail="Unknown error: {}".format(e))

    print(result)
    
    # Calculation section Here
    try:
        co2_amount = CC.caluculate(result)

    except Exception as e:
        raise HTTPException(status_code=500, detail="Unknown error: {}".format(e))

    return {
        "status": "OK",
        "CO2": co2_amount,
        "unit": "ppm",
        "vehicle_count": result,
        "image_path": ["/" + image_path for image_path in images_paths],
    }


# multiple point
@app.post('/api/measure_area')
async def handler_multiple_point(area : area_req):
    
    if(area == None):
        return {
            "status" : "No Parameter",
            "detail" : "No Parameter"
        }
        
    points = area.points
    
    if points == None:
        return {
            "status" : "No data",
            "detail" : "No points was sent!!!"
        }


    image_dirs =  []
    
    for point in points :
        print(point)
        lat = point["lat"]
        lng = point["lng"]
        path = GSV.get_split_image_paths(lng, lat)
        
        if path != None :
            image_dirs.append(path)
        
        
    print(image_dirs)
    
    point_res = []
    
    for dir in image_dirs :
        VC.set_folder_path(dir)
        result = VC.Count()
         
        print(result)
        point_res.append(result)
    
    return {
        "status":"OK",
        "point_res": point_res
    }
