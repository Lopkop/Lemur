from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, scoped_session, sessionmaker

from config import settings

engine = create_engine(settings.DATABASE_URL)

SessionLocal = scoped_session(sessionmaker(bind=engine))

Base = declarative_base()


def create_tables():
    Base.metadata.create_all(bind=engine)
