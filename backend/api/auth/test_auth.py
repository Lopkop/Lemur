import json

import pytest
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


@pytest.mark.parametrize(
    "user,status",
    [
        ({"name": "new_user", "password": "test", "lifetime": 1}, 200),
        ({"name": "existing_user", "password": "test", "lifetime": 2}, 401),
        ({"name": "bad_user", "password": "test"}, 422),
    ],
)
def test_sign_up(fill_db, user: dict, status: int):
    res = client.post("/api/sign-up", content=json.dumps(user))
    assert res.status_code == status


@pytest.mark.parametrize(
    "user,status",
    [
        ({"name": "undefined_user", "password": "test", "lifetime": 1}, 401),
        ({"name": "existing_user", "password": "wrong_password", "lifetime": 2}, 401),
        ({"name": "existing_user", "password": "test", "lifetime": 2}, 200),
        ({"name": "bad_user", "pass": "test"}, 422),
    ],
)
def test_log_in(db_connection, fill_db, user: dict, status: int):
    token_model = db_connection[1].fetch_token_by_username(
        next(db_connection[1].get_db()), user.get("name")
    )
    client.cookies = {"access_token": token_model and token_model.token}
    res = client.post("/api/login", content=json.dumps(user))
    assert res.status_code == status


@pytest.mark.parametrize(
    "data,status",
    [
        (
            {
                "name": "existing_user",
            },
            401,
        ),
        (
            {
                "name": "user_expired_token",
                "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9."
                "eyJuYW1lIjoidXNlcl9leHBpcmVkX3Rva2VuIn0."
                "Fw-nuhxlknSHUc59C1665Z9Wg93kER-06kE45IWasTk",
            },
            401,
        ),
        ({"name": "existing_user", "token": ""}, 401),
        (
            {
                "name": "existing_user",
                "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9."
                "eyJuYW1lIjoiZXhpc3RpbmdfdXNlciJ9."
                "9rgns-G5cW9RnadTqfxnmc8he3oGK7ytrsEkXRIAutU",
            },
            200,
        ),
    ],
)
def test_get_user(fill_db, data, status):
    client.cookies = {"access_token": data.get("token")}
    res = client.get("/api/get_user")
    assert res.status_code == status
