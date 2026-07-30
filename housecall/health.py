"""
Health check model for HouseCall.
"""

from abc import ABC, abstractmethod
from .diagnostics import Diagnostic
from .scanner import scan


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


class UnavailableEntitiesHealthCheck(HealthCheck):
    """Checks for unavailable Home Assistant entities."""

    def __init__(self):
        super().__init__("Unavailable Entities")

    def run(self) -> Diagnostic:
        inventory = scan()

        unavailable = inventory["summary"]["unavailable_entities"]

        if unavailable:
            return Diagnostic(
                self.name,
                False,
                f"{len(unavailable)} unavailable entities detected.",
            )

        return Diagnostic(
            self.name,
            True,
            "No unavailable entities found.",
        )

class UnknownEntitiesHealthCheck(HealthCheck):
    """Checks for unknown Home Assistant entities."""

    def __init__(self):
        super().__init__("Unknown Entities")

    def run(self) -> Diagnostic:
        inventory = scan()

        unknown = inventory["summary"]["unknown_entities"]

        if unknown:
            return Diagnostic(
                self.name,
                False,
                f"{len(unknown)} unknown entities detected.",
            )

        return Diagnostic(
            self.name,
            True,
            "No unknown entities found.",
        )


HEALTH_CHECKS = [
    ConfigurationHealthCheck(),
    ConnectionHealthCheck(),
    UnavailableEntitiesHealthCheck(),
    UnknownEntitiesHealthCheck(),
]