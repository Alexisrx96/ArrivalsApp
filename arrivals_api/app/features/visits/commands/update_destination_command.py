from typing import Optional
from mediatr import Mediator

from app.features.visits.models import Destination
from app.features.visits.read_repo import DestinationReadRepository
from app.features.visits.schemas import DestinationCreate, DestinationOut
from app.features.visits.write_repo import DestinationRepository


class UpdateDestinationCommand:
    def __init__(self, destination_id: int, destination: DestinationCreate):
        self.destination_id = destination_id
        self.destination = destination


@Mediator.handler
class UpdateDestinationCommandHandler:
    def __init__(self):
        self.destination_repository = DestinationRepository.instance()
        self.read_repository = DestinationReadRepository()

    async def handle(
        self, request: UpdateDestinationCommand
    ) -> Optional[Destination]:
        # Fetch the existing destination
        existing_destination = self.destination_repository.get(
            request.destination_id
        )
        if not existing_destination:
            return None

        # Update fields
        existing_destination.name = request.destination.name
        existing_destination.location = request.destination.location

        # Persist changes
        self.destination_repository.update(existing_destination)

        # Update read repository
        self.read_repository.update_one(
            {"id": request.destination_id},
            DestinationOut.model_validate(existing_destination).model_dump(),
        )
        return existing_destination
