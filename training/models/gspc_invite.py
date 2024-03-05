from training.models import Base
from sqlalchemy import Column, DateTime, Date, func
from sqlalchemy.orm import Mapped, mapped_column


class GspcInvite(Base):
    __tablename__ = "gspc_invite"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=False)
    created_date = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    certification_expiration_date = Column(Date(), nullable=False)
