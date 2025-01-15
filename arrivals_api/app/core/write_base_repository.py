import re
from typing import Generic, List, Type, TypeVar

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.exceptions import BadRequestException
from app.core.write_db import get_db

T = TypeVar("T")


class BaseRepository(Generic[T]):
    _instance = None

    @classmethod
    def instance(cls):
        if cls._instance is None:
            db = next(get_db())
            cls._instance = cls(db)
        return cls._instance

    def __init__(self, model: Type[T], db: Session):
        self.model = model
        self.db = db

    def get(self, id: int) -> T:
        return self.db.query(self.model).get(id)

    def get_all(self) -> List[T]:
        return self.db.query(self.model).all()

    def create(self, obj: T) -> T:
        try:
            self.db.add(obj)
            self.db.commit()
            self.db.refresh(obj)
            return obj
        except IntegrityError as e:
            self.db.rollback()
            self.refresh_db()
            raise BadRequestException(self._parse_integrity_error(e))

    def update(self, obj: T) -> T:
        try:
            self.db.merge(obj)
            self.db.commit()
            return obj
        except IntegrityError as e:
            self.db.rollback()
            self.refresh_db()
            raise BadRequestException(self._parse_integrity_error(e))

    def delete(self, id: int) -> None:
        obj = self.get(id)
        self.db.delete(obj)
        self.db.commit()

    def refresh_db(self):
        self.db = next(get_db())

    def _parse_integrity_error(self, error: IntegrityError) -> str:
        # Extract the original error message
        orig_msg = str(error.orig)
        err_msg = orig_msg.split(":")[-1].replace("\n", "").strip()

        if match := re.search(r"Key \((.*?)\)=\((.*?)\)", err_msg):
            column, value = match.groups()
            return (
                f"Duplicated value: '{value}' already exists in the '{column}'"
                " field. Please choose a different value."
            )
        else:
            return "An error occurred while processing your request."
