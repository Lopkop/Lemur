import secrets

from pydantic import ValidationError

from src.db.schemas import ChatRoomModel, MessageModel, UserModel


class RandomIdGenerator:
    """Secure random id generator"""

    def __init__(self):
        """Opens wordlists and store in memory"""
        with open("wordlists/nouns.txt") as nouns, open(
            "wordlists/adjectives.txt"
        ) as adjectives:
            self._nouns = [noun.strip() for noun in nouns]
            self._adjectives = [adj.strip() for adj in adjectives]

    def _generate_user_id(self):
        """Generates random user id"""
        return f"{secrets.choice(self._nouns)}#{''.join([f'{secrets.randbelow(10)}' for _ in range(4)])}"

    def _generate_message_id(self):
        return "".join([f"{secrets.randbelow(10)}" for _ in range(4)])

    def __call__(self, user_id=False, message_id=False):
        """Generates a secure random identifier"""
        if user_id:
            return self._generate_user_id()
        elif message_id:
            return self._generate_message_id()
        return f"{secrets.choice(self._adjectives)}-{secrets.choice(self._nouns)}-{secrets.choice(self._nouns)}"


# Models API
def create_and_get_user(username: str) -> UserModel:
    """Creates User object from returns it"""
    try:
        user = UserModel(name=username)
    except ValidationError as e:
        # todo: we can parse(e.json()) and return readable exception to the user
        print(e.json())
    else:
        return user


def create_and_get_message(username: str, text: str) -> MessageModel:
    """Creates Message object and returns it"""
    try:
        message = MessageModel(user=username, text=text)
    except ValidationError as e:
        print(e.json())
    else:
        return message


def create_and_get_chatroom(user: UserModel, name: str) -> ChatRoomModel:
    """Creates Chatroom object and returns it"""
    try:
        chatroom = ChatRoomModel(users=[user], name=name, messages=[])
    except ValidationError as e:
        print(e.json())
    else:
        return chatroom
