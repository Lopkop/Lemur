from datetime import datetime

from passlib.context import CryptContext
from jose import jwt
from sqlalchemy.orm import scoped_session
from fastapi import HTTPException, status
from cryptography.fernet import Fernet

from config import settings
from db.dbapi import DatabaseService
from api.auth.exceptions import LoginFailed, UserExpired

db = DatabaseService()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
fernet = Fernet(key=settings.ENCRYPTION_KEY)


def verify_user(session: scoped_session, token: str):
    username = decode_access_token(token)['name']
    user = db.fetch_user_by_name(session, username)
    if user.lifetime <= datetime.now() or token_expired(session, username):
        db.remove_user(session, username)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Your account was deleted",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


def authenticate_user(session: scoped_session, name: str, password: str):
    user = db.fetch_user_by_name(session, name)
    if not (user and verify_password(password, user.hashed_password)):
        raise LoginFailed("Either username or password is incorrect")
    if token_expired(session, user.name):
        db.remove_user(session, user.name)
        raise UserExpired("Your account was deleted")
    return user


def token_expired(session, username):
    access_token = db.fetch_token_by_username(session, username)
    if access_token.expires_at <= datetime.now():
        return True
    return False


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def hash_password(password):
    return pwd_context.hash(password)


def create_access_token(data: dict):
    encoded_jwt = jwt.encode(data, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str):
    decoded_jwt = jwt.decode(token, key=settings.SECRET_KEY, algorithms=settings.ALGORITHM)
    return decoded_jwt
