from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.write_base_repository import BaseRepository
from app.core.write_db import get_db
from app.features.users.models import User


class UserRepository(BaseRepository[User]):
    def __init__(self, db: Session = Depends(get_db)):
        super().__init__(User, db)

    def get_user_by_username(self, username: str):
        return self.db.query(User).filter(User.username == username).first()
