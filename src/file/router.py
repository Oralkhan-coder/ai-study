from fastapi import APIRouter, UploadFile
from fastapi.params import Depends

from src.file.dependencies import get_file_service
from src.file.schemas import FileResponse
from src.file.service import FileService


router = APIRouter(
    prefix="/files",
    tags=["Files"]
)

@router.post("/upload", response_model=FileResponse)
async def upload_file(file: UploadFile, service: FileService = Depends(get_file_service)):
    return await service.store_file(file)