from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from app.features.users.auth import AuthService, hash_password
from app.features.users.models import User as UserModel
from app.features.users.read_repo import MongoUser
from app.features.users.schemas import UserCreate, UserLogin, UserOut
from app.features.users.write_repo import UserRepository

user_router = APIRouter()

auth_router = APIRouter()


@user_router.post("/", response_model=UserOut)
def create_user(
    user: UserCreate,
    repo: UserRepository = Depends(UserRepository),
    mongo: MongoUser = Depends(MongoUser),
):
    db_user = repo.get_user_by_username(user.username)
    if db_user:
        raise HTTPException(
            status_code=400, detail="Username already registered"
        )

    hashed_password = hash_password(user.password)
    new_user = UserModel(
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        hashed_password=hashed_password,
    )

    new_user = repo.create(new_user)
    mongo.insert_one(new_user.__dict__)

    return new_user


@user_router.get("/{username}", response_model=UserOut)
def get_user(
    username: str,
    repo: UserRepository = Depends(UserRepository),
):
    db_user = repo.get_user_by_username(username)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@auth_router.post("/login")
def login(
    user: OAuth2PasswordRequestForm = Depends(),
    auth_service: AuthService = Depends(AuthService),
):
    db_user = auth_service.authenticate_user(user.username, user.password)

    if not db_user:
        raise HTTPException(
            status_code=401, detail="Incorrect username or password"
        )

    return auth_service.create_access_token(
        {
            "username": db_user.username,
            "email": db_user.email,
            "full_name": db_user.full_name,
        }
    )
