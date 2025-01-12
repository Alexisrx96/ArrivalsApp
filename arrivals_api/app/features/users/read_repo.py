from typing import Optional

from pymongo.errors import PyMongoError

from app.core.read_base_repository import ReadRepository
from app.features.users.schemas import UserOut


class MongoUser(ReadRepository[UserOut]):
    def __init__(self):
        super().__init__("users", UserOut)

    def get_user_by_username(self, username: str) -> Optional[UserOut]:
        try:
            user_data = self.collection.find_one({"username": username})
            if user_data:
                return UserOut(**user_data)
            return None
        except PyMongoError as e:
            print(f"Error finding user by username: {e}")
            return None
