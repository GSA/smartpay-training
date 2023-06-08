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

    def edit_user_for_reporting(self, user_id: int, report_agencies_list: list[int]) -> models.User:
        db_user = self._session.query(models.User).filter(models.User.id == user_id).first()
        if db_user is None:
            raise ValueError("invalid user id")
        report_role_exist = [obj for obj in db_user.roles if obj.name == "Report"]
        if len(report_agencies_list) > 0:
            if len(report_role_exist) == 0:
                report_role = self._session.query(models.Role).filter(models.Role.name == "Report").first()
                if report_role:
                    db_user.roles.append(report_role)
                else:
                    role = models.Role(name="Report")
                    self._session.add(role)
                    self._session.commit()
                    db_user.roles.append(role)
        else:
            if len(report_role_exist) > 0:
                db_user.roles = [obj for obj in db_user.roles if obj.name != "Report"]
        db_user.report_agencies.clear()
        for agency_id in report_agencies_list:
            agency = self._session.query(models.Agency).filter(models.Agency.id == agency_id).first()
            if agency:
                db_user.report_agencies.append(agency)
            else:
                raise ValueError("invalid agency associated with this user")
        self._session.commit()
        return db_user
