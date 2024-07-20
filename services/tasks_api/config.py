from typing import Optional

from pydantic_settings import BaseSettings

class Config(BaseSettings):
    TABLE_NAME: str = "tasks"
    DYNAMODB_URL: Optional[str] = None