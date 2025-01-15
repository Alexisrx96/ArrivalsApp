from typing import Optional

from pydantic import BaseModel, EmailStr, Field, model_validator


class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8)
    confirm_password: str = Field(..., min_length=8)
    full_name: str = Field(..., max_length=100)

    @model_validator(mode="after")
    def check_passwords_match(self):
        if self.password != self.confirm_password:
            raise ValueError("Passwords do not match")
        return self

    class Config:
        json_schema_extra = {
            "example": {
                "username": "john_doe",
                "email": "john.doe@example.com",
                "password": "securepassword123",
                "confirm_password": "securepassword123",
                "full_name": "John Doe",
            }
        }


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=8)
    confirm_password: Optional[str] = Field(None, min_length=8)
    full_name: Optional[str] = Field(None, max_length=100)

    @model_validator(mode="after")
    def check_passwords_match(self):
        if not self.password:
            return self
        if self.password != self.confirm_password:
            raise ValueError("Passwords do not match")
        return self

    class Config:
        json_schema_extra = {
            "example": {
                "email": "updated_email@example.com",
                "password": "newsecurepassword123",
                "confirm_password": "newsecurepassword123",
                "full_name": "Johnathan Doe",
            }
        }


class UserOut(BaseModel):
    id: int
    username: str
    email: str
    full_name: str

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "username": "john_doe",
                "email": "john.doe@example.com",
                "full_name": "John Doe",
            }
        }


class UserLogin(BaseModel):
    username: str
    password: str

    class Config:
        json_schema_extra = {
            "example": {
                "username": "john_doe",
                "password": "$ecurePassword123",
            }
        }
