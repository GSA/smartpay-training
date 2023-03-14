from typing import Optional
from training import models, schemas
from .base import BaseRepository


class AgencyRepository(BaseRepository):
    __model__ = models.Agency

    def create(self, agency: schemas.AgencyCreate) -> models.Agency:
        return self.save(models.Agency(name=agency.name))

    def find_by_name(self, name: str) -> Optional[models.Agency]:
        return self._session.query(models.Agency).filter(models.Agency.name == name).first()
