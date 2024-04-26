from training.schemas import GspcSubmission, GspcResult
from sqlalchemy.orm import Session


class GspcService():
    def __init__(self, db: Session):
        pass

    def grade(self, user_id: int, submission: GspcSubmission) -> GspcResult:
        """
        Grades a GspcSubmission submitted by user. Sends congratulation email if user meets the criteria.
        :param user_id: User ID
        :param submission: Quiz submission object
        :return: GspcResult model which includes the final result
        """

        passed = all(question.correct for question in submission.responses)

        # Todo
        # - Save Submission
        # - Generate and save cert
        # - Send Email on pass

        result = GspcResult(
            passed=passed,
        )

        return result
