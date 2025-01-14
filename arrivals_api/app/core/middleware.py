from fastapi import Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer
from starlette.middleware.base import BaseHTTPMiddleware

from app.features.users.auth import AuthService

# OAuth2PasswordBearer is used to specify the token URL for OAuth2 authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


class AuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, auth_service: AuthService = Depends(AuthService)):
        super().__init__(app)
        self.auth_service = auth_service

    async def dispatch(self, request: Request, call_next):
        # Exclude specific route (e.g., "/login" or "/token")
        if request.url.path in ["/login", "/docs", "/openapi.json", "/users/"]:
            return await call_next(request)

        # Extract the token from the Authorization header
        token = request.headers.get("Authorization")
        if not token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authorization token is missing",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Remove "Bearer " from the token
        token = token.split(" ")[1] if token.startswith("Bearer ") else token

        # Verify the token
        payload = self.auth_service.verify_access_token(token)
        if payload is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Attach the user to the request context (e.g., as a custom attribute)
        user_id = payload.get("sub")
        user = await self.auth_service._user_repo.get_user_by_id(user_id)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Add the user object to the request state (or context)
        request.state.user = user

        # Proceed with the request
        response = await call_next(request)
        return response
