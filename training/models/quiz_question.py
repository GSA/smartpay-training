from training.models import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship, Relationship
from sqlalchemy import ForeignKey


class QuizQuestion(Base):
    __tablename__ = "quiz_questions"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    text: Mapped[str] = mapped_column()
    type: Mapped[str] = mapped_column()
    quiz_id: Mapped[int] = mapped_column(ForeignKey("quizzes.id"))
    choices: Relationship = relationship("QuizChoice")
