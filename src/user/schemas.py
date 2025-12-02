from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    password: str
    email: str
    full_name: str

class UserUpdate(BaseModel):
    email: str | None = None
    password: str | None = None
    is_verified: bool | None = None

class UserOut(BaseModel):
    id: int
    is_verified: bool
    email: str
    full_name: str

    class Config:
        from_attributes = True
