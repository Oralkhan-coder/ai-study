from pydantic import BaseModel


class FileResponse(BaseModel):
    file_name: str
    file_extension: str
    file_type: str
    file_size: int
    url: str