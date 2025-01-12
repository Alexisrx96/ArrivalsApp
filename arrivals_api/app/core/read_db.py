from pymongo import MongoClient, errors
from app.core.config import settings


class MongoDB:
    def __init__(self):
        self.client: MongoClient = None
        self.database = None

    def connect(self):
        try:
            self.client = MongoClient(
                settings.read_db_url, serverSelectionTimeoutMS=5000
            )
            self.database = self.client[settings.read_db_name]
            # Trigger a server selection to verify the connection
            self.client.admin.command("ping")
            print("Connected to MongoDB")
        except errors.ServerSelectionTimeoutError as e:
            print(f"Failed to connect to MongoDB: {e}")
            self.client = None
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            self.client = None

    def close(self):
        if self.client:
            try:
                self.client.close()
                print("Disconnected from MongoDB")
            except Exception as e:
                print(f"Error while disconnecting from MongoDB: {e}")


# Instantiate MongoDB
mongodb = MongoDB()


# Helper functions for connection lifecycle
def connect_to_mongo():
    mongodb.connect()


def close_mongo_connection():
    mongodb.close()
