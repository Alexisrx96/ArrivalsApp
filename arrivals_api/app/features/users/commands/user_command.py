from mediatr import Mediator

from app.features.users.auth import hash_password
from app.features.users.exceptions import (
    UserAlreadyExistsException,
    UserNotFoundException,
)
from app.features.users.schemas import UserCreate, UserOut
from app.features.users.write_repo import UserRepository
from app.features.users.models import User as UserModel
from app.features.users.read_repo import UserReadRepository


class CreateUserCommand:
    def __init__(self, new_user: UserCreate):
        self.username = new_user.username
        self.email = new_user.email
        self.full_name = new_user.full_name
        self.password = new_user.password


@Mediator.handler
class CreateUserCommandHandler:
    def __init__(self):
        self.repo = UserRepository.instance()
        self.read_repo = UserReadRepository()

    async def handle(self, command: CreateUserCommand) -> UserModel:
        if self.repo.get_user_by_username(command.username):
            raise UserAlreadyExistsException(
                message="Username already registered"
            )

        # Hash password and create user
        hashed_password = hash_password(command.password)
        new_user = UserModel(
            username=command.username,
            email=command.email,
            full_name=command.full_name,
            hashed_password=hashed_password,
        )

        # Persist to write database and replicate to read database
        new_user = self.repo.create(new_user)
        self.read_repo.insert_one(vars(new_user))

        return new_user


class UpdateUserCommand:
    def __init__(self, username: str, updates: dict):
        self.username = username
        self.updates = updates


@Mediator.handler
class UpdateUserCommandHandler:
    def __init__(self):
        self.repo = UserRepository.instance()
        self.read_repo = UserReadRepository()

    async def handle(self, command: UpdateUserCommand) -> UserModel:
        # Fetch existing user by username
        existing_user = self.repo.get_user_by_username(command.username)
        if not existing_user:
            raise UserNotFoundException()

        # Update user fields
        for key, value in command.updates.items():
            if key == "password":
                value = hash_password(value)
                setattr(existing_user, "hashed_password", value)
                continue
            if hasattr(existing_user, key):
                setattr(existing_user, key, value)
            else:
                raise ValueError(f"Invalid field: {key}")

        updated_user = self.repo.update(existing_user)

        self.read_repo.update_one(
            {"username": command.username},
            UserOut.model_validate(updated_user).model_dump(),
        )
        return updated_user


class DeleteUserCommand:
    def __init__(self, username: str):
        self.username = username


@Mediator.handler
class DeleteUserCommandHandler:
    def __init__(self):
        self.repo = UserRepository.instance()
        self.read_repo = UserReadRepository()

    async def handle(self, command: DeleteUserCommand) -> None:
        # Fetch existing user by username
        existing_user = self.repo.get_user_by_username(command.username)
        if not existing_user:
            raise UserNotFoundException()

        # Delete user from write and read databases
        self.repo.delete(existing_user.id)
        self.read_repo.delete_one({"username": command.username})
