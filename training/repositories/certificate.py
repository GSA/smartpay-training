from sqlalchemy.orm import Session
from training import models
from training.schemas.user_cerificate import UserCertificate
from .base import BaseRepository


class CertificateRepository(BaseRepository[models.QuizCompletion]):

    def __init__(self, session: Session):
        super().__init__(session, models.QuizCompletion)

    def get_certificate_by_id(self, id: int) -> models.QuizCompletion | None:
        return self._session.query(models.QuizCompletion).filter(models.QuizCompletion.id == id, models.QuizCompletion.passed).first()

    def get_certificates_by_userid(self, user_id: int) -> list[UserCertificate]:
        results = (self._session.query(models.User.id.label("user_id"), models.User.name.label("user_name"), models.Quiz.id.label("quiz_id"),
                                       models.Quiz.name.label("quiz_name"), models.QuizCompletion.submit_ts.label("completion_date")).join(models.User)
                   .join(models.Quiz).filter(models.QuizCompletion.passed, models.User.id == user_id).all())
        return results
