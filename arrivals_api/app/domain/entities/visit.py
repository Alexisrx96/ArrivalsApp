from datetime import datetime


class Visit:
    def __init__(
        self,
        id: int,
        visitor: str,
        visit_type: str,
        destination: str,
        entry_time: datetime,
        exit_time: datetime = None,
    ):
        self.id = id
        self.visitor = visitor
        self.visit_type = visit_type
        self.destination = destination
        self.entry_time = entry_time
        self.exit_time = exit_time

    def __str__(self):
        return f"Visit(id={self.id}, visitor={self.visitor}, entry_time={self.entry_time}, destination={self.destination})"


class VisitType:
    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name

    def __str__(self):
        return f"VisitType(id={self.id}, name={self.name})"


class Destination:
    def __init__(self, id: int, name: str, location: str):
        self.id = id
        self.name = name
        self.location = location

    def __str__(self):
        return f"Destination(id={self.id}, name={self.name}, location={self.location})"
