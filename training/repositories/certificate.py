from sqlalchemy.orm import Session
from sqlalchemy import literal
from training import models
from training.schemas import UserCertificate, GspcCertificate, CertificateType, CertificateListValue
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

    def get_all_certificates_by_userid(self, user_id: int) -> list[CertificateListValue]:
        quiz_results = (self._session.query(models.QuizCompletion.id.label("id"), models.User.id.label("user_id"),
                                            models.User.name.label("user_name"), models.Quiz.name.label("cert_title"),
                                            models.QuizCompletion.submit_ts.label("completion_date"),
                                            literal(CertificateType.QUIZ.value).label('certificate_type'))
                            .join(models.User, models.QuizCompletion.user_id == models.User.id)
                            .join(models.Agency, models.User.agency_id == models.Agency.id)
                            .join(models.Quiz, models.QuizCompletion.quiz_id == models.Quiz.id)
                            .filter(models.QuizCompletion.passed, models.User.id == user_id).all())

        gspc_results = (self._session.query(models.GspcCompletion.id.label("id"), models.User.id.label("user_id"),
                                            models.User.name.label("user_name"), literal("GSA SmartPay Program Certification (GSPC)").label('cert_title'),
                                            models.GspcCompletion.submit_ts.label("completion_date"),
                                            literal(CertificateType.GSPC.value).label('certificate_type'))
                            .join(models.User, models.GspcCompletion.user_id == models.User.id)
                            .join(models.Agency, models.User.agency_id == models.Agency.id)
                            .filter(models.GspcCompletion.passed, models.User.id == user_id).all())

        results = quiz_results + gspc_results
        sorted_results = sorted(results, key=lambda x: x.completion_date, reverse=False)
        return sorted_results

    def get_gspc_certificate_by_id(self, id: int) -> GspcCertificate | None:

        result = (self._session.query(models.GspcCompletion.id.label("id"), models.User.id.label("user_id"),
                                      models.User.name.label("user_name"), models.Agency.name.label("agency"),
                                      models.GspcCompletion.submit_ts.label("completion_date"),
                                      models.GspcCompletion.certification_expiration_date.label("certification_expiration_date"))
                  .join(models.User, models.GspcCompletion.user_id == models.User.id)
                  .join(models.Agency, models.User.agency_id == models.Agency.id)
                  .filter(models.GspcCompletion.passed, models.GspcCompletion.id == id)
                  .first())
        return result
