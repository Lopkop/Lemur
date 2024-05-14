from datetime import datetime, timedelta

import pytest
from sqlalchemy_utils import create_database, drop_database
from sqlalchemy import create_engine

from db.dbapi import DatabaseService


@pytest.fixture(scope='module')
def postgres():
    from config import settings
    from db.database import _create_tables

    settings.DATABASE_URL = "postgresql://postgres:admin@localhost:5433/lemur-test"
    create_database(settings.DATABASE_URL)
    _create_tables()
    yield settings.DATABASE_URL
    drop_database(settings.DATABASE_URL)


@pytest.fixture(scope='module')
def db_connection(postgres):
    engine = create_engine(postgres,
                           pool_size=10,
                           max_overflow=2,
                           pool_recycle=300,
                           pool_pre_ping=True,
                           pool_use_lifo=True
                           )
    conn = engine.connect()
    db = DatabaseService()
    try:
        yield conn, db
    finally:
        conn.close()
        engine.dispose()


@pytest.fixture(scope='module')
def fill_db(db_connection):
    db_connection[0].execute(
        "INSERT INTO users (name,hashed_password,lifetime) "
        f"VALUES ('existing_user', '$2b$12$NlmobQnJ0.EMzOfJ9dZXfuj5lCl4RUuQdkC3MLAKPT/MRV2xJ2Qvi', "
        f"'{datetime.now() + timedelta(minutes=30)}')"
    )

    db_connection[0].execute(f"""INSERT INTO tokens (token,expires_at,"user")
                             VALUES ('eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.
                             eyJuYW1lIjoiZXhpc3RpbmdfdXNlciJ9.
                             9rgns-G5cW9RnadTqfxnmc8he3oGK7ytrsEkXRIAutU',
                             '{datetime.now() + timedelta(minutes=30)}','existing_user')""")

    db_connection[0].execute(
        "INSERT INTO users (name,hashed_password,lifetime) "
        f"VALUES ('user_expired_token', '$2b$12$NlmobQnJ0.EMzOfJ9dZXfuj5lCl4RUuQdkC3MLAKPT/MRV2xJ2Qvi', "
        f"'{datetime.now() + timedelta(minutes=30)}')"
    )

    db_connection[0].execute(f"""INSERT INTO tokens (token,expires_at,"user")
                             VALUES ('eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.
                             eyJuYW1lIjoidXNlcl9leHBpcmVkX3Rva2VuIn0.
                             Fw-nuhxlknSHUc59C1665Z9Wg93kER-06kE45IWasTk',
                             '{datetime.now() - timedelta(minutes=30)}','user_expired_token')""")
