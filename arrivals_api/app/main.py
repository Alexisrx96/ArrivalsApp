from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI
from mediatr import Mediator

from app.core.middleware import AuthMiddleware
from app.core.write_db import init_db
from app.data_generator import initialize_data
from app.features.users.api import auth_router, user_router
from app.features.users.auth import AuthService
from app.features.visits.controllers import (
    DestinationController,
    ReportController,
    VisitController,
    VisitTypeController,
)
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.core.config import settings

mediator = Mediator()


@asynccontextmanager
async def lifespan(*args, **kwargs):
    await init_db()
    yield


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

app = FastAPI(lifespan=lifespan)

if settings.enable_data_generation:

    class InitData:
        create_destination = False
        create_visit_types = False
        create_visits = True

    @app.post("/init-data", status_code=201, tags=["init-data"])
    async def init_data(
        init_data: InitData = Depends(),
    ):
        await initialize_data(
            create_destinations=init_data.create_destination,
            create_visit_types=init_data.create_visit_types,
            create_visits=init_data.create_visits,
        )


app.add_middleware(AuthMiddleware, auth_service=AuthService)

visit_controller = VisitController(mediator=mediator)
visit_type_controller = VisitTypeController(mediator=mediator)
destination_controller = DestinationController(mediator=mediator)
report_controller = ReportController(mediator=mediator)


app.include_router(auth_router, tags=["auth"])
app.include_router(
    report_controller.router, prefix="/reports", tags=["reports"]
)
app.include_router(user_router, prefix="/users", tags=["users"])
app.include_router(
    visit_type_controller.router,
    prefix="/visit-types",
    tags=["visit-types"],
)
app.include_router(
    visit_controller.router,
    prefix="/visits",
    tags=["visits"],
)

app.include_router(
    destination_controller.router,
    prefix="/destinations",
    tags=["destinations"],
)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
