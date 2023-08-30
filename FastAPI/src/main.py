# from typing import Union
from fastapi import FastAPI
# from pydantic import BaseModel
from .streetview.image_downloader import get_images

# class Image(BaseModel):
#     name: str
#     description: Union[str, None] = None
#     location: str

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/image/download")
def download_image():
    images = get_images('43.079734,141.525624')
    return {"images": images}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}