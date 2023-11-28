from unittest.mock import patch
from fastapi.testclient import TestClient
from fastapi import status
import jwt
import pytest
from training.config import settings
from training.main import app
from training.repositories import UserRepository
from .factories import UserCreateSchemaFactory, UserSchemaFactory
from training.schemas import UserSearchResult, Agency, Role


@pytest.fixture
def admin_user():
    return {
        'name': 'Albus Dumbledore',
        'email': 'dumbledore@hogwarts.edu',
        'roles': ['Admin']
    }


@pytest.fixture
def goodJWT(admin_user):
    return jwt.encode(admin_user, settings.JWT_SECRET, algorithm="HS256")


client = TestClient(app)


@patch('training.config.settings', 'JWT_SECRET', 'super_secret')
def test_create_user(goodJWT, mock_user_repo: UserRepository):
    user_create = UserCreateSchemaFactory.build()
    mock_user_repo.find_by_email.return_value = None
    mock_user_repo.create.return_value = UserSchemaFactory.build()
    response = client.post(
        "/api/v1/users",
        json=user_create.model_dump(),
        headers={"Authorization": f"Bearer {goodJWT}"}
    )
    assert response.status_code == status.HTTP_201_CREATED


@patch('training.config.settings', 'JWT_SECRET', 'super_secret')
def test_create_user_duplicate(goodJWT, mock_user_repo: UserRepository):
    user_create = UserCreateSchemaFactory.build()
    mock_user_repo.find_by_email.return_value = user_create
    response = client.post(
        "/api/v1/users",
        json=user_create.model_dump(),
        headers={"Authorization": f"Bearer {goodJWT}"}
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@patch('training.config.settings', 'JWT_SECRET', 'super_secret')
def test_get_users(goodJWT, mock_user_repo: UserRepository):
    users = [UserSchemaFactory.build(name="test name") for x in range(2)]
    user_search_result = UserSearchResult(users=users, total_count=2)
    mock_user_repo.get_users.return_value = user_search_result
    response = client.get(
        "/api/v1/users?searchText=test&page_number=1",
        headers={"Authorization": f"Bearer {goodJWT}"}
    )
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 2
    assert response.json()["total_count"] == 2
    assert response.json()["users"] == [user.model_dump() for user in users]


def test_edit_user_for_reporting(mock_user_repo: UserRepository, goodJWT: str):
    user = UserSchemaFactory.build(roles=[])
    mock_user_repo.create(user)
    agency = Agency(id=3, name='test agency')
    user.report_agencies.append(agency)
    role = Role(id=2, name="Report")
    user.roles.append(role)

    mock_user_repo.edit_user_for_reporting.return_value = user
    user_id = user.id
    URL = f"/api/v1/users/edit-user-for-reporting?user_id={user_id}"
    response = client.patch(
        URL,
        json=[3],
        headers={"Authorization": f"Bearer {goodJWT}"}
    )
    assert response.status_code == status.HTTP_200_OK
    assert role.model_dump() in response.json()["roles"]
    assert agency.model_dump() in response.json()["report_agencies"]


def test_edit_user_details(mock_user_repo: UserRepository, goodJWT: str):
    updated_user = UserSchemaFactory.build()
    updated_user.name = "some name"
    updated_user.agency_id = 1
    mock_user_repo.update_user.return_value = updated_user
    user_id = updated_user.id
    URL = f"/api/v1/users/{user_id}"
    response = client.put(
        URL,
        json=updated_user.model_dump(),
        headers={"Authorization": f"Bearer {goodJWT}"}
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["name"] == updated_user.name
    assert response.json()["agency_id"] == updated_user.agency_id
