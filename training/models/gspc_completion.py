from datetime import datetime
from training.models import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Column, Date, ForeignKey, func


class GspcCompletion(Base):
    __tablename__ = "gspc_completions"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    passed: Mapped[bool] = mapped_column()
    certification_expiration_date = Column(Date(), nullable=False)
    submit_ts: Mapped[datetime] = mapped_column(server_default=func.now())
    responses: Mapped[str] = mapped_column()
