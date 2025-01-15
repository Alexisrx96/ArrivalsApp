from app.core.exceptions import (
    ArrivalHTTPException,
    BadRequestException,
    NotFoundException,
)


class InvalidCredentialsException(ArrivalHTTPException):
    def __init__(self, message="Incorrect username or password"):
        super().__init__(message, status_code=401)


class UserNotFoundException(NotFoundException):
    def __init__(self, message="User not found."):
        super().__init__(message)


class UserAlreadyExistsException(BadRequestException):
    def __init__(self, message="User already exists."):
        super().__init__(message)
