from sqlalchemy import nullsfirst
from sqlalchemy.orm import Session
from training import models, schemas
from training.schemas import UserQuizCompletionReportData, UserSearchResult
from .base import BaseRepository


class UserRepository(BaseRepository[models.User]):

    def __init__(self, session: Session):
        super().__init__(session, models.User)

    def create(self, user: schemas.UserCreate) -> models.User:
        return self.save(models.User(email=user.email.lower(), name=user.name, agency_id=user.agency_id))

    def find_by_email(self, email: str) -> models.User | None:
        return self._session.query(models.User).filter(models.User.email == email.lower()).first()

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

    def get_admins_users(self) -> list[models.User]:
        return self._session.query(models.User).filter(models.User.roles.any(name='Admin')).all()

    def get_user_quiz_completion_report(self, report_user_id: int) -> list[UserQuizCompletionReportData]:
        report_user = self.find_by_id(report_user_id)
        if report_user and report_user.report_agencies:
            allowed_agency_ids = [obj.id for obj in report_user.report_agencies]
            results = (self._session.query(models.User.name.label("name"), models.User.email.label("email"),
                                           models.Agency.name.label("agency"), models.Agency.bureau.label("bureau"),
                                           models.Quiz.name.label("quiz"), models.QuizCompletion.submit_ts.label("completion_date"))
                       .select_from(models.User)
                       .join(models.Agency)
                       .join(models.QuizCompletion)
                       .join(models.Quiz).filter(models.QuizCompletion.passed, models.User.agency_id.in_(allowed_agency_ids))
                       .order_by(models.Agency.name.asc(), nullsfirst(models.Agency.bureau.asc()), models.QuizCompletion.submit_ts.desc()).all())
            return results
        else:
            raise ValueError("Invalid Report User")

    def search_users_by_name(self, name: str, page_number: int) -> UserSearchResult:
        if (name and name.strip() != '' and page_number > 0):
            count = self._session.query(models.User).filter(models.User.name.ilike(f"%{name}%")).count()
            page_size = 25
            offset = (page_number - 1) * page_size
            search_results = self._session.query(models.User).filter(models.User.name.ilike(f"%{name}%")).limit(page_size).offset(offset).all()
            user_search_result = UserSearchResult(users=search_results, total_count=count)
            return user_search_result
        else:
            raise ValueError("Invalid search criteria")
