from functools import wraps

from fastapi import Depends, Request, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.exceptions import InvalidTokenException
from app.features.users.auth import AuthService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


class Token(BaseModel):
    access_token: str
    token_type: str


def exception_handler(f):
    @wraps(f)
    async def wrapper(*args, **kwargs):
        try:
            return await f(*args, **kwargs)
        except InvalidTokenException as e:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"message": e.message},
                headers={"WWW-Authenticate": "Bearer"},
            )
        except Exception as e:
            raise e

    return wrapper


class AuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, auth_service: AuthService = Depends(AuthService)):
        super().__init__(app)
        self.auth_service = auth_service

    @exception_handler
    async def dispatch(self, request: Request, call_next):
        # Exclude specific route (e.g., "/login" or "/token")
        if request.url.path in ["/login", "/docs", "/openapi.json", "/users/"]:
            return await call_next(request)

        # Extract the token from the Authorization header
        token = request.headers.get("Authorization")
        if not token:
            raise InvalidTokenException("Authorization token is missing")

        # Remove "Bearer " from the token
        token = token.split(" ")[1] if token.startswith("Bearer ") else token

        # Verify the token
        payload = self.auth_service.verify_access_token(token)
        if payload is None:
            raise InvalidTokenException()

        # Proceed with the request
        return await call_next(request)
