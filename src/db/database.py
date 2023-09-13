from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, scoped_session, sessionmaker

from config import DATABASE_URL

engine = create_engine(DATABASE_URL)

SessionLocal = scoped_session(sessionmaker(bind=engine))

Base = declarative_base()
