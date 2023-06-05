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
        db_results = self._session.query(models.Agency).order_by(models.Agency.name.asc()).all()
        parent_agencies = [record for record in db_results if record.bureau is None]
        transform_angecies = []
        for record in parent_agencies:
            agency_with_bureaus = [obj for obj in db_results if obj.bureau and obj.name == record.name]
            bureaus = []
            if len(agency_with_bureaus) > 0:
                for obj in agency_with_bureaus:
                    bureau = Bureau(id=obj.id, name=obj.bureau)
                    bureaus.append(bureau)

            transform_angecies.append({
                'id': record.id,
                'name': record.name,
                'bureaus': bureaus
            })
        return transform_angecies
