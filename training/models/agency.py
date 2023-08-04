from training.models import Base
from sqlalchemy.orm import Mapped, mapped_column


class Agency(Base):
    __tablename__ = "agencies"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    bureau: Mapped[str] = mapped_column(nullable=True)
