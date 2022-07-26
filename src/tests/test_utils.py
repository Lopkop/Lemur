from src.utils import create_user


json_signup_request = """
{
    "username": "funky_goblin",
    "user_id": "123415",
    "chatroom_id": "a-chatroom-id"
}
"""


def test_create_user_works_correctly():
    user = create_user(json_signup_request)

    assert user.user_id == 123415
    assert user.chatroom_id == "a-chatroom-id"
    assert user.username == "funky_goblin"
