import csv
from io import StringIO
from typing import List
from training.api.auth import RequireRole
from fastapi import APIRouter, status, HTTPException, Response, Depends
from training.schemas import User, UserCreate, UserSearchResult
from training.repositories import UserRepository
from training.api.deps import user_repository
from training.api.auth import user_from_form


router = APIRouter()


@router.post("/users", response_model=User, status_code=status.HTTP_201_CREATED)
def create_user(
    new_user: UserCreate,
    repo: UserRepository = Depends(user_repository),
    user=Depends(RequireRole(["Admin"]))
):
    db_user = repo.find_by_email(new_user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User email address already exists"
        )
    db_user = repo.create(user)
    return db_user


@router.get("/users", response_model=List[User])
def get_users(
    agency_id: int | None = None,
    repo: UserRepository = Depends(user_repository),
    user=Depends(RequireRole(["Admin"]))
):
    if agency_id:
        return repo.find_by_agency(agency_id)
    else:
        # If agency_id is <= 0 or None, return all users:
        return repo.find_all()


@router.get("/users/{id}", response_model=User)
def get_user(id: int, repo: UserRepository = Depends(user_repository)):
    db_user = repo.find_by_id(id)
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return db_user


@router.put("/users/edit-user-for-reporting", response_model=User)
def edit_user_by_id(user_id: int, agency_id_list: list[int], repo: UserRepository = Depends(user_repository)):
    try:
        return repo.edit_user_for_reporting(user_id, agency_id_list)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="invalid user id or agencies ids"
        )


@router.post("/users/download-user-quiz-completion-report")
def download_report_csv(user=Depends(user_from_form), repo: UserRepository = Depends(user_repository)):
    try:
        results = repo.get_user_quiz_completion_report(user['id'])
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="invalid report user"
        )

    output = StringIO()
    writer = csv.writer(output)

    # header row
    writer.writerow(['Full Name', 'Email Address', 'Agency', 'Bureau', 'Quiz Name', 'Quiz Completion Date'])
    for item in results:
        # data row
        writer.writerow([item.name, item.email, item.agency, item.bureau, item.quiz, item.completion_date.strftime("%m/%d/%Y")])  # noqa 501

    headers = {'Content-Disposition': 'attachment; filename="SmartPayTrainingQuizCompletionReport.csv"'}
    return Response(output.getvalue(), headers=headers, media_type='application/csv')


@router.get("/users/search-users-by-name/{name}", response_model=UserSearchResult)
def search_users_by_name(
    name: str,
    page_number: int,
    repo: UserRepository = Depends(user_repository),
    user=Depends(RequireRole(["Admin"]))
):
    try:
        return repo.search_users_by_name(name, page_number)

    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="invalid search criteria"
        )
