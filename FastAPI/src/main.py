from os.path import join, basename, dirname
import os
from dotenv import load_dotenv

# fastapi
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse, StreamingResponse, FileResponse
from fastapi.staticfiles import StaticFiles

# exception
from .exception.streetview import \
    StreetViewPointNotFound, \
    StreetViewLatitudeOutOfRange, \
    StreetViewLongitudeOutOfRange, \
    StreetViewUnknownError, \
    StreetViewZeroResults

# co2 calculator
from .measuring.co2 import CO2Counter

# vehicle counter
from .vehicle_counting import VehicleCounting
from .streetview.streetview import GoogleStreetView

# cloud services
from .cloud.gcp.storage import CloudStorageService

from pydantic import BaseModel

if(os.path.exists('.env')):
    load_dotenv(verbose=True)
elif(os.path.exists('FastAPI/.env')):
    load_dotenv("FastAPI/.env", verbose=True)

# /api/measure_area
class area_req(BaseModel) :
    points : list

# initialize instances
app = FastAPI()
GSV = GoogleStreetView()
VC = VehicleCounting(None)
CC = CO2Counter()

CSS = CloudStorageService(bucket_name="icpc-a", path_prefix="temp")

# download images
if(os.environ.get("S3_PROVIDER") == "GCP"):

    print("GCP Object Storage Setting loaded")
    @app.get('/downloads/{directory}/{filename}')
    def download_file(directory: str, filename: str):
        print("request for downloads/{}/{}".format(directory, filename))
        file_path = "downloads/{}/{}".format(directory, filename)
        CSS.download_file(file_path)
        return FileResponse(
            file_path
        )
else:

    print("Local Object Storage Setting loaded")
    app.mount("/downloads", StaticFiles(directory="downloads"), name="static")


# html file
app.mount("/html", StaticFiles(directory="html", html=True), name="html")


@app.get('/')
def read_root():
    return {"Hello": "World"}

@app.get('/api/test')
def test():
    CSS.upload_file("downloads/2023-09-05.17-28-06-265417/boxed_image_0.jpg")

@app.get('/api/test2')
def test2():
    CSS.download_file("downloads/2023-09-05.17-28-06-265417/boxed_image_0.jpg")
    return FileResponse(
        "downloads/2023-09-05.17-28-06-265417/boxed_image_0.jpg"
    )

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
    
    json_boxed_images_paths = ["/" + join(dirname(image_path), "boxed_" + basename(image_path)) for image_path in images_paths]
    json_images_paths = ["/" + image_path for image_path in images_paths]

    CSS.upload_dir(images_dir)

    return {
        "status": "OK",
        "CO2": co2_amount,
        "unit": "ppm",
        "vehicle_count": result,
        "images_paths": {
            "original": json_images_paths,
            "boxed": json_boxed_images_paths,
        },
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


# serverless entry point
def get_app():
    return app