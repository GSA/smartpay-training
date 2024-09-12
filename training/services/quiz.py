import logging
from email.message import EmailMessage
from smtplib import SMTP
from string import Template

from training.config import settings
from training.errors import IncompleteQuizResponseError, QuizNotFoundError, SendEmailError
from training.repositories import QuizRepository, QuizCompletionRepository, UserRepository, CertificateRepository
from training.schemas import Quiz, QuizSubmission, QuizGrade, QuizCompletionCreate
from sqlalchemy.orm import Session

from training.services import Certificate

CERTIFICATE_EMAIL_TEMPLATE = Template('''
<p>Hello $name,</p>

<p>
Congratulations!
</p>
<p>You've successfully passed the GSA SmartPay® $course_name quiz.</p>
<p>Your certificate is attached below.</p>
<p>
If you did not submit this request, you may be receiving this message in error. Please disregard this email. If you have any questions or need further
 assistance, email us at gsa_smartpay@gsa.gov.
</p>
<p>Thank you.</p>
''')


class QuizService():
    def __init__(self, db: Session):
        self.quiz_repo = QuizRepository(db)
        self.quiz_completion_repo = QuizCompletionRepository(db)
        self.user_repo = UserRepository(db)
        self.certificate_repo = CertificateRepository(db)
        self.certificate_service = Certificate()

    def grade(self, quiz_id: int, user_id: int, submission: QuizSubmission) -> QuizGrade:
        """
        Grades quizzes submitted by user. Sends congratulation email if user passes the quiz.
        :param quiz_id: Quiz ID
        :param user_id: User ID
        :param submission: Quiz submission object
        :return: QuizGrade model which includes quiz results
        """
        db_quiz = self.quiz_repo.find_by_id(quiz_id)
        if db_quiz is None:
            raise QuizNotFoundError

        quiz = Quiz.model_validate(db_quiz)
        correct_count = 0
        question_count = len(quiz.content.questions)
        questions = []
        questions_without_responses = []

        for question in quiz.content.questions:
            # From the submission, get the response matching the current question
            response = next((r for r in submission.responses if r.question_id == question.id), None)
            if response is None:
                questions_without_responses.append(question.id)
                continue

            # Get a list of correct choice IDs from the answer sheet
            correct_ids = [choice.id for choice in question.choices if choice.correct]

            # Verify whether the set of response IDs match the correct choice IDs
            response_correct = set(correct_ids) == set(response.response_ids)
            if response_correct:
                correct_count += 1

            # Mark the question response as correct or incorrect
            questions.append({
                "question_id": question.id,
                "correct": response_correct,
                "selected_ids": response.response_ids,
                "correct_ids": correct_ids,
            })

        if questions_without_responses:
            raise IncompleteQuizResponseError(questions_without_responses)

        percentage = correct_count / question_count
        passed = percentage >= 0.75

        # Strip out the correct answers if the user didn't pass
        if not passed:
            for question in questions:
                question["correct_ids"] = []

        grade = QuizGrade(
            quiz_id=quiz_id,
            correct_count=correct_count,
            question_count=question_count,
            percentage=percentage,
            passed=passed,
            questions=questions,
            quiz_completion_id=None
        )

        responses_dict = submission.model_dump()

        result = self.quiz_completion_repo.create(QuizCompletionCreate(
            quiz_id=quiz_id,
            user_id=user_id,
            passed=grade.passed,
            responses=responses_dict
        ))

        grade.quiz_completion_id = result.id

        if passed:
            # Send email with quiz completion attached
            try:
                user = self.user_repo.find_by_id(user_id)
                db_user_certificate = self.certificate_repo.get_certificate_by_id(result.id)
                pdf_bytes = self.certificate_service.generate_pdf(
                    db_user_certificate.quiz_name,
                    db_user_certificate.user_name,
                    db_user_certificate.agency,
                    db_user_certificate.completion_date
                )
                self.email_certificate(user.name, quiz.name, user.email, pdf_bytes)
                logging.info(f"Sent confirmation email to {user.email} for passing training quiz")
            except Exception as e:
                logging.error("Error sending quiz confirmation mail", e)
                raise

        return grade

    def email_certificate(self, user_name: str, course_name: str, to_email: str, certificate: bytes) -> None:
        """
        Sends congratulatory email to user with certificate attached.
        :param user_name: User's Name
        :param course_name: Name of course user completed
        :param to_email: User's email
        :param certificate: Certificate PDF file
        :return: N/A
        """
        body = CERTIFICATE_EMAIL_TEMPLATE.substitute({"name": user_name, "course_name": course_name})
        message = EmailMessage()
        message.set_content(body, subtype="html")
        message["Subject"] = "Certificate - GSA SmartPay " + course_name
        message["From"] = f"{settings.EMAIL_FROM_NAME} <{settings.EMAIL_FROM}>"
        message["To"] = to_email
        message.add_attachment(certificate, maintype="application", subtype="pdf", filename="SmartPayTraining.pdf")

        with SMTP(settings.SMTP_SERVER, port=settings.SMTP_PORT) as smtp:
            smtp.starttls()
            if settings.SMTP_USER and settings.SMTP_PASSWORD:
                smtp.login(user=settings.SMTP_USER, password=settings.SMTP_PASSWORD)
            try:
                smtp.send_message(message)
            except Exception as e:
                raise SendEmailError from e
            finally:
                smtp.quit()
