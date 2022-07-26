from sqlalchemy import Column, DateTime, Integer, String, func
from sqlalchemy.orm import relationship

from ..session import Base
from .chat_room_model import ChatRoom


class User(Base):
    """User Table Definition"""

    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    chat_room_id = Column(String, unique=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), server_onupdate=func.now())

    children = relationship(ChatRoom)

    def __repr__(self):
        return "<User(name='{}', chat_room_id='{}')>".format(
            self.name, self.chat_room_id
        )
