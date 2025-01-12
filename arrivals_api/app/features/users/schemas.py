from pydantic import BaseModel


class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    full_name: str


class UserOut(BaseModel):
    id: int
    username: str
    email: str
    full_name: str

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    username: str
    password: str
