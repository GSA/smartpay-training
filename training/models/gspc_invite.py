from datetime import datetime, date
import uuid
from training.models import Base
from sqlalchemy import UUID, DateTime, Date, func
from sqlalchemy.orm import Mapped, mapped_column


class GspcInvite(Base):
    __tablename__ = "gspc_invite"

    id: Mapped[int] = mapped_column(primary_key=True)
    gspc_invite_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), unique=True, nullable=True)
    email: Mapped[str] = mapped_column(unique=False)
    created_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now(), nullable=False)
    certification_expiration_date: Mapped[date] = mapped_column(Date(), nullable=False)
    second_invite_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    final_invite_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    completed_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
