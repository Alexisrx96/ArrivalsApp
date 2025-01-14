from mediatr import Mediator
from app.features.visits.schemas import VisitCreate
from app.features.visits.models import Visit
from app.features.visits.write_repo import (
    VisitRepository,
    VisitTypeRepository,
    DestinationRepository,
)
from app.features.visits.read_repo import (
    VisitReadRepository as VisitReadRepository,
)


class CreateVisitCommand:
    def __init__(self, visit: VisitCreate):
        self.visit = visit


@Mediator.handler
class CreateVisitCommandHandler:
    def __init__(self):
        self.visit_repository = VisitRepository.instance()
        self.visit_type_repository = VisitTypeRepository.instance()
        self.destination_repository = DestinationRepository.instance()
        self.visit_read_repository = VisitReadRepository()

    async def handle(self, request: CreateVisitCommand) -> Visit:
        visit = Visit(
            visitor=request.visit.visitor,
            visit_type_id=request.visit.visit_type_id,
            destination_id=request.visit.destination_id,
            entry_time=request.visit.entry_time,
            exit_time=request.visit.exit_time,
        )
        self.visit_repository.create(visit)

        visit_type = self.visit_type_repository.get(
            request.visit.visit_type_id
        )
        destination = self.destination_repository.get(
            request.visit.destination_id
        )

        document = {
            "id": visit.id,
            "visitor": visit.visitor,
            "visit_type": visit_type.__dict__ if visit_type else None,
            "destination": destination.__dict__ if destination else None,
            "entry_time": visit.entry_time.isoformat(),
            "exit_time": (
                visit.exit_time.isoformat() if visit.exit_time else None
            ),
        }

        self.visit_read_repository.insert_one(document)
        return visit
