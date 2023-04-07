from sqlalchemy.orm import Session
from training import models, schemas
from .base import BaseRepository


class AgencyRepository(BaseRepository[models.Agency]):

    def __init__(self, session: Session):
        super().__init__(session, models.Agency)

    def create(self, agency: schemas.AgencyCreate) -> models.Agency:
        return self.save(models.Agency(name=agency.name))

    def find_by_name(self, name: str) -> models.Agency | None:
        return self._session.query(models.Agency).filter(models.Agency.name == name).first()
