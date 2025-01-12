from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.core.write_db import Base


class Visit(Base):
    __tablename__ = "visits"

    id = Column(Integer, primary_key=True, autoincrement=True)
    visitor = Column(String, nullable=False)
    visit_type_id = Column(
        Integer, ForeignKey("visit_types.id"), nullable=False
    )
    destination_id = Column(
        Integer, ForeignKey("destinations.id"), nullable=False
    )
    entry_time = Column(
        DateTime, nullable=False, default=lambda: datetime.now(timezone.utc)
    )
    exit_time = Column(DateTime, nullable=True)

    # Relationships
    visit_type = relationship("VisitType", back_populates="visits")
    destination = relationship("Destination", back_populates="visits")


class VisitType(Base):
    __tablename__ = "visit_types"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)

    # Relationships
    visits = relationship("Visit", back_populates="visit_type")


class Destination(Base):
    __tablename__ = "destinations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)
    location = Column(String, nullable=False)

    # Relationships
    visits = relationship("Visit", back_populates="destination")
