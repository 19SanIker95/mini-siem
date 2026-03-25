
from pydantic import BaseModel
import os

class Settings(BaseModel):
    app_env: str = os.getenv("APP_ENV", "dev")
    database_url: str = os.getenv("DATABASE_URL", "")
    cors_origins: str = os.getenv("CORS_ORIGINS", "http://localhost:5173")

settings = Settings()
