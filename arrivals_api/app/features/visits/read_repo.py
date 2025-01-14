from typing import Dict, List, Union
from app.core.read_base_repository import ReadRepository, handle_errors
from app.features.visits.schemas import (
    DestinationOut,
    VisitOut,
    VisitTypeOut,
)


class VisitReadRepository(ReadRepository):
    def __init__(self):
        super().__init__("visits", VisitOut)

    @handle_errors
    def get_processing_time_by_visit_type(
        self,
    ) -> List[Dict[str, Union[str, float, int]]]:
        """
        Calculate processing time statistics (average, min, max) grouped by visit type.

        Returns:
            List[Dict[str, Union[str, float, int]]]: List of processing time stats per visit type.
        """
        pipeline = [
            {
                "$addFields": {
                    "processing_time_minutes": {
                        "$divide": [
                            {"$subtract": ["$exit_time", "$entry_time"]},
                            60000,  # Convert milliseconds to minutes
                        ]
                    }
                }
            },  # Calculate processing time in minutes
            {
                "$group": {
                    "_id": "$visit_type.name",  # Group by visit type
                    "avg_processing_time": {
                        "$avg": "$processing_time_minutes"
                    },
                    "min_processing_time": {
                        "$min": "$processing_time_minutes"
                    },
                    "max_processing_time": {
                        "$max": "$processing_time_minutes"
                    },
                    "total_visits": {"$sum": 1},
                }
            },
            {
                "$project": {
                    "visit_type": "$_id",
                    "_id": 0,  # Exclude the `_id` field
                    "avg_processing_time": 1,
                    "min_processing_time": 1,
                    "max_processing_time": 1,
                    "total_visits": 1,
                }
            },
            {
                "$sort": {"avg_processing_time": -1}
            },  # Sort by average processing time descending
        ]
        result = list(self.collection.aggregate(pipeline))
        return result

    @handle_errors
    def get_processing_time_by_destination(
        self,
    ) -> List[Dict[str, Union[str, float, int]]]:
        """
        Calculate processing time statistics (average, min, max) grouped by destination.

        Returns:
            List[Dict[str, Union[str, float, int]]]: List of processing time stats per destination.
        """
        pipeline = [
            {
                "$addFields": {
                    "processing_time_minutes": {
                        "$divide": [
                            {"$subtract": ["$exit_time", "$entry_time"]},
                            60000,  # Convert milliseconds to minutes
                        ]
                    }
                }
            },  # Calculate processing time in minutes
            {
                "$group": {
                    "_id": "$destination.name",  # Group by destination
                    "avg_processing_time": {
                        "$avg": "$processing_time_minutes"
                    },
                    "min_processing_time": {
                        "$min": "$processing_time_minutes"
                    },
                    "max_processing_time": {
                        "$max": "$processing_time_minutes"
                    },
                    "total_visits": {"$sum": 1},
                }
            },
            {
                "$project": {
                    "destination": "$_id",
                    "_id": 0,  # Exclude the `_id` field
                    "avg_processing_time": 1,
                    "min_processing_time": 1,
                    "max_processing_time": 1,
                    "total_visits": 1,
                }
            },
            {
                "$sort": {"avg_processing_time": -1}
            },  # Sort by average processing time descending
        ]
        result = list(self.collection.aggregate(pipeline))
        return result

    @handle_errors
    def get_unusual_processing_times(
        self,
        min_threshold: float,
        max_threshold: float,
        page: int = 1,
        page_size: int = 10,
    ) -> List[Dict[str, Union[str, float, int]]]:
        """
        Find visits with unusually short or long processing times.

        Args:
            min_threshold (float): Minimum processing time in minutes.
            max_threshold (float): Maximum processing time in minutes.
            page (int): Page number for pagination (default is 1).
            page_size (int): Number of results per page (default is 10).

        Returns:
            List[Dict[str, Union[str, float, int]]]: List of unusual processing times.
        """
        # Calculate the number of documents to skip based on the page number and page size
        skip = (page - 1) * page_size

        pipeline = [
            {
                "$addFields": {
                    "processing_time_minutes": {
                        "$divide": [
                            {"$subtract": ["$exit_time", "$entry_time"]},
                            60000,  # Convert milliseconds to minutes
                        ]
                    }
                }
            },  # Calculate processing time in minutes
            {
                "$match": {
                    "$or": [
                        {"processing_time_minutes": {"$lt": min_threshold}},
                        {"processing_time_minutes": {"$gt": max_threshold}},
                    ]
                }
            },  # Filter for unusual processing times
            {
                "$project": {
                    "_id": 0,  # Exclude the MongoDB _id field
                    "id": 1,  # Include the custom id field
                    "visitor": 1,
                    "visit_type": "$visit_type.name",
                    "destination": "$destination.name",
                    "processing_time_minutes": 1,
                    "entry_time": 1,
                    "exit_time": 1,
                }
            },
            {"$skip": skip},  # Skip documents based on page number
            {"$limit": page_size},  # Limit the number of documents per page
        ]

        result = list(self.collection.aggregate(pipeline))
        return result


class VisitTypeReadRepository(ReadRepository):
    def __init__(self):
        super().__init__("visit_types", VisitTypeOut)


class DestinationReadRepository(ReadRepository):
    def __init__(self):
        super().__init__("destinations", DestinationOut)
