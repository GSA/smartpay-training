from training.models import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from training.models.agency import Agency
from training.models.role import Role
from datetime import datetime


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True, index=True)
    name: Mapped[str] = mapped_column()
    agency_id: Mapped[int] = mapped_column(ForeignKey("agencies.id"))
    agency: Mapped[Agency] = relationship()
    roles: Mapped[list[Role]] = relationship(secondary="users_x_roles")
    report_agencies: Mapped[list[Agency]] = relationship(secondary="report_users_x_agencies")
    created_on: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now(), nullable=False)
    created_by: Mapped[str] = mapped_column(nullable=False)
    modified_on: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    modified_by: Mapped[str] = mapped_column()
