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

    def edit_user_roles(self, user_id: int, role_id_list: list[int]) -> models.User:
        db_user = self._session.query(models.User).filter(models.User.id == user_id).first()
        if db_user is None:
            raise Exception("no such user in DB")
        db_user.roles.clear()
        for role_id in role_id_list:
            role = self._session.query(models.Role).filter(models.Role.id == role_id).first()
            db_user.roles.append(role)
        self._session.commit()
        return db_user
