from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.write_base_repository import BaseRepository
from app.core.write_db import get_db
from app.features.visits.models import Destination, Visit, VisitType


class DestinationRepository(BaseRepository[Destination]):
    def __init__(self, db: Session = Depends(get_db)):
        super().__init__(Destination, db)


class VisitRepository(BaseRepository[Visit]):
    def __init__(self, db: Session = Depends(get_db)):
        super().__init__(Visit, db)


class VisitTypeRepository(BaseRepository[VisitType]):
    def __init__(self, db: Session = Depends(get_db)):
        super().__init__(VisitType, db)
