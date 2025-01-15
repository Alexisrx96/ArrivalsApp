from mediatr import Mediator
from app.core.secure import Token
from app.features.users.auth import AuthService
from app.features.users.exceptions import InvalidCredentialsException
from app.features.users.write_repo import UserRepository


class LoginCommand:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password


@Mediator.handler
class LoginCommandHandler:
    def __init__(self):
        self.repo = UserRepository.instance()
        self.auth_service = AuthService()

    async def handle(self, command: LoginCommand) -> dict:
        """
        Handle the login command by authenticating the user and generating an access token.
        """
        # Authenticate the user
        user = self.repo.get_user_by_username(
            command.username,
        )
        if not user or not self.auth_service.verify_password(
            command.password, user.hashed_password
        ):
            raise InvalidCredentialsException()
        # Generate and return the access token
        token = self.auth_service.create_access_token(
            {
                "username": user.username,
                "email": user.email,
                "full_name": user.full_name,
            }
        )
        return Token(access_token=token, token_type="bearer")
