from training.models import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Agency(Base):
    __tablename__ = "agencies"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    name: Mapped[str] = mapped_column(unique=True, index=True)
    users = relationship("User", back_populates="agency")