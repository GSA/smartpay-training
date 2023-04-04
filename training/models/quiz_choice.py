from training.models import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey


class QuizChoice(Base):
    __tablename__ = "quiz_choices"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    text: Mapped[str] = mapped_column()
    correct: Mapped[bool] = mapped_column()
    question_id: Mapped[int] = mapped_column(ForeignKey("quiz_questions.id"))
