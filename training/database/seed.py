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
    fas = AgencyCreate(name="U.S. General Services Administration", bureau="Federal Acquisition Service")
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

# load AOPCs data
for item in data["AOPSs"]:
    # find user's agency
    user_agency = user_repo._session.query(models.Agency).filter(models.Agency.name == item['agency'] and models.Agency.bureau == item['bureau']).first()
    user = UserCreate(name=item['name'], email=item['email'], agency_id=user_agency.id)
    print("AOPC User:", user.name, "email:", user.email, "user_agency:", user_agency.name, "user_bureau:", user_agency.bureau, end=" - ")
    if user_repo.find_by_email(user.email):
        print("already exists, skipping")
    else:
        user_repo.create(user)
        print("added")
    user_for_edit = user_repo.find_by_email(user.email)
    report_role_exists = any(role.name == "Report" for role in user_for_edit.roles)
    if report_role_exists:
        print("Report role already exisits, skipping")
    else:
        role = user_repo._session.query(models.Role).filter(models.Role.name == "Report").first()
        user_for_edit.roles.append(role)
        user_repo._session.commit()
        print("Report role added")
    for objAgency in item['reporting_agencies']:
        # use repo's own session to find its object to avoid object attached to multiple sessions issue when you need to update DB data
        user_report_agency = user_repo._session.query(models.Agency).filter(models.Agency.name == objAgency['report_agency']
                                                                            and models.Agency.bureau == objAgency['report_bureau']).first()
        if (user_report_agency in user_for_edit.report_agencies):
            print("Report Agency: ", user_report_agency.name, "Report bureau: ", user_report_agency.bureau,  " already exists, skipping")
        else:
            user_for_edit.report_agencies.append(user_report_agency)
            user_repo._session.commit()
            print("Report Agency: ", user_report_agency.name, "Report bureau: ", user_report_agency.bureau,  " added")
