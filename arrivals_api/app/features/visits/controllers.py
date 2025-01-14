from typing import Dict, List, Union

from fastapi import APIRouter, Depends, HTTPException
from mediatr import Mediator

from app.features.visits.commands.create_visit_command import (
    CreateVisitCommand,
)
from app.features.visits.commands.create_visit_type_command import (
    CreateVisitTypeCommand,
)
from app.features.visits.models import Destination
from app.features.visits.queries.get_visit_querie import (
    GetProcessingTimeByDestinationQuery,
    GetProcessingTimeByVisitTypeQuery,
    GetUnusualProcessingTimesQuery,
    GetVisitQuery,
)
from app.features.visits.schemas import (
    DestinationCreate,
    DestinationOut,
    Threshold,
    VisitCreate,
    VisitOut,
    VisitQueryParams,
    VisitTypeCreate,
    VisitTypeOut,
)
from app.features.visits.write_repo import (
    DestinationRepository,
    VisitRepository,
    VisitTypeRepository,
)


# Controller
class ReportController:
    def __init__(
        self,
        mediator: Mediator,
    ):
        self.mediator = mediator
        self.router = APIRouter()
        self._set_routes()

    def _set_routes(self):
        self.router.get("/processing-time-by-visit-type")(
            self.get_processing_time_by_visit_type
        )
        self.router.get("/processing-time-by-destination")(
            self.get_processing_time_by_destination
        )
        self.router.get("/unusual-processing-times")(
            self.get_unusual_processing_times
        )

    async def get_processing_time_by_visit_type(self):
        return await self.mediator.send_async(
            GetProcessingTimeByVisitTypeQuery()
        )

    async def get_processing_time_by_destination(self):
        return await self.mediator.send_async(
            GetProcessingTimeByDestinationQuery()
        )

    async def get_unusual_processing_times(
        self, threshold: Threshold = Depends()
    ):
        return await self.mediator.send_async(
            GetUnusualProcessingTimesQuery(threshold)
        )


class VisitController:
    def __init__(
        self,
        mediator: Mediator,
    ):
        self.mediator = mediator
        self.router = APIRouter()
        self._set_routes()

    def _set_routes(self):
        self.router.post("/", response_model=VisitOut, status_code=201)(
            self.create_visit
        )
        self.router.get("/", response_model=List[VisitOut])(self.list_visits)
        self.router.get("/{visit_id}", response_model=VisitOut)(self.get_visit)
        self.router.put("/{visit_id}", response_model=VisitOut)(
            self.update_visit
        )
        self.router.delete("/{visit_id}", status_code=204)(self.delete_visit)

    async def create_visit(
        self,
        visit: VisitCreate,
    ) -> VisitOut:
        return await self.mediator.send_async(CreateVisitCommand(visit))

    async def list_visits(
        self,
        query_params: VisitQueryParams = Depends(),
    ) -> List[VisitOut]:
        # Build filters dictionary based on query parameters
        filters = {}
        if query_params.visitor:
            filters["visitor"] = query_params.visitor
        if query_params.visit_type_id:
            filters["visit_type.id"] = query_params.visit_type_id
        if query_params.destination_id:
            filters["destination.id"] = query_params.destination_id
        if query_params.start_date:
            filters["entry_time"] = {"$gte": query_params.start_date}
        if query_params.end_date:
            filters["entry_time"] = filters.get("entry_time", {})
            filters["entry_time"]["$lte"] = query_params.end_date

        # Create the Mediator query
        query = GetVisitQuery(
            filters=filters,
            page=query_params.page,
            page_size=query_params.page_size,
        )

        # Execute the query using Mediator
        return await self.mediator.send_async(query)

    async def get_visit(
        self,
        visit_id: int,
        repo: VisitRepository = Depends(VisitRepository),
    ):
        visit = repo.get(visit_id)
        if not visit:
            raise HTTPException(status_code=404, detail="Visit not found")
        return visit

    async def update_visit(
        self,
        visit_id: int,
        visit: VisitCreate,
        repo: VisitRepository = Depends(VisitRepository),
    ):
        existing_visit = repo.get(visit_id)
        if not existing_visit:
            raise HTTPException(status_code=404, detail="Visit not found")
        updated_visit = repo.update(visit_id, visit.model_dump())
        return updated_visit

    async def delete_visit(
        self,
        visit_id: int,
        repo: VisitRepository = Depends(VisitRepository),
    ):
        existing_visit = repo.get(visit_id)
        if not existing_visit:
            raise HTTPException(status_code=404, detail="Visit not found")
        repo.delete(visit_id)


class VisitTypeController:
    def __init__(
        self,
        mediator: Mediator,
    ):
        self.mediator = mediator
        self.router = APIRouter()
        self._set_routes()

    def _set_routes(self):
        self.router.post("/", response_model=VisitTypeOut, status_code=201)(
            self.create_visit_type
        )
        self.router.get("/", response_model=List[VisitTypeOut])(
            self.list_visit_types
        )
        self.router.get("/{visit_type_id}", response_model=VisitTypeOut)(
            self.get_visit_type
        )
        self.router.put("/{visit_type_id}", response_model=VisitTypeOut)(
            self.update_visit_type
        )
        self.router.delete("/{visit_type_id}", status_code=204)(
            self.delete_visit_type
        )

    async def create_visit_type(self, visit_type: VisitTypeCreate):
        return await self.mediator.send_async(
            CreateVisitTypeCommand(visit_type)
        )

    async def list_visit_types(
        self,
        repo: VisitTypeRepository = Depends(VisitTypeRepository),
    ):
        visit_types = repo.get_all()
        return visit_types

    async def get_visit_type(
        self,
        visit_type_id: int,
        repo: VisitTypeRepository = Depends(VisitTypeRepository),
    ):
        visit_type = repo.get(visit_type_id)
        if not visit_type:
            raise HTTPException(status_code=404, detail="Visit type not found")
        return visit_type

    async def update_visit_type(
        self,
        visit_type_id: int,
        visit_type: VisitTypeCreate,
        repo: VisitTypeRepository = Depends(VisitTypeRepository),
    ):
        existing_visit_type = repo.get(visit_type_id)
        if not existing_visit_type:
            raise HTTPException(status_code=404, detail="Visit type not found")
        updated_visit_type = repo.update(
            existing_visit_type, visit_type.dict()
        )
        return updated_visit_type

    async def delete_visit_type(
        self,
        visit_type_id: int,
        repo: VisitTypeRepository = Depends(VisitTypeRepository),
    ):
        visit_type = repo.get(visit_type_id)
        if not visit_type:
            raise HTTPException(status_code=404, detail="Visit type not found")
        repo.delete(visit_type_id)


class DestinationController:
    def __init__(
        self,
        mediator: Mediator,
    ):
        self.mediator = mediator
        self.router = APIRouter()
        self._set_routes()

    def _set_routes(self):
        self.router.post("/", response_model=DestinationOut, status_code=201)(
            self.create_destination
        )
        self.router.get("/", response_model=List[DestinationOut])(
            self.list_destinations
        )
        self.router.get("/{destination_id}", response_model=DestinationOut)(
            self.get_destination
        )
        self.router.put("/{destination_id}", response_model=DestinationOut)(
            self.update_destination
        )
        self.router.delete("/{destination_id}", status_code=204)(
            self.delete_destination
        )

    async def create_destination(
        self,
        destination: DestinationCreate,
        repo: DestinationRepository = Depends(DestinationRepository),
    ):
        new_destination = repo.create(Destination(**destination.model_dump()))
        return new_destination

    async def list_destinations(
        self,
        repo: DestinationRepository = Depends(DestinationRepository),
    ):
        destinations = repo.get_all()
        return destinations

    async def get_destination(
        self,
        destination_id: int,
        repo: DestinationRepository = Depends(DestinationRepository),
    ):
        destination = repo.get(destination_id)
        if not destination:
            raise HTTPException(
                status_code=404, detail="Destination not found"
            )
        return destination

    async def update_destination(
        self,
        destination_id: int,
        destination: DestinationCreate,
        repo: DestinationRepository = Depends(DestinationRepository),
    ):
        existing_destination = repo.get(destination_id)
        if not existing_destination:
            raise HTTPException(
                status_code=404, detail="Destination not found"
            )
        updated_destination = repo.update(
            existing_destination, destination.dict()
        )
        return updated_destination

    async def delete_destination(
        self,
        destination_id: int,
        repo: DestinationRepository = Depends(DestinationRepository),
    ):
        destination = repo.get(destination_id)
        if not destination:
            raise HTTPException(
                status_code=404, detail="Destination not found"
            )
        repo.delete(destination_id)
