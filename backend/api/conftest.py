from datetime import datetime, timedelta

import pytest
from sqlalchemy_utils import create_database, drop_database
from sqlalchemy import create_engine


@pytest.fixture
def postgres():
    from config import settings
    from db.database import _create_tables

    settings.DATABASE_URL = "postgresql://postgres:admin@localhost:5433/lemur-test"
    create_database(settings.DATABASE_URL)
    _create_tables()
    yield settings.DATABASE_URL
    drop_database(settings.DATABASE_URL)


@pytest.fixture
def db_connection(postgres):
    engine = create_engine(postgres)
    conn = engine.connect()
    try:
        yield conn
    finally:
        conn.close()
        engine.dispose()


@pytest.fixture
def fill_db(db_connection):
    db_connection.execute(
        "INSERT INTO users (name,hashed_password,lifetime) "
        f"VALUES ('existing_user', 'test', '{datetime.now() + timedelta(minutes=30)}')"
    )
