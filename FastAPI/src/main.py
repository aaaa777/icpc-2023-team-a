from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

from FastAPI.src.vehicle_counting import VehicalCounting
from .streetview.image_downloader import get_images
  
from .exception.streetview import StreetViewPointNotFound, StreetViewLatitudeOutOfRange, StreetViewLongitudeOutOfRange, StreetViewUnknownError, StreetViewZeroResults



app = FastAPI()


@app.get('/')
def read_root():
    return {"Hello": "World"}

@app.get('/api/measure_point')
async def download_image(lon: float, lat: float):
    
    # try to download image
    try:
        images_path = get_images(lon, lat)

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
        VC = VehicalCounting(images_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Unknown error: {}".format(e))
    
    result = VC.Count()
    print(result)
    
    # Calculation section Here
    
    
    return {
        "status": "OK",
        "CO2": 12345678,
        "unit": "ppm",
    }