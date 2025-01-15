from mediatr import Mediator

from app.features.visits.models import VisitType
from app.features.visits.read_repo import VisitTypeReadRepository
from app.features.visits.schemas import VisitTypeCreate
from app.features.visits.write_repo import VisitTypeRepository


class CreateVisitTypeCommand:
    def __init__(self, visit_type: VisitTypeCreate):
        self.visit_type = visit_type


@Mediator.handler
class CreateVisitTypeCommandHandler:
    def __init__(self):
        self.visit_type_repository = VisitTypeRepository.instance()
        self.read_repository = VisitTypeReadRepository()

    async def handle(self, request: CreateVisitTypeCommand) -> VisitType:
        print(request)
        visit_type = VisitType(name=request.visit_type.name)
        self.visit_type_repository.create(visit_type)

        self.read_repository.insert_one(vars(visit_type))
        return visit_type
