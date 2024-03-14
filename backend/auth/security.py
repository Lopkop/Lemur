from datetime import datetime

from passlib.context import CryptContext
from jose import JWTError, jwt

from config import settings
from db.dbapi import DatabaseService
from auth.exceptions import LoginFailed, UserExpired

db = DatabaseService()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def authenticate_user(session, name: str, password: str):
    user = db.fetch_user_by_name(session, name)
    if not (user and verify_password(password, user.hashed_password)):
        raise LoginFailed("Either username or password is incorrect")
    return user


def token_expired_check(session, username):
    user = db.fetch_user_by_name(session, username)
    access_token = db.fetch_token_by_username(session, username)
    if (access_token.expires_at - datetime.now()).total_seconds() < 0:
        db.remove_user(session, user)
        raise UserExpired("Token has expired")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def hash_password(password):
    return pwd_context.hash(password)


def create_access_token(data: dict):
    encoded_jwt = jwt.encode(data, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str):
    decoded = jwt.decode(token, key=settings.SECRET_KEY, algorithms=settings.ALGORITHM)
    return decoded
