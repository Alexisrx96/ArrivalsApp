from functools import wraps
import logging
from typing import (
    Any,
    Callable,
    Generic,
    List,
    Mapping,
    Optional,
    Type,
    TypeVar,
    Union,
)

from pydantic import BaseModel, ValidationError
from pymongo.collection import Collection
from pymongo.errors import PyMongoError
from pymongo.results import DeleteResult, UpdateResult

from app.core.read_db import connect_to_mongo, mongodb

# Set up logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

# Define a generic type for Pydantic models
T = TypeVar("T", bound=BaseModel)


def handle_errors(func: Callable):
    """
    Decorator to handle PyMongo errors and log exceptions.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except PyMongoError as e:
            logger.error(f"MongoDB error in {func.__name__}: {e}")
            raise e
        except ValidationError as ve:
            logger.error(f"Validation error in {func.__name__}: {ve}")
            raise ve

    return wrapper


class ReadRepository(Generic[T]):
    def __init__(self, collection_name: str, model: Type[T]):
        # Ensure the database connection is established
        if mongodb.database is None:
            connect_to_mongo()
        self.collection: Collection = mongodb.database[collection_name]
        self.model = model

    @handle_errors
    def get_by_id(self, _id: Union[int, str]) -> Optional[T]:
        """
        Retrieve a document by its ID.
        """
        document = self.collection.find_one({"_id": _id})
        return self.model(**document) if document else None

    @handle_errors
    def get_all(self) -> List[T]:
        """
        Retrieve all documents in the collection.
        """
        documents = self.collection.find()
        return [self.model(**doc) for doc in documents]

    @handle_errors
    def find_by_field(self, field: str, value: Union[str, int]) -> Optional[T]:
        """
        Retrieve a document by a specific field and value.
        """
        document = self.collection.find_one({field: value})
        return self.model(**document) if document else None

    @handle_errors
    def insert_one(self, data: dict) -> bool:
        """
        Insert a single document into the collection.
        """
        validated_data = self.model(**data)  # Validate against the schema
        self.collection.replace_one(
            {"_id": validated_data.id},
            validated_data.model_dump(),
            upsert=True,
        )
        return True

    @handle_errors
    def update_one(self, filters: Mapping[str, Any], data: dict) -> bool:
        """
        Update a single document in the collection.
        """
        validated_data = self.model(**data, partial=True)
        update_result: UpdateResult = self.collection.update_one(
            filters,
            {"$set": validated_data.model_dump()},
        )
        return update_result.modified_count > 0

    @handle_errors
    def delete_one(self, filters: Mapping[str, Any]) -> bool:
        """
        Delete a document by its ID.
        """
        result: DeleteResult = self.collection.delete_one(filters)
        return result.deleted_count > 0

    @handle_errors
    def filter(self, filters: dict, limit: int = 10, skip: int = 0) -> List[T]:
        """
        Filter documents based on dynamic filters.
        """
        documents = self.collection.find(filters).skip(skip).limit(limit)
        return [self.model(**doc) for doc in documents]
