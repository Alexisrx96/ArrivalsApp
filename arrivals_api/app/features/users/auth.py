from datetime import datetime, timedelta, timezone
from typing import Optional

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


class AuthService:

    def __init__(self):
        self._secret_key = settings.secret_key
        self._algorithm = settings.algorithm
        self._access_token_expire_minutes = (
            settings.access_token_expire_minutes
        )

    def verify_password(
        self, plain_password: str, hashed_password: str
    ) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    def create_access_token(self, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + (
            timedelta(minutes=self._access_token_expire_minutes)
        )
        to_encode.update({"exp": expire})
        return jwt.encode(
            to_encode, self._secret_key, algorithm=self._algorithm
        )

    def verify_access_token(self, token) -> Optional[dict]:
        if not token:
            return None
        try:
            payload = jwt.decode(
                token,
                self._secret_key,
                algorithms=[self._algorithm],
            )
            return payload
        except JWTError:
            return None
