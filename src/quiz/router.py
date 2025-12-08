from fastapi import APIRouter
from fastapi.params import Depends

from src.quiz.dependencies import get_quiz_service
from src.quiz.service import QuizService

router = APIRouter(prefix="/quiz", tags=["Quizzes"])

@router.post("/generate")
async def generate_quiz(file_id: int, service: QuizService = Depends(get_quiz_service)):
    return await service.generate_quiz(file_id)