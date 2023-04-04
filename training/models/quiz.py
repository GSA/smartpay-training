from training.models import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship, Relationship


class Quiz(Base):
    __tablename__ = "quizzes"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    name: Mapped[str] = mapped_column()
    topic: Mapped[str] = mapped_column()
    audience: Mapped[str] = mapped_column()
    active: Mapped[bool] = mapped_column()
    questions: Relationship = relationship("QuizQuestion")
