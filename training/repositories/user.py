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

    def edit_user_by_id(self, user_id: int, role_id_list: list[int], report_agencies_list: list[int]) -> models.User:
        db_user = self._session.query(models.User).filter(models.User.id == user_id).first()
        if db_user is None:
            raise Exception("invalid user id")

        db_user.roles.clear()
        for role_id in role_id_list:
            role = self._session.query(models.Role).filter(models.Role.id == role_id).first()
            if role:
                db_user.roles.append(role)
            else:
                raise Exception("invalid role associated with this user")

        db_user.report_agencies.clear()
        for agency_id in report_agencies_list:
            agency = self._session.query(models.Agency).filter(models.Agency.id == agency_id).first()
            if agency:
                db_user.report_agencies.append(agency)
            else:
                raise Exception("invalid agency associated with this user")
        self._session.commit()
        return db_user

    def edit_user(self, edit_user: schemas.User) -> models.User:
        db_user = self._session.query(models.User).filter(models.User.id == edit_user.id).first()
        if db_user is None:
            raise Exception("invalid user for edit")

        db_user.roles.clear()
        for item in edit_user.roles:
            role = self._session.query(models.Role).filter(models.Role.id == item.id).first()
            if role:
                db_user.roles.append(role)
            else:
                raise Exception("invalid role associated with this user")

        db_user.report_agencies.clear()
        for obj in edit_user.report_agencies:
            agency = self._session.query(models.Agency).filter(models.Agency.id == obj.id).first()
            if agency:
                db_user.report_agencies.append(agency)
            else:
                raise Exception("invalid agency associated with this user")
        self._session.commit()
        return db_user
