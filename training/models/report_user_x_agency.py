from training.models import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey


class ReportUserXAgency(Base):
    __tablename__ = "report_users_x_agencies"
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    agency_id: Mapped[int] = mapped_column(ForeignKey("agencies.id"), primary_key=True)
