from sqlalchemy import Column, DateTime, ForeignKeyConstraint, Integer, String, func
from sqlalchemy.orm import relationship

from ..session import Base
from .messages_model import Message


class ChatRoom(Base):
    """Message Table Definition"""

    __tablename__ = "chatrooms"
    id = Column(Integer, primary_key=True)
    chat_room_id = Column(String, unique=True)
    user_one = Column(String)
    user_two = Column(String)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), server_onupdate=func.now())
    children = relationship(Message)
    __table_args__ = (
        ForeignKeyConstraint([user_one, user_two], ["users.user_id", "users.user_id"]),
        {},
    )

    def __repr__(self):
        return "<ChatRoom(chat_room_id='{}', message='{}')>".format(
            self.chat_room_id, self.message
        )
