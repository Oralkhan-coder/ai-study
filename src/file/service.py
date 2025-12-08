import io
import os
import uuid
import src.file.minio_client as minio
import src.file.exceptions as exceptions

from dotenv import load_dotenv
from minio import S3Error
from src.file.model import FileResource
from sqlalchemy.ext.asyncio import AsyncSession

load_dotenv()
PUBLIC_URL = os.getenv("MINIO_PUBLIC_URL")

class FileService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def store_file(self, file):
        try:
            file_name = f"{uuid.uuid4()}_{file.filename}"
            file_bytes = await file.read()
            minio.upload_file_to_minio(file_name,file_bytes,
                                       file.content_type)

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

    async def get_file(self, file_id: int):
        file = await self.db.get(FileResource, file_id)
        if not file:
            raise exceptions.FileNotFoundError
        return file