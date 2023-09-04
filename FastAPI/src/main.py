from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

from .exception.streetview import StreetViewPointNotFound, StreetViewLatitudeOutOfRange, StreetViewLongitudeOutOfRange, StreetViewUnknownError, StreetViewZeroResults


from .vehicle_counting import VehicleCounting
from .streetview.streetview import GoogleStreetView

app = FastAPI()
GSV = GoogleStreetView()

@app.get('/')
def read_root():
    return {"Hello": "World"}

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
        VC = VehicleCounting(images_dir)
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