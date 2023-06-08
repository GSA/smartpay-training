from sqlalchemy.orm import Session
from training import models, schemas
from .base import BaseRepository


class RoleRepository(BaseRepository[models.Role]):

    def __init__(self, session: Session):
        super().__init__(session, models.Role)

    def create(self, role: schemas.RoleCreate) -> models.Role:
        return self.save(models.Role(name=role.name))

    def find_by_name(self, name: str) -> models.Role | None:
        return self._session.query(models.Role).filter(models.Role.name == name).first()
