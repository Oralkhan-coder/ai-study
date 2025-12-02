from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.user import model, schemas, exceptions, utils


class UserService:
    def __init__(self, db: AsyncSession):
        self.db = db

    # CREATE
    async def create_user(self, data: schemas.UserCreate):
        existing = await self.db.scalar(
            select(model.User).where(model.User.email == data.email)
        )
        if existing:
            raise exceptions.UserAlreadyExists

        user = model.User(
            username=data.email,
            email=data.email,
            full_name=data.full_name,
            password=utils.hash_password(data.password),
            role="user"
        )
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    # READ
    async def get_user(self, user_id: int):
        user = await self.db.get(model.User, user_id)
        if not user:
            raise exceptions.UserNotFound
        return user

    async def get_user_by_email(self, email: str):
        return await self.db.scalar(
            select(model.User).where(model.User.email == email)
        )

    # UPDATE
    async def update_user(self, user_id: int, data: schemas.UserUpdate):
        user = await self.get_user(user_id)

        if data.email:
            user.email = data.email
        if data.password:
            user.hashed_password = utils.hash_password(data.password)
        if data.is_verified is not None:
            user.is_verified = data.is_verified

        await self.db.commit()
        await self.db.refresh(user)
        return user

    # DELETE
    async def delete_user(self, user_id: int):
        user = await self.get_user(user_id)
        await self.db.delete(user)
        await self.db.commit()
        return True
