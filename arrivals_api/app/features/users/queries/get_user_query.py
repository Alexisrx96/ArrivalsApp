from typing import List, Optional

from mediatr import Mediator

from app.features.users.exceptions import UserNotFoundException
from app.features.users.read_repo import UserReadRepository
from app.features.users.schemas import UserOut


# Query object to encapsulate request data for fetching users
class GetUserQuery:
    def __init__(
        self,
        filters: Optional[dict] = None,
        page: int = 1,
        page_size: int = 10,
    ):
        self.filters = filters or {}
        self.page = page
        self.page_size = page_size


# Query handler to process the GetUserQuery
@Mediator.handler
class GetUserQueryHandler:
    def __init__(self):
        self.user_read_repository = UserReadRepository()

    async def handle(self, request: GetUserQuery) -> List[UserOut]:
        # Calculate pagination parameters
        skip = (request.page - 1) * request.page_size
        limit = request.page_size

        # Fetch users from the repository
        return self.user_read_repository.filter(
            filters=request.filters, limit=limit, skip=skip
        )


# Query object to encapsulate request data for fetching a user by username
class GetUserByUsernameQuery:
    def __init__(self, username: str):
        self.username = username


# Query handler to process the GetUserByUsernameQuery
@Mediator.handler
class GetUserByUsernameQueryHandler:
    def __init__(self):
        self.user_read_repository = UserReadRepository()

    async def handle(
        self, request: GetUserByUsernameQuery
    ) -> Optional[UserOut]:
        user = self.user_read_repository.get_user_by_username(request.username)
        if not user:
            raise UserNotFoundException()
        return user
