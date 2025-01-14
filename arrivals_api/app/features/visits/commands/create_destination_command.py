from mediatr import Mediator

from app.features.visits.models import Destination
from app.features.visits.read_repo import DestinationReadRepository
from app.features.visits.schemas import DestinationCreate
from app.features.visits.write_repo import DestinationRepository


class CreateDestinationCommand:
    def __init__(self, destination: DestinationCreate):
        self.destination = destination


@Mediator.handler
class CreateDestinationCommandHandler:
    def __init__(self):
        self.destination_repository = DestinationRepository.instance()
        self.read_repository = DestinationReadRepository()

    async def handle(self, request: CreateDestinationCommand) -> Destination:
        destination = Destination(
            name=request.destination.name,
            location=request.destination.location,
        )
        self.destination_repository.create(destination)

        self.read_repository.insert_one(destination.__dict__)
        return destination
