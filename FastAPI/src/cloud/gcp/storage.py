import os
from fastapi.responses import JSONResponse, StreamingResponse
from google.cloud import storage
from dotenv import load_dotenv

class CloudStorageService:
    def __init__(self, bucket_name=None, path_prefix=None) -> None:
        self.bucket_name = bucket_name
        self.path_prefix = path_prefix
        # some authentication code here
        self.client = storage.Client()

    def add_prefix(self, filename: str, prefix: str=None) -> str:
        if(prefix is None and self.path_prefix is None):
            return filename
        return self.path_prefix + "/" + filename

    def upload_dir(self, directory: str) -> str:
        for filename in os.listdir(directory):
            filepath = os.path.join(directory, filename)
            self.upload_file(filepath)

    def upload_file(self, filepath: str) -> str:
        bucket_obj = self.client.get_bucket(self.bucket_name)
        bucket_obj.blob(self.add_prefix(filepath)).upload_from_filename(filepath)

    def download_file(self, filename: str) -> None:
        bucket_obj = self.client.get_bucket(self.bucket_name)
        bucket_obj.blob(self.add_prefix(filename)).download_to_filename(filename)

    def download_blob(self, filename: str):
        bucket_obj = self.client.get_bucket(self.bucket_name)
        blob = bucket_obj.blob(self.path_prefix + "/" + filename)
        with blob.open() as f:
            return StreamingResponse(
                f,
                media_type="image/jpeg",
            )