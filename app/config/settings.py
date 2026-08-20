"""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    app_name: str
    app_version: str
    environment: str

    ollama_base_url: str
    ollama_model: str

    chroma_db_path: str

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False
    )



settings = Settings()
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    app_name: str
    app_version: str
    environment: str

    hf_token: str
    hf_model: str

    chroma_db_path: str

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False
    )


settings = Settings()