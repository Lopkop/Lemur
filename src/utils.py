import secrets


def generate_random_id() -> str:
    """Generates a secure random identifier"""
    with open('wordlists/nouns.txt') as nouns, open('wordlists/adjectives.txt') as adjectives:
        nouns = [noun.strip() for noun in nouns]
        adjectives = [adj.strip() for adj in adjectives]
        return f'{secrets.choice(adjectives)}-{secrets.choice(nouns)}-{secrets.choice(nouns)}'
