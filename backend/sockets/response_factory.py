from db.schemas import (
    ChatRoomModel,
    GetMessagesResponseModel,
    MessageModel,
    SendMessageResponseModel,
    SignUpResponseModel,
    UserModel,
    UserUndefinedModel,
    ChatResponseModel,
)


class ResponseFactory:
    @staticmethod
    def generate_sign_up_response(status: int, access_token: str) -> SignUpResponseModel:
        """Generates sign up response in JSON"""
        response_model = SignUpResponseModel(status=status, access_token=access_token)
        return response_model

    @staticmethod
    def generate_send_message_response(status: bool, message: MessageModel) -> SendMessageResponseModel:
        """Generates send_message response in JSON"""
        response_model = SendMessageResponseModel(status=status, message=message)
        return response_model

    @staticmethod
    def generate_get_messages_response(status: bool, chatroom: ChatRoomModel) -> GetMessagesResponseModel:
        """Generates get_messages response in JSON"""
        response_model = GetMessagesResponseModel(
            **chatroom.dict(exclude={"users"}), status=status
        )
        return response_model

    @staticmethod
    def generate_chat_response(status: int, chatroom: ChatRoomModel):
        response_model = ChatResponseModel(**chatroom.dict(), status=status)
        return response_model

    @staticmethod
    def generate_user_undefined_error_response(username: str) -> UserUndefinedModel:
        return UserUndefinedModel(name=username, status=401)
