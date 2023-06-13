from fastapi.testclient import TestClient
from fastapi import status
from training.main import app
from training.repositories import UserRepository
from .factories import UserCreateSchemaFactory, UserSchemaFactory


client = TestClient(app)


def test_create_user(mock_user_repo: UserRepository):
    user_create = UserCreateSchemaFactory.build()
    mock_user_repo.find_by_email.return_value = None
    mock_user_repo.create.return_value = UserSchemaFactory.build()
    response = client.post(
        "/api/v1/users",
        json=user_create.dict()
    )
    assert response.status_code == status.HTTP_201_CREATED


def test_create_user_duplicate(mock_user_repo: UserRepository):
    user_create = UserCreateSchemaFactory.build()
    mock_user_repo.find_by_email.return_value = user_create
    response = client.post(
        "/api/v1/users",
        json=user_create.dict()
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_get_users_all(mock_user_repo: UserRepository):
    users = [UserSchemaFactory.build() for x in range(3)]
    mock_user_repo.find_all.return_value = users
    response = client.get(
        "/api/v1/users"
    )
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 3


def test_get_users_by_agency(mock_user_repo: UserRepository):
    users = [UserSchemaFactory.build(agency_id=2) for x in range(5)]
    mock_user_repo.find_by_agency.return_value = users
    response = client.get(
        "/api/v1/users?agency_id=2"
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


def test_search_users(mock_user_repo: UserRepository):
    users = [UserSchemaFactory.build(name="test name") for x in range(2)]
    mock_user_repo.search_users.return_value = users
    response = client.get(
        "/api/v1/users/search-users/test"
    )
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 2
