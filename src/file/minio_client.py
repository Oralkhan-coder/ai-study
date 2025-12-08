import os
import io

from dotenv import load_dotenv
from minio import Minio

load_dotenv()

BUCKET_NAME = os.getenv("MINIO_BUCKET")

minio_client = Minio(
    endpoint=os.getenv("MINIO_URL"),
    access_key=os.getenv("MINIO_LOGIN"),
    secret_key=os.getenv("MINIO_PASSWORD"),
    secure=False
)

def download_file_from_minio(object_name: str):
    response = minio_client.get_object(BUCKET_NAME, object_name)
    data = response.read()
    response.close()
    return data

def upload_file_to_minio(object_name: str, data: bytes, content_type: str = "application/octet-stream"):
    minio_client.put_object(
        bucket_name=BUCKET_NAME,
        object_name=object_name,
        data=io.BytesIO(data),
        length=len(data),
        content_type=content_type
    )