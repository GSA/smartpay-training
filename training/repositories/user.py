from sqlalchemy import nullsfirst, or_
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
        # edit_user_for_reporting allow admin to assign report role and associate report agencies to specific user
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
                    # if Report role is not in DB, add it to DB (should not happen if data is prepopulated properly via seed.py and no direct DB removal)
                    role = models.Role(name="Report")
                    self._session.add(role)
                    self._session.commit()
                    db_user.roles.append(role)
        else:
            # if report_agencies_list =[], it will remove all user associated agencies and thus remove user report role.
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

    def get_users(self, searchText: str, page_number: int) -> UserSearchResult:
        # current UI only support search by user name and email. The search field it is required field.
        if (searchText and searchText.strip() != '' and page_number > 0):
            count = self._session.query(models.User).filter(or_(models.User.name.ilike(f"%{searchText}%"), models.User.email.ilike(f"%{searchText}%"))).count()
            page_size = 25
            offset = (page_number - 1) * page_size
            search_results = self._session.query(models.User).filter(
                or_(models.User.name.ilike(f"%{searchText}%"), models.User.email.ilike(f"%{searchText}%"))).limit(page_size).offset(offset).all()
            user_search_result = UserSearchResult(users=search_results, total_count=count)
            return user_search_result

    def update_user(self, user_id: int, user: schemas.UserUpdate) -> models.User:
        """
        Updates user name and agency values
        :param user_id: User's ID to update
        :param user: User object with updated values
        :return: Updated User object
        """
        db_user = self.find_by_id(user_id)
        if db_user is None:
            raise ValueError("invalid user id")
        db_user.name = user.name
        db_user.agency_id = user.agency_id
        self._session.commit()
        return db_user
