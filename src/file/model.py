from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, Enum
from src.core.model import BaseModel


class FileResource(BaseModel):
    __tablename__ = "files"

    file_name: Mapped[str] = mapped_column(String, nullable=False)
    file_size: Mapped[int] = mapped_column(Integer, nullable=False)
    file_extension: Mapped[str] = mapped_column(String(20), nullable=False)
    file_type: Mapped[str] = mapped_column(String(50), nullable=False)
    url: Mapped[str] = mapped_column(String(255), nullable=False)
