from datetime import datetime, timedelta, timezone
from typing import TYPE_CHECKING, Optional

from fastapi import Depends
from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings

if TYPE_CHECKING:
    from app.features.users.models import User

from fastapi import HTTPException, Request, status
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer

from app.features.users.write_repo import UserRepository

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


class AuthService:

    def __init__(self, user_repo: UserRepository = Depends(UserRepository)):
        self._user_repo = user_repo
        self._secret_key = settings.secret_key
        self._algorithm = settings.algorithm
        self._access_token_expire_minutes = (
            settings.access_token_expire_minutes
        )

    def verify_password(
        self, plain_password: str, hashed_password: str
    ) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    def authenticate_user(
        self, username: str, password: str
    ) -> Optional["User"]:
        """
        Validate the user credentials.
        Returns user data if valid, None otherwise.
        """
        user = self._user_repo.get_user_by_username(username)
        if user and self.verify_password(password, user.hashed_password):
            return user
        return None

    def create_access_token(self, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + (
            timedelta(minutes=self._access_token_expire_minutes)
        )
        to_encode.update({"exp": expire})
        return jwt.encode(
            to_encode, self._secret_key, algorithm=self._algorithm
        )

    def verify_access_token(self, token: str) -> Optional[dict]:
        try:
            payload = jwt.decode(
                token, self._secret_key, algorithms=[self._algorithm]
            )
            return payload
        except JWTError:
            return None
