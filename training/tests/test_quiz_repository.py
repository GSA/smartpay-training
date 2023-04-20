from training import schemas
from training.repositories import QuizRepository


def test_create(quiz_repo_empty: QuizRepository, valid_quiz_create: schemas.QuizCreate):
    db_quiz = quiz_repo_empty.create(valid_quiz_create)
    assert db_quiz.id
    assert db_quiz.name == valid_quiz_create.name


def test_create_duplicate(quiz_repo_empty: QuizRepository, valid_quiz_create: schemas.QuizCreate):
    existing_quiz = quiz_repo_empty.create(valid_quiz_create)
    assert existing_quiz.active
    duplicate_quiz = quiz_repo_empty.create(valid_quiz_create)
    assert duplicate_quiz.active
    assert not existing_quiz.active


def test_find_by_type(quiz_repo_with_data: QuizRepository):
    result = quiz_repo_with_data.find_all(filters={
        "topic": schemas.QuizTopic.Travel,
        "audience": schemas.QuizAudience.AccountHoldersApprovingOfficials,
        "active": True
    })
    assert len(result) == 1
    assert result[0].name == "Travel Training for Ministry of Magic"


def test_find_by_nonexistent_type(quiz_repo_with_data: QuizRepository):
    result = quiz_repo_with_data.find_all(filters={
        "topic": "Nonexistent"
    })
    assert result == []


def test_find_by_id(quiz_repo_with_data: QuizRepository, valid_quiz_ids: list[int]):
    result = quiz_repo_with_data.find_by_id(valid_quiz_ids[0])
    assert result is not None
    assert result.id == valid_quiz_ids[0]


def test_find_by_nonexistent_id(quiz_repo_with_data: QuizRepository, valid_quiz_ids: list[int]):
    nonexistent_quiz_id = 0
    while nonexistent_quiz_id in valid_quiz_ids:
        nonexistent_quiz_id += 1
    result = quiz_repo_with_data.find_by_id(nonexistent_quiz_id)
    assert result is None


def test_find_all(quiz_repo_with_data: QuizRepository, testdata: dict):
    result = quiz_repo_with_data.find_all()
    names = list(map(lambda r: r.name, result))
    for valid_quiz in testdata["quizzes"]:
        assert valid_quiz["name"] in names


def test_delete_by_id(quiz_repo_with_data: QuizRepository, valid_quiz_ids: list[int]):
    quiz_repo_with_data.delete_by_id(valid_quiz_ids[0])
    assert quiz_repo_with_data.find_by_id(valid_quiz_ids[0]) is None
