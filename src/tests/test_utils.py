from src.utils import create_user

from .mocks.db import MockDataBase

json_signup_request = """
{
    "username": "funky_goblin",
    "user_id": "123415",
    "chatroom_id": "a-chatroom-id"
}
"""


def test_create_user():
    db = MockDataBase()
    create_user(json_signup_request, db)

    assert db.user_saved is True
    assert db.users.get(123415).user_id == 123415
    assert db.users.get(123415).username == 'funky_goblin'
    assert db.users.get(123415).chatroom_id == 'a-chatroom-id'
