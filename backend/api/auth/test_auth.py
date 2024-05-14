import json

import pytest
from fastapi import Depends
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


@pytest.mark.parametrize('user,status',
                         [
                             ({'name': 'new_user', 'password': 'test', 'lifetime': 1}, 200),
                             ({'name': 'existing_user', 'password': 'test', 'lifetime': 2}, 401),
                             ({'name': 'bad_user', 'password': 'test'}, 422),
                         ])
def test_sign_up(fill_db, user: dict, status: int):
    req = client.post('/api/sign-up', content=json.dumps(user))
    assert req.status_code == status


@pytest.mark.parametrize('user,status',
                         [
                             ({'name': 'new_user', 'password': 'test', 'lifetime': 1}, 401),
                             ({'name': 'existing_user', 'password': 'wrong_password', 'lifetime': 2}, 401),
                             ({'name': 'existing_user', 'password': 'test', 'lifetime': 2}, 200),
                             ({'name': 'bad_user', 'pass': 'test'}, 422),
                         ])
def test_log_in(db_connection, fill_db, user: dict, status: int):
    token_model = db_connection[1].fetch_token_by_username(next(db_connection[1].get_db())
                                                     , user.get('name'))
    client.cookies = {'access_token': token_model and token_model.token}
    req = client.post('/api/login', content=json.dumps(user))
    assert req.status_code == status
