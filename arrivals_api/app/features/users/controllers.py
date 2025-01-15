from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from mediatr import Mediator

from app.core.secure import Token
from app.features.users.commands.user_command import (
    CreateUserCommand,
    DeleteUserCommand,
    UpdateUserCommand,
)
from app.features.users.commands.login_command import LoginCommand
from app.features.users.queries.get_user_query import (
    GetUserByUsernameQuery,
    GetUserQuery,
)
from app.features.users.schemas import UserCreate, UserOut, UserUpdate

from app.core.secure import oauth2_scheme


class AuthController:
    def __init__(self, mediator: Mediator):
        self.mediator = mediator
        self.router = APIRouter()
        self._set_routes()

    def _set_routes(self):
        self.router.post("/login")(self.login)

    async def login(
        self,
        user: OAuth2PasswordRequestForm = Depends(),
    ) -> Token:
        """
        Authenticate a user and return an access token.
        """

        return await self.mediator.send_async(
            LoginCommand(user.username, user.password)
        )


class UserController:
    def __init__(self, mediator: Mediator):
        self.mediator = mediator
        self.router = APIRouter()
        self._set_routes()

    def _set_routes(self):
        self.router.post("/", response_model=UserOut, status_code=201)(
            self.create_user
        )
        self.router.get("/", response_model=list[UserOut])(self.get_users)
        self.router.get("/{username}", response_model=UserOut)(
            self.get_user_by_username
        )
        self.router.put("/{username}", response_model=UserOut)(
            self.update_user
        )
        self.router.delete("/{username}", status_code=204)(self.delete_user)

    async def create_user(
        self,
        user: UserCreate,
    ) -> UserOut:
        """Create a new user."""
        return await self.mediator.send_async(CreateUserCommand(user))

    async def get_user_by_username(
        self,
        username: str,
        token: str = Depends(oauth2_scheme),
    ) -> UserOut:
        """Retrieve a user by username."""
        return await self.mediator.send_async(GetUserByUsernameQuery(username))

    async def get_users(self) -> list[UserOut]:
        """Retrieve a list of all users."""
        return await self.mediator.send_async(GetUserQuery())

    async def update_user(
        self,
        username: str,
        user_update: UserUpdate,
        token: str = Depends(oauth2_scheme),
    ) -> UserOut:
        """Update user details using their username."""
        if (
            user_update.password
            and user_update.password != user_update.confirm_password
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Passwords do not match.",
            )

        try:
            return await self.mediator.send_async(
                UpdateUserCommand(
                    username,
                    user_update.model_dump(
                        exclude_unset=True,
                        exclude=["confirm_password"],
                    ),
                )
            )
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
            )

    async def delete_user(
        self,
        username: str,
        token: str = Depends(oauth2_scheme),
    ) -> None:
        """Delete a user by their username."""
        await self.mediator.send_async(DeleteUserCommand(username))
