from sqlalchemy.orm import Session
from training import models, schemas
from .base import BaseRepository


class UserRepository(BaseRepository[models.User]):

    def __init__(self, session: Session):
        super().__init__(session, models.User)

    def create(self, user: schemas.UserCreate) -> models.User:
        return self.save(models.User(email=user.email, name=user.name, agency_id=user.agency_id))

    def find_by_email(self, email: str) -> models.User | None:
        return self._session.query(models.User).filter(models.User.email == email).first()

    def find_by_agency(self, agency_id: int) -> list[models.User]:
        return self._session.query(models.User).filter(models.User.agency_id == agency_id).all()
