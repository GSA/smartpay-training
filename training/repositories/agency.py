from sqlalchemy.orm import Session
from training import models, schemas
from training.schemas.agency import AgencyWithBureaus, Bureau
from .base import BaseRepository
from sqlalchemy.sql.expression import collate


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
        db_results = self._session.query(models.Agency).order_by(collate(models.Agency.name, 'C')).all()
        parent_agencies = [record for record in db_results if record.bureau is None]
        
        # For UI display, sort all parent agency by alphabetical order except for 'Other', 'Other" needs to be placed at the bottom of the list.
        other_agency = [record for record in parent_agencies if record.name.lower() == 'other']
        rest_agencies = [record for record in parent_agencies if record.name.lower() != 'other']
        sorted_parent_agencies = rest_agencies + other_agency
        
        transform_angecies = []
        for record in sorted_parent_agencies:
            agency_with_bureaus = [obj for obj in db_results if obj.bureau and obj.name == record.name]
            bureaus = []
            if len(agency_with_bureaus) > 0:
                sorted_bureaus = sorted(agency_with_bureaus, key=lambda x: x.bureau)
                other_bureau = {}
                for obj in sorted_bureaus:
                    bureau = Bureau(id=obj.id, name=obj.bureau)
                    # for bureau name that is not 'Other', add them in alphebetic order
                    if (bureau.name.lower() != 'other'):
                        bureaus.append(bureau)
                    else:
                        other_bureau = bureau
                # if agency has "Other" bureau, put it all the way in the end
                if (other_bureau.id):
                    bureaus.append(other_bureau)

            transform_angecies.append({
                'id': record.id,
                'name': record.name,
                'bureaus': bureaus
            })
        return transform_angecies
