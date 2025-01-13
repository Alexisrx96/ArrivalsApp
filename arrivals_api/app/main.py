from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.write_db import init_db
from app.features.users.api import auth_router, user_router


@asynccontextmanager
async def lifespan(*args, **kwargs):
    init_db()
    yield


app = FastAPI(lifespan=lifespan)


app.include_router(user_router, prefix="/users", tags=["users"])
app.include_router(auth_router, tags=["auth"])

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
