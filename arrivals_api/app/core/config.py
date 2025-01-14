from dotenv import load_dotenv
from pydantic import Field, ValidationError
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    write_db_url: str = Field(
        json_schema_extra={"env": "WRITE_DB_URL"},
    )

    read_db_url: str = Field(
        json_schema_extra={"env": "READ_DB_URL"},
    )
    read_db_name: str = Field(
        json_schema_extra={"env": "READ_DB_NAME"},
    )

    initial_admin_username: str = Field(
        json_schema_extra={"env": "INITIAL_ADMIN_USERNAME"},
    )
    initial_admin_password: str = Field(
        json_schema_extra={"env": "INITIAL_ADMIN_PASSWORD"},
    )

    secret_key: str = Field(
        json_schema_extra={"env": "SECRET_KEY"},
    )
    algorithm: str = Field(
        json_schema_extra={"env": "ALGORITHM"},
    )
    access_token_expire_minutes: int = Field(
        json_schema_extra={"env": "ACCESS_TOKEN_EXPIRE_MINUTES"},
    )
    enable_data_generation: bool = Field(
        json_schema_extra={"env": "ENABLE_DATA_GENERATION"},
    )
    total_records: int = Field(
        json_schema_extra={"env": "TOTAL_RECORDS"},
    )

    batch_size: int = Field(
        json_schema_extra={"env": "BATCH_SIZE"},
    )

    class Config:
        env_file = ".env"


try:
    settings = Settings()
except ValidationError as e:
    print(e.json())
    raise
