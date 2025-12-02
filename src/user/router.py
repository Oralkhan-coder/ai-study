from fastapi import APIRouter, Depends
from src.user import schemas
from src.user.service import UserService
from src.user.dependencies import get_user_service

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=schemas.UserOut)
async def create_user(data: schemas.UserCreate, svc: UserService = Depends(get_user_service)):
    return await svc.create_user(data)


@router.get("/{user_id}", response_model=schemas.UserOut)
async def get_user(user_id: int, svc: UserService = Depends(get_user_service)):
    return await svc.get_user(user_id)


@router.put("/{user_id}", response_model=schemas.UserOut)
async def update_user(user_id: int, data: schemas.UserUpdate, svc: UserService = Depends(get_user_service)):
    return await svc.update_user(user_id, data)


@router.delete("/{user_id}")
async def delete_user(user_id: int, svc: UserService = Depends(get_user_service)):
    await svc.delete_user(user_id)
    return {"message": "User deleted"}
