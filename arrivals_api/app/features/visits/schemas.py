from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, model_validator


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

    @model_validator(mode="after")
    def validate_exit_time(self):
        entry_time = self.entry_time
        exit_time = self.exit_time

        if exit_time and exit_time < entry_time:
            raise ValueError("exit_time must be after entry_time")

        return self


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

    @model_validator(mode="after")
    def validate_dates(self):
        start_date = self.start_date
        end_date = self.end_date

        if start_date and end_date and start_date > end_date:
            raise ValueError("start_date must be before end_date")

        return self


# Threshold Schema
class Threshold(BaseModel, PaginationParams):
    low: float
    high: float
