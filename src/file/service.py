import io
import os
import uuid

from dotenv import load_dotenv
from minio import Minio, S3Error
from src.file.model import FileResource
from sqlalchemy.ext.asyncio import AsyncSession

load_dotenv()
BUCKET_NAME = os.getenv("MINIO_BUCKET")
PUBLIC_URL = os.getenv("MINIO_PUBLIC_URL")

class FileService:
    def __init__(self, db: AsyncSession, minio_client: Minio):
        self.db = db
        self.minio_client = minio_client

    async def store_file(self, file):
        try:
            file_name = f"{uuid.uuid4()}_{file.filename}"
            file_bytes = await file.read()
            self.minio_client.put_object(
                bucket_name=BUCKET_NAME,
                object_name=file_name,
                data=io.BytesIO(file_bytes),
                length=len(file_bytes),
                content_type=file.content_type
            )

            _, ext = os.path.splitext(file.filename)
            file_extension = ext.lstrip(".").lower()

            file = FileResource(
                file_name=file_name,
                file_size=len(file_bytes),
                file_extension=file_extension,
                file_type=file.content_type,
                url=f"{PUBLIC_URL}/{file_name}"
            )
            self.db.add(file)
            await self.db.commit()
            await self.db.refresh(file)
            return file
        except S3Error as e:
            raise e

