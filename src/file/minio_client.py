import os

from dotenv import load_dotenv
from minio import Minio

load_dotenv()

minio_client = Minio(
    endpoint=os.getenv("MINIO_URL"),
    access_key=os.getenv("MINIO_LOGIN"),
    secret_key=os.getenv("MINIO_PASSWORD"),
    secure=False
)