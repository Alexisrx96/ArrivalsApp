# flake8: noqa: F401
from passlib.context import CryptContext
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, declarative_base, sessionmaker

from app.core.config import settings

SQLALCHEMY_DATABASE_URL = settings.write_db_url

engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_size=20, max_overflow=10)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base: DeclarativeBase = declarative_base()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def init_db():

    from app.features.users.models import User
    from app.features.visits.models import Destination, Visit, VisitType
    from app.features.visits.write_repo import (
        DestinationRepository,
        VisitTypeRepository,
    )

    # Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
