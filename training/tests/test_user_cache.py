import pytest
import json
from unittest import mock
from training.data.user_cache import UserCache, redis
from training.schemas import TempUser


@pytest.fixture
def temp_user():
    return {"email": "test@example.com", "name": "Meg March", "agency_id": 3}


@pytest.fixture
def uuid():
    return 'da43a735-5905-4635-8a39-43555d4e2671'


def test_get_user(temp_user, uuid):
    '''It gets a user from redis given a key'''
    with mock.patch.object(redis, 'get') as RedisMock:
        RedisMock.return_value = json.dumps(temp_user)
        u = UserCache()
        found_user = u.get(uuid)
        redis.get.assert_called_with(uuid)
        assert found_user == TempUser(**temp_user)


def test_get_non_user(uuid):
    '''It returns None when the user is not found'''
    with mock.patch.object(redis, 'get') as RedisMock:
        RedisMock.return_value = None
        u = UserCache()
        found_user = u.get(uuid)
        redis.get.assert_called_with(uuid)
        assert found_user is None


@mock.patch('training.data.user_cache.redis')
@mock.patch('training.data.user_cache.uuid4')
def test_set_user(uuid_mock, redis_mock, uuid, temp_user):
    '''It sets redis key and generates a UUID for the user'''
    uuid_mock.return_value = uuid
    new_user = TempUser(**temp_user)
    u = UserCache()
    new_id = u.set(new_user)
    redis_mock.set.assert_called_with(uuid, json.dumps(temp_user))
    redis_mock.expire.assert_called()
    assert new_id == uuid


@mock.patch('training.data.user_cache.redis')
def test_delete_user(redis_mock, uuid):
    '''It calls redis delete'''
    u = UserCache()
    u.delete(uuid)
    redis_mock.delete.assert_called_with(uuid)
