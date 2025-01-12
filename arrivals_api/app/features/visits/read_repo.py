from app.features.visits.schemas import VisitOut, VisitTypeOut, DestinationOut
from app.core.read_base_repository import ReadRepository


class VisitRepository(ReadRepository):
    def __init__(self):
        super().__init__("visits", VisitOut)


class VisitTypeRepository(ReadRepository):
    def __init__(self):
        super().__init__("visit_types", VisitTypeOut)


class DestinationRepository(ReadRepository):
    def __init__(self):
        super().__init__("destinations", DestinationOut)
