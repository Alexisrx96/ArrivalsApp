from pydantic import BaseModel
from datetime import datetime
from typing import Optional


# VisitType Schemas
class VisitTypeCreate(BaseModel):
    name: str


class VisitTypeOut(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


# Destination Schemas
class DestinationCreate(BaseModel):
    name: str
    location: str


class DestinationOut(BaseModel):
    id: int
    name: str
    location: str

    class Config:
        from_attributes = True


# Visit Schemas
class VisitCreate(BaseModel):
    visitor: str
    visit_type_id: int
    destination_id: int
    entry_time: datetime
    exit_time: Optional[datetime] = None


class VisitOut(BaseModel):
    id: int
    visitor: str
    visit_type: VisitTypeOut
    destination: DestinationOut
    entry_time: datetime
    exit_time: Optional[datetime] = None

    class Config:
        from_attributes = True
