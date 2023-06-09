from typing import List
from fastapi import APIRouter, status, HTTPException, Depends
from training.schemas import User, UserCreate, UserQuizCompletionReportData
from training.repositories import UserRepository
from training.api.deps import user_repository


router = APIRouter()


@router.post("/users", response_model=User, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, repo: UserRepository = Depends(user_repository)):
    db_user = repo.find_by_email(user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User email address already exists"
        )
    db_user = repo.create(user)
    return db_user


@router.get("/users", response_model=List[User])
def get_users(agency_id: int | None = None, repo: UserRepository = Depends(user_repository)):
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


@router.get("/users/user-quiz-report-data/{report_user_id}", response_model=List[UserQuizCompletionReportData])
def get_user_quiz_completion_report(report_user_id: int | None = None, repo: UserRepository = Depends(user_repository)):
    try:
        return repo.get_user_quiz_completion_report(report_user_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="invalid report user id"
        )
