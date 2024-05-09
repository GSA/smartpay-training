from sqlalchemy.orm import Session
from training import models
from training.schemas.user_certificate import UserCertificate
from .base import BaseRepository


class CertificateRepository(BaseRepository[models.QuizCompletion]):

    def __init__(self, session: Session):
        super().__init__(session, models.QuizCompletion)

    def get_certificate_by_id(self, id: int) -> UserCertificate | None:

        result = (self._session.query(models.QuizCompletion.id.label("id"), models.User.id.label("user_id"),
                                      models.User.name.label("user_name"), models.Quiz.id.label("quiz_id"),
                                      models.Agency.name.label("agency"), models.Quiz.name.label("quiz_name"),
                                      models.QuizCompletion.submit_ts.label("completion_date")
                                      )
                               .join(models.User, models.QuizCompletion.user_id == models.User.id)
                               .join(models.Agency, models.User.agency_id == models.Agency.id)
                               .join(models.Quiz, models.QuizCompletion.quiz_id == models.Quiz.id)
                               .filter(models.QuizCompletion.passed, models.QuizCompletion.id == id)
                               .first())
        return result

    def get_certificates_by_userid(self, user_id: int) -> list[UserCertificate]:
        results = (self._session.query(models.QuizCompletion.id.label("id"), models.User.id.label("user_id"),
                                       models.User.name.label("user_name"), models.Quiz.id.label("quiz_id"),
                                       models.Agency.name.label("agency"), models.Quiz.name.label("quiz_name"),
                                       models.Quiz.name.label("quiz_name"), models.QuizCompletion.submit_ts.label("completion_date"))
                                .join(models.User, models.QuizCompletion.user_id == models.User.id)
                                .join(models.Agency, models.User.agency_id == models.Agency.id)
                                .join(models.Quiz, models.QuizCompletion.quiz_id == models.Quiz.id)
                                .filter(models.QuizCompletion.passed, models.User.id == user_id).all())
        return results
    