import os

import yaml
from training.database import SessionLocal
from training.schemas import AgencyCreate
from training.repositories import AgencyRepository


agencies_seed_source = os.path.join(os.path.dirname(__file__), "..", "..", "data", "agencies_bureaus.yaml")

with open(agencies_seed_source) as f:
    data = yaml.safe_load(f)

repo = AgencyRepository(SessionLocal())

for item in data:
    agency = AgencyCreate(name=item['name'], bureau=item['bureau'])
    print("Agency:", agency.name, "Bureau:", agency.bureau, end=" - ")
    if repo.find_by_name(agency):
        print("already exists, skipping")
    else:
        repo.create(agency)
        print("added")
