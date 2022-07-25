from src.models import User


class MockDataBase:
    """Mock DB for testing purpose"""

    def __init__(self):
        self.user_saved = False
        self.users = {}

    def save_user(self, user: User):
        """Saves user to storage"""
        self.users[user.user_id] = user
        self.user_saved = True
