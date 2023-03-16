import os
from training.database import SessionLocal
from training.schemas import AgencyCreate
from training.repositories import AgencyRepository


agencies_seed_source = os.path.join(os.path.dirname(__file__), "..", "..", "data", "agencies.txt")

with open(agencies_seed_source) as f:
    agency_names = [line.strip() for line in f]

repo = AgencyRepository(SessionLocal())

for agency_name in agency_names:
    print("Agency:", agency_name, end=" - ")
    if repo.find_by_name(agency_name):
        print("already exists, skipping")
    else:
        repo.create(AgencyCreate(name=agency_name))
        print("added")
