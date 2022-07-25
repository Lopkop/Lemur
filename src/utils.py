import secrets


class RandomIdGenerator:
    """By calling generates random identifier"""
    def __init__(self):
        """Opens wordlists and store in memory"""
        with open('wordlists/nouns.txt') as nouns, open('wordlists/adjectives.txt') as adjectives:
            self._nouns = [noun.strip() for noun in nouns]
            self._adjectives = [adj.strip() for adj in adjectives]

    def __call__(self):
        """Generates a secure random identifier"""
        return f'{secrets.choice(self._adjectives)}-{secrets.choice(self._nouns)}-{secrets.choice(self._nouns)}'
