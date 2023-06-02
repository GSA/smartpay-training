from sqlalchemy.orm import Session
from training import models, schemas
from training.schemas.agency import AgencyWithBureaus, Bureau
from .base import BaseRepository


class AgencyRepository(BaseRepository[models.Agency]):

    def __init__(self, session: Session):
        super().__init__(session, models.Agency)

    def create(self, agency: schemas.AgencyCreate) -> models.Agency:
        db_agency = self.find_by_name(agency)
        if db_agency:
            raise Exception("record already exists in DB")
        if agency.bureau and agency.bureau.strip() == '':
            bureau_value = None
        else:
            bureau_value = agency.bureau
        return self.save(models.Agency(name=agency.name, bureau=bureau_value))

    def find_by_name(self, agency: schemas.AgencyCreate) -> models.Agency | None:
        return self._session.query(models.Agency).filter(models.Agency.name == agency.name, models.Agency.bureau == agency.bureau).first()

    def get_agencies_with_bureaus(self) -> list[AgencyWithBureaus]:
        db_results = self.find_all()
        transform_angecies = {}
        for record in db_results:
            transform_angecies.setdefault(record.name, {'id': record.id, 'name': record.name, 'bureaus': []})
        if record.bureau:
            transform_angecies[record.name]['bureaus'].append(Bureau(id=record.id, name=record.bureau))
        else:
            transform_angecies[record.name]['id'] = record.id
        return list(transform_angecies.values())
