from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String

from src.model import BaseModel


class User(BaseModel):
    __tablename__ = 'users'

    full_name: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    role: Mapped[str] = mapped_column(String)
    username: Mapped[str] = mapped_column(String, unique=True)
    password: Mapped[str] = mapped_column(String)
    is_verified: Mapped[bool] = mapped_column(default=False)
