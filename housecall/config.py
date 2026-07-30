"""
HouseCall configuration management.
"""

import os

from .exceptions import ConfigurationError
from dotenv import load_dotenv

load_dotenv()


def get_setting(name: str) -> str:
    """Return a required configuration value."""

    value = os.getenv(name)

    if not value:
        raise ConfigurationError(
            f"Missing required configuration setting: {name}"
        )

    return value


HA_URL = get_setting("HA_URL").rstrip("/")
HA_TOKEN = get_setting("HA_TOKEN")


def validate_configuration():
    """Validate the application configuration."""

    get_setting("HA_URL")
    get_setting("HA_TOKEN")
