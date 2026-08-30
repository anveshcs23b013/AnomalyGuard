import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    # App Config
    APP_NAME: str = "AnomalyGuard"
    DEBUG_MODE: bool = True
    
    # Kafka Configuration
    KAFKA_BOOTSTRAP_SERVERS: str
    KAFKA_API_KEY: str
    KAFKA_API_SECRET: str
    KAFKA_TOPIC: str = "user_stream_v1"
    
    # Paths
    BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    FEATURE_REPO_PATH: str = os.path.join(BASE_DIR, "feature_repo")
    MODEL_PATH: str = os.path.join(BASE_DIR, "services", "model.pkl")

    # New Pydantic V2 Config
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)

@lru_cache()
def get_settings():
    return Settings()