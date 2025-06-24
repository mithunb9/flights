from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
    # Application settings
    APP_ENV: str = "development"
    APP_DEBUG: bool = True
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8000

    # GENERAL
    DEFAULT_BOUNDS: str = "33.373294,32.473972,-97.524450,-96.453058"
    
    # FLIGHT RADAR
    FLIGHT_RADAR_TOKEN: str = os.getenv("FLIGHT_RADAR_TOKEN")
    
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

@lru_cache()
def get_settings() -> Settings:

    return Settings()

# Initialize settings
settings = get_settings()
