import os

import yaml
from training import models
from training.database import SessionLocal
from training.schemas import AgencyCreate, UserCreate, RoleCreate
from training.repositories import AgencyRepository, UserRepository, RoleRepository


seed_source = os.path.join(os.path.dirname(__file__), "..", "..", "data", "seedsdata.yaml")
with open(seed_source) as f:
    data = yaml.safe_load(f)
agency_repo = AgencyRepository(SessionLocal())

for item in data["agencies"]:
    agency = AgencyCreate(name=item['name'], bureau=item['bureau'])
    print("Agency:", agency.name, "Bureau:", agency.bureau, end=" - ")
    if agency_repo.find_by_name(agency):
        print("already exists, skipping")
    else:
        agency_repo.create(agency)
        print("added")

role_repo = RoleRepository(SessionLocal())

for item in data["roles"]:
    role = RoleCreate(name=item['name'])
    print("role:", role.name, end=" - ")
    if role_repo.find_by_name(role.name):
        print("already exists, skipping")
    else:
        role_repo.create(role)
        print("added")

user_repo = UserRepository(SessionLocal())

for item in data["admins"]:
    fas = AgencyCreate(name="General Services Administration", bureau="Federal Acquisition Service")
    smartpay_agency = agency_repo.find_by_name(fas)
    user = UserCreate(name=item['name'], email=item['email'], agency_id=smartpay_agency.id)
    print("User:", user.name, "Email:", user.email, "Agency_id:", smartpay_agency.id, end=" - ")
    if user_repo.find_by_email(user.email):
        print("already exists, skipping user add")
    else:
        user_repo.create(user)
        print("added")
    user_for_edit = user_repo.find_by_email(user.email)
    admin_role_exists = any(role.name == "Admin" for role in user_for_edit.roles)
    if admin_role_exists:
        print("Admin role already exisits, skipping")
    else:
        role = user_repo._session.query(models.Role).filter(models.Role.name == "Admin").first()
        user_for_edit.roles.append(role)
        user_repo._session.commit()
        print("Admin role added")
