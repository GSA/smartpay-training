from sqlalchemy.orm import Session
from sqlalchemy import desc, literal
from training import models, schemas
from .base import BaseRepository


class GspcCompletionRepository(BaseRepository[models.GspcCompletion]):

    def __init__(self, session: Session):
        super().__init__(session, models.GspcCompletion)

    def create(self, gspc_completion: schemas.GspcCompletion) -> models.GspcCompletion:
        return self.save(models.GspcCompletion(
            user_id=gspc_completion.user_id,
            passed=gspc_completion.passed,
            certification_expiration_date=gspc_completion.certification_expiration_date,
            responses=gspc_completion.responses
        ))

    def get_gspc_completion_report(self):
        completed_results = self._get_completed_gspc_results()
        uncompleted_results = self._get_uncompleted_gspc_results()
        return completed_results + uncompleted_results

    def _get_completed_gspc_results(self):
        result = (
            self._session.query(
                models.GspcInvite.email.label("invitedEmail"),
                models.User.email.label("registeredEmail"),
                models.User.name.label("username"),
                models.Agency.name.label("agency"),
                models.Agency.bureau.label("bureau"),
                models.GspcCompletion.passed.label("passed"),
                models.GspcCompletion.submit_ts.label("completionDate")
            )
            .select_from(models.GspcCompletion)
            .join(models.User)
            .join(models.Agency)
            .outerjoin(models.GspcInvite, models.User.email == models.GspcInvite.email)
            .distinct()
            .order_by(desc(models.GspcCompletion.passed), models.GspcCompletion.submit_ts)
        ).all()

        return result

    def _get_uncompleted_gspc_results(self):
        # Subquery to get all emails from User that are referenced in GspcCompletion
        subquery = (
            self._session.query(models.User.email)
            .select_from(models.User)
            .join(models.GspcCompletion, models.GspcCompletion.user_id == models.User.id)
            .subquery()
        )

        # Query to get all unique emails from GspcInvite that are not in the subquery
        result = (
            self._session.query(
                models.GspcInvite.email.label("invitedEmail"),
                literal(None).label('registeredEmail'),
                literal(None).label('username'),
                literal(None).label('agency'),
                literal(None).label('bureau'),
                literal(None).label('passed'),
                literal(None).label('completionDate')
            )
            .select_from(models.GspcInvite)
            .outerjoin(subquery, models.GspcInvite.email == subquery.c.email)
            .filter(subquery.c.email.is_(None))
            .distinct()
        ).all()

        return result
