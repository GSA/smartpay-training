from typing import List
from fastapi import APIRouter, status, HTTPException, Depends
from training.schemas import Agency, AgencyCreate
from training.repositories import AgencyRepository
from training.api.deps import agency_repository
from training.schemas.agency import AgencyWithBureaus


router = APIRouter()


@router.post("/agencies", response_model=Agency, status_code=status.HTTP_201_CREATED)
def create_agency(agency: AgencyCreate, repo: AgencyRepository = Depends(agency_repository)):
    db_agency = repo.find_by_name(agency)
    if db_agency:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Agency already exists"
        )
    db_agency = repo.create(agency)
    return db_agency


@router.get("/agencies", response_model=List[AgencyWithBureaus])
def get_agencies(repo: AgencyRepository = Depends(agency_repository)):
    return repo.get_agencies_with_bureaus()


@router.get("/agencies/{id}", response_model=Agency)
def get_agency(id: int, repo: AgencyRepository = Depends(agency_repository)):
    db_agency = repo.find_by_id(id)
    if db_agency is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return db_agency
