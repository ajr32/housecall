"""
Health check model for HouseCall.
"""

from abc import ABC, abstractmethod

from housecall.exceptions import APIError, ConfigurationError

from .diagnostics import Diagnostic
from .scanner import scan


class HealthCheck(ABC):
    """Base class for all health checks."""

    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def run(self) -> Diagnostic:
        """Run the health check and return a Diagnostic."""


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
                "OK",
            )
        except ConfigurationError as exc:
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
                "Connected",
            )
        except APIError as exc:
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
                f"{len(unavailable)} unavailable entities detected",
            )

        return Diagnostic(
            self.name,
            True,
            "None found",
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
                f"{len(unknown)} unknown entities detected",
            )

        return Diagnostic(
            self.name,
            True,
            "None found",
        )


class MissingFriendlyNamesHealthCheck(HealthCheck):
    """Checks for entities missing friendly names."""

    def __init__(self):
        super().__init__("Friendly Names")

    def run(self) -> Diagnostic:
        inventory = scan()

        missing = []

        for state in inventory["states"]:
            friendly_name = state.get("attributes", {}).get("friendly_name")

            if not friendly_name or not friendly_name.strip():
                missing.append(state["entity_id"])

        if missing:
            return Diagnostic(
                self.name,
                False,
                f"{len(missing)} entities missing friendly names",
            )

        return Diagnostic(
            self.name,
            True,
            "All entities have friendly names",
        )


class DuplicateEntityNamesHealthCheck(HealthCheck):
    """Checks for duplicate friendly names."""

    def __init__(self):
        super().__init__("Duplicate Names")

    def run(self) -> Diagnostic:
        inventory = scan()

        names = {}

        for state in inventory["states"]:
            friendly_name = state.get("attributes", {}).get("friendly_name")

            if not friendly_name:
                continue

            entity_id = state.get("entity_id", "<unknown>")

            domain = entity_id.split(".", 1)[0]
            key = (domain, friendly_name)

            names.setdefault(key, []).append(entity_id)

        duplicates = []

        for entities in names.values():
            if len(entities) > 1:
                duplicates.extend(entities)

        if duplicates:
            return Diagnostic(
                self.name,
                False,
                f"{len(duplicates)} entities have duplicate friendly names",
            )

        return Diagnostic(
            self.name,
            True,
            "No duplicate friendly names found",
        )


HEALTH_CHECKS = [
    ConfigurationHealthCheck(),
    ConnectionHealthCheck(),
    UnavailableEntitiesHealthCheck(),
    UnknownEntitiesHealthCheck(),
    MissingFriendlyNamesHealthCheck(),
    DuplicateEntityNamesHealthCheck(),
]
