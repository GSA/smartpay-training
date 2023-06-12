from training.models import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from training.models.agency import Agency
from training.models.role import Role


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True, index=True)
    name: Mapped[str] = mapped_column()
    agency_id: Mapped[int] = mapped_column(ForeignKey("agencies.id"))
    roles: Mapped[Role] = relationship(secondary="users_x_roles")
    report_agencies: Mapped[Agency] = relationship(secondary="report_users_x_agencies")
