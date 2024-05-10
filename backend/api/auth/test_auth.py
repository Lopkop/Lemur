import json

import pytest
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
    assert 1 == 1
