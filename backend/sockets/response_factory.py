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
    def generate_sign_up_response(
        status: bool, user_model: UserModel
    ) -> SignUpResponseModel:
        """Generates sign up response in JSON"""
        response_model = SignUpResponseModel(status=status, user=user_model)
        return response_model

    @staticmethod
    def generate_send_message_response(
        status: bool, message: MessageModel
    ) -> SendMessageResponseModel:
        """Generates send_message response in JSON"""
        response_model = SendMessageResponseModel(status=status, message=message)
        return response_model

    @staticmethod
    def generate_get_messages_response(
        status: bool, chatroom: ChatRoomModel
    ) -> GetMessagesResponseModel:
        """Generates get_messages response in JSON"""
        response_model = GetMessagesResponseModel(
            **chatroom.dict(exclude={"users"}), status=status
        )
        return response_model

    @staticmethod
    def generate_chat_response(status: bool, chatroom: ChatRoomModel):
        response_model = ChatResponseModel(**chatroom.dict(), status=status)
        return response_model

    @staticmethod
    def generate_user_undefined_error_response(user: UserModel) -> UserUndefinedModel:
        return UserUndefinedModel(name=user.name, password=user.password, lifetime=user.lifetime, status=False)
