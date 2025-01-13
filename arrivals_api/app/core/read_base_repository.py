from typing import Generic, List, Optional, Type, TypeVar, Union

from pydantic import BaseModel, ValidationError
from pymongo.collection import Collection
from pymongo.errors import PyMongoError

from app.core.read_db import connect_to_mongo, mongodb

# Define a generic type for Pydantic models
T = TypeVar("T", bound=BaseModel)


class ReadRepository(Generic[T]):
    def __init__(self, collection_name: str, model: Type[T]):
        # Ensure the database connection is established
        if not mongodb.database:
            connect_to_mongo()
        self.collection: Collection = mongodb.database[collection_name]
        self.model = model

    def get_by_id(self, id: Union[int, str]) -> Optional[T]:
        """
        Retrieve a document by its ID.
        """
        try:
            document = self.collection.find_one({"_id": id})
            if document:
                return self.model(**document)
            return None
        except PyMongoError as e:
            print(f"Error retrieving document by ID: {e}")
            return None

    def get_all(self) -> List[T]:
        """
        Retrieve all documents in the collection.
        """
        try:
            documents = self.collection.find()
            return [self.model(**doc) for doc in documents]
        except PyMongoError as e:
            print(f"Error retrieving all documents: {e}")
            return []

    def find_by_field(self, field: str, value: Union[str, int]) -> Optional[T]:
        """
        Retrieve a document by a specific field and value.
        """
        try:
            document = self.collection.find_one({field: value})
            if document:
                return self.model(**document)
            return None
        except PyMongoError as e:
            print(f"Error retrieving document by {field}: {e}")
            return None

    def insert_one(self, data: dict) -> bool:
        """
        Insert a single document into the collection.
        """
        try:
            validated_data = self.model(**data)  # Validate against the schema
            self.collection.insert_one(validated_data.model_dump())
            return True
        except ValidationError as ve:
            print(f"Validation error: {ve}")
            return False
        except PyMongoError as e:
            print(f"Error inserting document: {e}")
            return False

    def delete_by_id(self, id: Union[int, str]) -> bool:
        """
        Delete a document by its ID.
        """
        try:
            result = self.collection.delete_one({"_id": id})
            return result.deleted_count > 0
        except PyMongoError as e:
            print(f"Error deleting document by ID: {e}")
            return False
