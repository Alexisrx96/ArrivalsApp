from fastapi import APIRouter, Depends, HTTPException
from typing import List

from app.features.visits.schemas import (
    VisitCreate,
    VisitOut,
    VisitTypeCreate,
    VisitTypeOut,
    DestinationCreate,
    DestinationOut,
)
from app.features.visits.write_repo import (
    VisitRepository,
    VisitTypeRepository,
    DestinationRepository,
)

# Routers
visit_router = APIRouter(prefix="/visits", tags=["Visits"])
visit_type_router = APIRouter(prefix="/visit-types", tags=["Visit Types"])
destination_router = APIRouter(prefix="/destinations", tags=["Destinations"])


# Visit Endpoints
@visit_router.post("/", response_model=VisitOut, status_code=201)
async def create_visit(
    visit: VisitCreate,
    repo: VisitRepository = Depends(VisitRepository),
):
    new_visit = repo.create(visit)
    return new_visit


@visit_router.get("/", response_model=List[VisitOut])
async def list_visits(
    repo: VisitRepository = Depends(VisitRepository),
):
    visits = repo.get_all()
    return visits


@visit_router.get("/{visit_id}", response_model=VisitOut)
async def get_visit(
    visit_id: int,
    repo: VisitRepository = Depends(VisitRepository),
):
    visit = repo.get(visit_id)
    if not visit:
        raise HTTPException(status_code=404, detail="Visit not found")
    return visit


@visit_router.put("/{visit_id}", response_model=VisitOut)
async def update_visit(
    visit_id: int,
    visit: VisitCreate,
    repo: VisitRepository = Depends(VisitRepository),
):
    existing_visit = repo.get(visit_id)
    if not existing_visit:
        raise HTTPException(status_code=404, detail="Visit not found")
    updated_visit = repo.update(existing_visit, visit.dict())
    return updated_visit


@visit_router.delete("/{visit_id}", status_code=204)
async def delete_visit(
    visit_id: int,
    repo: VisitRepository = Depends(VisitRepository),
):
    visit = repo.get(visit_id)
    if not visit:
        raise HTTPException(status_code=404, detail="Visit not found")
    repo.delete(visit_id)


# VisitType Endpoints
@visit_type_router.post("/", response_model=VisitTypeOut, status_code=201)
async def create_visit_type(
    visit_type: VisitTypeCreate,
    repo: VisitTypeRepository = Depends(VisitTypeRepository),
):
    new_visit_type = repo.create(visit_type)
    return new_visit_type


@visit_type_router.get("/", response_model=List[VisitTypeOut])
async def list_visit_types(
    repo: VisitTypeRepository = Depends(VisitTypeRepository),
):
    visit_types = repo.get_all()
    return visit_types


@visit_type_router.get("/{visit_type_id}", response_model=VisitTypeOut)
async def get_visit_type(
    visit_type_id: int,
    repo: VisitTypeRepository = Depends(VisitTypeRepository),
):
    visit_type = repo.get(visit_type_id)
    if not visit_type:
        raise HTTPException(status_code=404, detail="Visit type not found")
    return visit_type


@visit_type_router.put("/{visit_type_id}", response_model=VisitTypeOut)
async def update_visit_type(
    visit_type_id: int,
    visit_type: VisitTypeCreate,
    repo: VisitTypeRepository = Depends(VisitTypeRepository),
):
    existing_visit_type = repo.get(visit_type_id)
    if not existing_visit_type:
        raise HTTPException(status_code=404, detail="Visit type not found")
    updated_visit_type = repo.update(existing_visit_type, visit_type.dict())
    return updated_visit_type


@visit_type_router.delete("/{visit_type_id}", status_code=204)
async def delete_visit_type(
    visit_type_id: int,
    repo: VisitTypeRepository = Depends(VisitTypeRepository),
):
    visit_type = repo.get(visit_type_id)
    if not visit_type:
        raise HTTPException(status_code=404, detail="Visit type not found")
    repo.delete(visit_type_id)


# Destination Endpoints
@destination_router.post("/", response_model=DestinationOut, status_code=201)
async def create_destination(
    destination: DestinationCreate,
    repo: DestinationRepository = Depends(DestinationRepository),
):
    new_destination = repo.create(destination)
    return new_destination


@destination_router.get("/", response_model=List[DestinationOut])
async def list_destinations(
    repo: DestinationRepository = Depends(DestinationRepository),
):
    destinations = repo.get_all()
    return destinations


@destination_router.get("/{destination_id}", response_model=DestinationOut)
async def get_destination(
    destination_id: int,
    repo: DestinationRepository = Depends(DestinationRepository),
):
    destination = repo.get(destination_id)
    if not destination:
        raise HTTPException(status_code=404, detail="Destination not found")
    return destination


@destination_router.put("/{destination_id}", response_model=DestinationOut)
async def update_destination(
    destination_id: int,
    destination: DestinationCreate,
    repo: DestinationRepository = Depends(DestinationRepository),
):
    existing_destination = repo.get(destination_id)
    if not existing_destination:
        raise HTTPException(status_code=404, detail="Destination not found")
    updated_destination = repo.update(existing_destination, destination.dict())
    return updated_destination


@destination_router.delete("/{destination_id}", status_code=204)
async def delete_destination(
    destination_id: int,
    repo: DestinationRepository = Depends(DestinationRepository),
):
    destination = repo.get(destination_id)
    if not destination:
        raise HTTPException(status_code=404, detail="Destination not found")
    repo.delete(destination_id)
