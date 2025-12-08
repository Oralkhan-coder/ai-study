from typing import List

from sqlalchemy import ForeignKey, String, Text, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.model import BaseModel
from src.user.model import User


class Quiz(BaseModel):
    __tablename__ = "quizzes"

    material_id: Mapped[str] = mapped_column(ForeignKey("materials.id"))
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"))

    title: Mapped[str] = mapped_column(String(255))

    material: Mapped["Material"] = relationship(back_populates="quizzes")
    user: Mapped["User"] = relationship(back_populates="quizzes")
    questions: Mapped[List["QuizQuestion"]] = relationship(
        back_populates="quiz", cascade="all, delete-orphan"
    )
    results: Mapped[List["QuizResult"]] = relationship(
        back_populates="quiz", cascade="all, delete-orphan"
    )


class QuizQuestion(BaseModel):
    __tablename__ = "quiz_questions"


    quiz_id: Mapped[str] = mapped_column(ForeignKey("quizzes.id"))
    question: Mapped[str] = mapped_column(Text)

    quiz: Mapped["Quiz"] = relationship(back_populates="questions")
    answers: Mapped[List["QuizAnswer"]] = relationship(
        back_populates="question", cascade="all, delete-orphan"
    )


class QuizAnswer(BaseModel):
    __tablename__ = "quiz_answers"

    question_id: Mapped[str] = mapped_column(ForeignKey("quiz_questions.id"))
    answer_text: Mapped[str] = mapped_column(Text)
    is_correct: Mapped[bool] = mapped_column(Boolean)

    question: Mapped["QuizQuestion"] = relationship(back_populates="answers")


class QuizResult(BaseModel):
    __tablename__ = "quiz_results"

    quiz_id: Mapped[str] = mapped_column(ForeignKey("quizzes.id"))
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"))

    score: Mapped[float] = mapped_column()

    quiz: Mapped["Quiz"] = relationship(back_populates="results")
