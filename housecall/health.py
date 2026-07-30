"""
Health check model for HouseCall.
"""

from abc import ABC, abstractmethod

from .diagnostics import Diagnostic


class HealthCheck(ABC):
    """Base class for all health checks."""

    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def run(self) -> Diagnostic:
        """Run the health check and return a Diagnostic."""
        pass

from .config import validate_configuration


class ConfigurationHealthCheck(HealthCheck):
    """Checks that the HouseCall configuration is valid."""

    def __init__(self):
        super().__init__("Configuration")

    def run(self) -> Diagnostic:
        try:
            validate_configuration()
            return Diagnostic(
                self.name,
                True,
                "Configuration OK",
            )
        except Exception as exc:
            return Diagnostic(
                self.name,
                False,
                str(exc),
            )

from .api import client


class ConnectionHealthCheck(HealthCheck):
    """Checks the Home Assistant connection."""

    def __init__(self):
        super().__init__("Connection")

    def run(self) -> Diagnostic:
        try:
            client.test_connection()
            return Diagnostic(
                self.name,
                True,
                "Home Assistant connection",
            )
        except Exception as exc:
            return Diagnostic(
                self.name,
                False,
                str(exc),
            )

HEALTH_CHECKS = [
    ConfigurationHealthCheck(),
    ConnectionHealthCheck(),
]