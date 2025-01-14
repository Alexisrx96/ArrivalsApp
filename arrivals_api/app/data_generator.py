import asyncio
import os
from concurrent.futures import ProcessPoolExecutor
from datetime import timedelta
from typing import List, Optional

from faker import Faker
from mediatr import Mediator

from app.features.visits.commands.create_destination_command import (
    CreateDestinationCommand,
    DestinationCreate,
)
from app.features.visits.commands.create_visit_command import (
    CreateVisitCommand,
    VisitCreate,
)
from app.features.visits.commands.create_visit_type_command import (
    CreateVisitTypeCommand,
    VisitTypeCreate,
)
from app.core.config import settings

faker = Faker()


# Helper function to generate a single VisitCreate record
def generate_visit_record(
    visit_type_count: int, destination_count: int
) -> dict:
    entry_time = faker.date_time_this_year()
    exit_time = entry_time + timedelta(hours=faker.random_int(min=1, max=8))

    return {
        "visitor": faker.name(),
        "visit_type_id": faker.random_int(min=1, max=visit_type_count),
        "destination_id": faker.random_int(min=1, max=destination_count),
        "entry_time": entry_time,
        "exit_time": (
            exit_time if faker.boolean(chance_of_getting_true=80) else None
        ),  # 80% chance of having an exit time
    }


def generate_batch(
    batch_size: int, visit_type_count: int, destination_count: int
):
    return [
        generate_visit_record(visit_type_count, destination_count)
        for _ in range(batch_size)
    ]


async def generate_visits_parallel(
    total_records: int,
    batch_size: int,
    visit_type_count: int,
    destination_count: int,
    callback: Optional[callable] = None,
):
    """
    Generate VisitCreate records in parallel.
    :param total_records: Total number of records to generate.
    :param batch_size: Number of records to generate per batch.
    :param visit_type_count: Total number of visit types available.
    :param destination_count: Total number of destinations available.
    """
    num_workers = os.cpu_count() or 4  # Use the number of available CPU cores
    total_batches = (total_records + batch_size - 1) // batch_size

    print(
        f"Generating {total_records} records in "
        f"parallel using {num_workers} workers..."
    )
    with ProcessPoolExecutor(max_workers=num_workers) as executor:
        futures = [
            executor.submit(
                generate_batch, batch_size, visit_type_count, destination_count
            )
            for _ in range(total_batches)
        ]
        for i, future in enumerate(futures, start=1):
            # Here you can send the data to the database or mediator
            batch = future.result()
            if callback:
                await callback(batch)
            print(
                f"Processed batch {i} of {total_batches} "
                f"with {len(batch)} records."
            )


async def initialize_data(
    *,
    create_visits: bool = True,
    create_destinations: bool = True,
    create_visit_types: bool = True,
):

    mediator = Mediator()
    if create_visit_types:
        # Create Visit Types
        visit_type_tasks = [
            mediator.send_async(CreateVisitTypeCommand(VisitTypeCreate(**v)))
            for v in [
                {"name": "Customer"},
                {"name": "Supplier"},
                {"name": "Employee"},
                {"name": "Contractor"},
                {"name": "Other"},
            ]
        ]

    else:
        visit_type_tasks = []

    if create_destinations:
        # Create Destinations
        destination_tasks = [
            mediator.send_async(
                CreateDestinationCommand(DestinationCreate(**d))
            )
            for d in [
                {"name": "Management", "location": "First Floor, Room 101"},
                {"name": "Marketing", "location": "First Floor, Room 102"},
                {"name": "Sales", "location": "Second Floor, Room 201"},
                {"name": "Engineering", "location": "Second Floor, Room 202"},
                {"name": "IT", "location": "Third Floor, Room 301"},
                {"name": "Legal", "location": "Third Floor, Room 302"},
                {"name": "HR", "location": "Fourth Floor, Room 401"},
                {"name": "Finance", "location": "Fifth Floor, Room 501"},
            ]
        ]

    else:
        destination_tasks = []

    total_records = settings.total_records
    batch_size = settings.batch_size
    visit_type_count = len(visit_type_tasks) if visit_type_tasks else 5
    destination_count = len(destination_tasks) if destination_tasks else 8

    # Combine all tasks
    all_tasks = visit_type_tasks + destination_tasks
    await asyncio.gather(*all_tasks)

    if not create_visits:
        return

    # Create Visits
    async def _create_visit(visits: List[dict]):
        await asyncio.gather(
            *[
                mediator.send_async(CreateVisitCommand(VisitCreate(**v)))
                for v in visits
            ]
        )

    await generate_visits_parallel(
        total_records,
        batch_size,
        visit_type_count,
        destination_count,
        _create_visit,
    )
