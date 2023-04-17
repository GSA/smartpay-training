from training.errors import IncompleteQuizResponseError, QuizNotFoundError
from training.repositories import QuizRepository, QuizCompletionRepository
from training.schemas import Quiz, QuizSubmission, QuizGrade, QuizCompletionCreate
from sqlalchemy.orm import Session


class QuizService():
    def __init__(self, db: Session):
        self.quiz_repo = QuizRepository(db)
        self.quiz_completion_repo = QuizCompletionRepository(db)

    def grade(self, quiz_id: int, user_id: int, submission: QuizSubmission) -> QuizGrade:
        db_quiz = self.quiz_repo.find_by_id(quiz_id)
        if db_quiz is None:
            raise QuizNotFoundError

        quiz = Quiz.from_orm(db_quiz)
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
                "correct": response_correct
            })

        if questions_without_responses:
            raise IncompleteQuizResponseError(questions_without_responses)

        grade = QuizGrade(
            quiz_id=quiz_id,
            correct_count=correct_count,
            question_count=question_count,
            percentage=(correct_count / question_count),
            passed=((correct_count / question_count) >= 0.75),
            questions=questions,
        )

        self.quiz_completion_repo.create(QuizCompletionCreate(
            quiz_id=quiz_id,
            user_id=user_id,
            passed=grade.passed
        ))

        return grade
