from src.schemas import UserModel
from src.sockets.response_factory import ResponseFactory

test_data = {
    "new_user": UserModel(
        name="funky_goblin", user_id="a-user-id", chatroom_id="a-chatroom-id"
    )
}


def test_sign_up_response():
    user = test_data["new_user"]
    response = ResponseFactory.generate_sign_up_response(status=True, user_model=user)

    expected_response = {
        "status": True,
        "user": {
            "chatroom_id": "a-chatroom-id",
            "name": "funky_goblin",
            "user_id": "a-user-id",
        },
    }

    assert response == expected_response
