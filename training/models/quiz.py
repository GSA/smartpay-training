from typing import Any
from training.models import Base
from sqlalchemy.orm import Mapped, mapped_column


class Quiz(Base):
    __tablename__ = "quizzes"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    topic: Mapped[str] = mapped_column()
    audience: Mapped[str] = mapped_column()
    active: Mapped[bool] = mapped_column()
    content: Mapped[dict[str, Any]] = mapped_column()
