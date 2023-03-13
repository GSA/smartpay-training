from training.database import Session
from training import models, schemas


class AgencyRepository:
    def create(self, agency: schemas.AgencyCreate, db=Session()):
        db_agency = models.Agency(name=agency.name)
        db.add(db_agency)
        db.commit()
        db.refresh(db_agency)
        return db_agency

    def get(self, id: int, db=Session()):
        return db.query(models.Agency).filter(models.Agency.id == id).first()

    def get_by_name(self, name: str, db=Session()):
        return db.query(models.Agency).filter(models.Agency.name == name).first()

    def get_all(self, db=Session()):
        return db.query(models.Agency).all()


agency = AgencyRepository()
