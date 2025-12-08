from sqlalchemy.ext.asyncio import AsyncSession

from src.file.service import FileService
from src.shared.gemini_service import generate_quiz_by_file


class QuizService:
    def __init__(self, db: AsyncSession, file_service: FileService):
        self.db = db
        self.file_service = file_service

    async def generate_quiz(self, file_id: int):
        file = await self.file_service.get_file(file_id)
        return await generate_quiz_by_file(file.file_name)
