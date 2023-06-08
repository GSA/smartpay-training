from datetime import datetime
from training.models import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey, func


class QuizCompletion(Base):
    __tablename__ = "quiz_completions"

    id: Mapped[int] = mapped_column(primary_key=True)
    quiz_id: Mapped[int] = mapped_column(ForeignKey("quizzes.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    passed: Mapped[bool] = mapped_column()
    submit_ts: Mapped[datetime] = mapped_column(server_default=func.now())
