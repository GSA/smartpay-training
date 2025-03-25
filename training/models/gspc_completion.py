from typing import Any
from datetime import date, datetime
import uuid
from training.models import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import UUID, ForeignKey, func


class GspcCompletion(Base):
    __tablename__ = "gspc_completions"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    passed: Mapped[bool] = mapped_column()
    certification_expiration_date: Mapped[date] = mapped_column(nullable=False)
    submit_ts: Mapped[datetime] = mapped_column(server_default=func.now())
    responses: Mapped[dict[str, Any]] = mapped_column()
    gspc_invite_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("gspc_invite.gspc_invite_id"),
        type_=UUID(as_uuid=True),
        unique=False,
        nullable=True)
