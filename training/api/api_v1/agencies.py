from typing import List
from fastapi import APIRouter, status, HTTPException
from training.schemas import Agency, AgencyCreate
import training.repositories as repo


router = APIRouter()


@router.post(
        "/agencies",
        response_model=Agency,
        status_code=status.HTTP_201_CREATED
)
def create_agency(agency: AgencyCreate):
    db_agency = repo.agency.get_by_name(agency.name)
    if db_agency:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Agency already exists"
        )
    db_agency = repo.agency.create(agency)
    return db_agency


@router.get("/agencies", response_model=List[Agency])
def get_agencies():
    return repo.agency.get_all()


@router.get("/agencies/{id}", response_model=Agency)
def get_agency(id: int):
    db_agency = repo.agency.get(id=id)
    if db_agency is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return db_agency
