import src.db.models.messages_model  # noqa: F401
import src.db.models.user_model  # noqa: F401
from src.db.session import Base, engine

Base.metadata.create_all(engine)
print("Finished seeding database")
