from pydantic import BaseModel
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./local.db"  # override with Postgres in Docker/Cloud
    SECRET_KEY: str = "dev-secret"
    OPENAI_API_KEY: str = ""
    ENV: str = "development"

    class Config:
        env_file = ".env"
        extra = "allow"


class StreamDelta(BaseModel):
    message_id: str
    delta: str