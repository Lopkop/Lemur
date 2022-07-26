from nanoid import generate

from src.db.models.chat_room_model import ChatRoom
from src.db.models.user_model import User
from src.db.session import Base, Session, engine

Base.metadata.create_all(engine)


class UserFactory:
    """User Factory Class is used to create user"""

    def create_user(self, name: str):
        """Create a user

        Creates a user and assigns a unique 5 letter chatroom id he can use

        :param name: Name of User
        :return:
            User object of User model

        """
        user_obj = User(name=name, chat_room_id=generate(size=5))
        Session.add(user_obj)
        Session.commit()
        return user_obj

    def fetch_user_by_name(self, name):
        """Get User by name

        Fetch user object by querying on name
        :param name:
        :return:
        """
        return Session.query(User).filter_by(name=name).first()


class ChatRoomFactory:
    """ChatRoom Factory to create messages"""

    def create_messaage(self, chatroom_id: str, user_id: int, message: str):
        """
        Create a message in chatroom

        :param chatroom_id: chatroom id
        :param user_id: user id; primary key of user table
        :param message: message the user sends
        :return:
            ChatRoom Object
        """
        chat_room_obj = ChatRoom(
            chat_room_id=chatroom_id, user_id=user_id, message=message
        )
        Session.add(chat_room_obj)
        Session.commit()
        return chat_room_obj

    def get_chat_room_messages(self, chatroom_id: str, page: int = 1, size: int = 20):
        """
            Fetch all messages in a chat room

        :param chatroom_id:
        :param page:
        :param size:
        :return:
        """
        page = page - 1
        offset = page * size
        return (
            Session.query(ChatRoom)
            .filter_by(chat_room_id=chatroom_id)
            .limit(size)
            .offset(offset)
            .all()
        )
