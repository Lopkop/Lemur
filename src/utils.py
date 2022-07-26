import secrets
from typing import Union

from pydantic import ValidationError

from models import UserModel


class RandomIdGenerator:
    """By calling generates random identifier"""

    def __init__(self):
        """Opens wordlists and store in memory"""
        with open("wordlists/nouns.txt") as nouns, open(
                "wordlists/adjectives.txt"
        ) as adjectives:
            self._nouns = [noun.strip() for noun in nouns]
            self._adjectives = [adj.strip() for adj in adjectives]

    def __call__(self):
        """Generates a secure random identifier"""
        return f"{secrets.choice(self._adjectives)}-{secrets.choice(self._nouns)}-{secrets.choice(self._nouns)}"


def create_and_get_user(request: Union[str, dict]) -> UserModel:
    """Creates User object from json or dict and returns it"""
    try:
        if isinstance(request, str):
            user = UserModel.parse_raw(request)
        else:
            user = UserModel(**request)
    except ValidationError as e:
        # todo: we can parse(e.json()) and return readable exception to the user
        print(e.json())
    else:
        return user
