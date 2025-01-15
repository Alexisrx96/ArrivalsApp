from fastapi import HTTPException


class ArrivalException(Exception):
    pass


class ArrivalHTTPException(ArrivalException):
    def __init__(self, message, status_code):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class NotFoundException(ArrivalHTTPException):
    def __init__(self, message, status_code=404):
        super().__init__(message, status_code)


class BadRequestException(ArrivalHTTPException):
    def __init__(self, message, status_code=400):
        super().__init__(message, status_code)


class InvalidTokenException(ArrivalException):
    def __init__(self, message="Invalid or expired token."):
        self.message = message
        super().__init__(self.message)
