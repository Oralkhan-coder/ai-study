from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import get_db
from src.file.service import FileService
from src.file.dependencies import get_file_service
from src.quiz.service import QuizService


async def get_quiz_service(db:AsyncSession = Depends(get_db),
                           file_service: FileService = Depends(get_file_service)):
    return QuizService(db, file_service)