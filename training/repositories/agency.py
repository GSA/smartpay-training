
from sqlalchemy import func
from sqlalchemy.orm import Session
from training import models, schemas
from training.schemas.agency import AgencyWithBureaus
from .base import BaseRepository
from sqlalchemy.sql.expression import collate, case
from itertools import groupby


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
        '''
        get agencies_with_bureaus return a list of parent agencies with bureaus list, if parent agency doesn't have bureaus, its bureaus list =[].
        parent agencies are those db records with bureau value is null
        UI want to sort agency alphabetically but needs 'Other' option to be displayed at the end. Both parent agency and bureau has 'Other' option.
        several sort order are combined and is put in a specific order to achieve this.
        group by is used to group same agency together
        '''

        # set 'Other' order rule for both agency and bureau
        agency_other_order = case((models.Agency.name == "Other", 1), else_=0)
        bureau_other_order = case((models.Agency.bureau == "Other", 2), (models.Agency.bureau==None, 0), else_=1)  # noqa E711

        db_results = self._session.query(models.Agency).order_by(
            agency_other_order,  # agency named Other should be at the bottom of parent agencies list
            collate(func.lower(models.Agency.name), 'C'),  # alphabetical order but ignore case on agency's name
            bureau_other_order,  # bureau named 'Other' should be at the bollom of the bureau list
            collate(func.lower(models.Agency.bureau), 'C')  # alphabetical order but ignore case on bureau
            ).all()

        transform_angecies = []
        for _, group in groupby(db_results, lambda row: row.name):
            parent = next(group)  # Parent is first in the group

            transform_angecies.append({
                'id': parent.id,
                'name': parent.name,
                'bureaus': [{"id": b.id, "name": b.bureau} for b in group]
            })
        return transform_angecies
