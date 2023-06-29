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
        json=user_create.dict(),
        headers={"Authorization": f"Bearer {goodJWT}"}
    )
    assert response.status_code == status.HTTP_201_CREATED


@patch('training.config.settings', 'JWT_SECRET', 'super_secret')
def test_create_user_duplicate(goodJWT, mock_user_repo: UserRepository):
    user_create = UserCreateSchemaFactory.build()
    mock_user_repo.find_by_email.return_value = user_create
    response = client.post(
        "/api/v1/users",
        json=user_create.dict(),
        headers={"Authorization": f"Bearer {goodJWT}"}
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@patch('training.config.settings', 'JWT_SECRET', 'super_secret')
def test_get_users_all(goodJWT, mock_user_repo: UserRepository):
    users = [UserSchemaFactory.build() for x in range(3)]
    mock_user_repo.find_all.return_value = users
    response = client.get(
        "/api/v1/users",
        headers={"Authorization": f"Bearer {goodJWT}"}
    )
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 3


@patch('training.config.settings', 'JWT_SECRET', 'super_secret')
def test_get_users_by_agency(goodJWT, mock_user_repo: UserRepository):
    users = [UserSchemaFactory.build(agency_id=2) for x in range(5)]
    mock_user_repo.find_by_agency.return_value = users
    response = client.get(
        "/api/v1/users?agency_id=2",
        headers={"Authorization": f"Bearer {goodJWT}"}
    )
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 5


def test_get_user(mock_user_repo: UserRepository):
    user = UserSchemaFactory.build(id=1)
    mock_user_repo.find_by_id.return_value = user
    response = client.get(
        "/api/v1/users/1"
    )
    assert response.status_code == status.HTTP_200_OK


def test_get_user_invalid_id(mock_user_repo: UserRepository):
    mock_user_repo.find_by_id.return_value = None
    response = client.get(
        "/api/v1/users/1"
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND


@patch('training.config.settings', 'JWT_SECRET', 'super_secret')
def test_search_users_by_name(goodJWT, mock_user_repo: UserRepository):
    users = [UserSchemaFactory.build(name="test name") for x in range(2)]
    user_search_result = UserSearchResult(users=users, total_count=2)
    mock_user_repo.search_users_by_name.return_value = user_search_result
    response = client.get(
        "/api/v1/users/search-users-by-name/test?page_number=1",
        headers={"Authorization": f"Bearer {goodJWT}"}
    )
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 2
    assert response.json()["total_count"] == 2
    assert response.json()["users"] == users


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
    response = client.put(
        URL,
        json=[3],
        headers={"Authorization": f"Bearer {goodJWT}"}
    )
    assert response.status_code == status.HTTP_200_OK
    assert role in response.json()["roles"]
    assert agency in response.json()["report_agencies"]
