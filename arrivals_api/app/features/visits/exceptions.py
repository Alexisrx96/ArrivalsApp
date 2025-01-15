from app.core.exceptions import NotFoundException, BadRequestException


class VisitNotFoundException(NotFoundException):
    def __init__(self, message="Visit not found."):
        super().__init__(message)


class VisitTypeNotFoundException(NotFoundException):
    def __init__(self, message="Visit type not found."):
        super().__init__(message)


class VisitTypeAlreadyExistsException(BadRequestException):
    def __init__(self, message="Visit type already exists."):
        super().__init__(message)


class DestinationNotFoundException(NotFoundException):
    def __init__(self, message="Destination not found."):
        super().__init__(message)


class DestinationAlreadyExistsException(BadRequestException):
    def __init__(self, message="Destination already exists."):
        super().__init__(message)


class DestinationValidationException(BadRequestException):
    def __init__(self, message):
        super().__init__(message)
