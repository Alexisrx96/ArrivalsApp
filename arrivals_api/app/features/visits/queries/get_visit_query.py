from datetime import date
from mediatr import Mediator
from typing import Dict, List, Optional
from app.features.visits.read_repo import VisitReadRepository
from app.features.visits.schemas import Threshold, VisitOut


class GetVisitQuery:
    def __init__(
        self,
        filters: Optional[dict] = None,
        page: int = 1,
        page_size: int = 10,
    ):
        self.filters = filters or {}
        self.page = page
        self.page_size = page_size


@Mediator.handler
class GetVisitQueryHandler:
    def __init__(self):
        self.visit_read_repository = VisitReadRepository()

    async def handle(self, request: GetVisitQuery) -> List[VisitOut]:

        # Calculate pagination parameters
        skip = (request.page - 1) * request.page_size
        limit = request.page_size

        # Fetch visits from the repository
        return self.visit_read_repository.filter(
            filters=request.filters, limit=limit, skip=skip
        )


# get_processing_time_by_visit_type
class GetProcessingTimeByVisitTypeQuery:
    pass


@Mediator.handler
class GetProcessingTimeByVisitTypeQueryHandler:
    def __init__(self):
        self.visit_read_repository = VisitReadRepository()

    async def handle(self, request: GetProcessingTimeByVisitTypeQuery):
        return self.visit_read_repository.get_processing_time_by_visit_type()


# get_processing_time_by_destination
class GetProcessingTimeByDestinationQuery:
    pass


@Mediator.handler
class GetProcessingTimeByDestinationQueryHandler:
    def __init__(self):
        self.visit_read_repository = VisitReadRepository()

    async def handle(self, request: GetProcessingTimeByDestinationQuery):
        return self.visit_read_repository.get_processing_time_by_destination()


# get_unusual_processing_times
class GetUnusualProcessingTimesQuery:
    def __init__(self, threshold: Threshold):
        self.min_threshold = threshold.low
        self.max_threshold = threshold.high
        self.page = threshold.page or 1
        self.page_size = threshold.page_size or 10


@Mediator.handler
class GetUnusualProcessingTimesQueryHandler:
    def __init__(self):
        self.visit_read_repository = VisitReadRepository()

    async def handle(self, request: GetUnusualProcessingTimesQuery):
        return self.visit_read_repository.get_unusual_processing_times(
            request.min_threshold,
            request.max_threshold,
            request.page,
            request.page_size,
        )
