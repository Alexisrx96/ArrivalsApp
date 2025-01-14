from pydantic import BaseModel, Field
from datetime import date, datetime
from typing import Optional


class PaginationParams:
    page: int = Field(
        1, ge=1, description="Page number for pagination (1-based)"
    )
    page_size: int = Field(
        10, ge=1, le=100, description="Number of results per page"
    )


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


class VisitQueryParams(BaseModel, PaginationParams):

    visitor: Optional[str] = Field(None, description="Filter by visitor name")
    visit_type_id: Optional[int] = Field(
        None, description="Filter by visit type ID"
    )
    destination_id: Optional[int] = Field(
        None, description="Filter by destination ID"
    )
    start_date: Optional[datetime] = Field(
        None, description="Filter visits starting from this date (entry_time)"
    )
    end_date: Optional[datetime] = Field(
        None, description="Filter visits up to this date (entry_time)"
    )


class Threshold(BaseModel, PaginationParams):
    low: float
    high: float
