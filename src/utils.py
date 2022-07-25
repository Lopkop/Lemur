import secrets

from pydantic import ValidationError

from .models import User


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


def create_user(json_request: str, db_connection) -> None:
    """Creates User object from model class and saves in db"""
    try:
        user = User.parse_raw(json_request)
    except ValidationError as e:
        # todo: we can parse(e.json()) and return readable exception to the user
        print(e.json())
    else:
        db_connection.save_user(user)
