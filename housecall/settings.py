"""
HouseCall application settings.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    app_name: str = "HouseCall"
    version: str = "0.3"

    output_file: str = "inventory.json"

    request_timeout: int = 30

    log_directory: str = "logs"
    log_level: str = "INFO"


settings = Settings()
