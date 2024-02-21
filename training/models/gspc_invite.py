from training.models import Base
from sqlalchemy.orm import Mapped, DateTime,  mapped_column
from sqlalchemy.sql import func
from datetime  import datetime


class GspcInvite(Base):
    __tablename__ = "gspc_invite"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=False, index=True)
    created_date: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=False), server_default=func.now()
    )
    certification_expiration_date: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=False), server_default=func.now()
    )