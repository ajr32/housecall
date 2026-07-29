"""
HouseCall application settings.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    """Application settings."""

    app_name: str = "HouseCall"
    version: str = "0.1.0"

    request_timeout: int = 30

    output_file: str = "inventory.json"

    log_level: str = "INFO"

    log_directory: str = "logs"


settings = Settings()