"""
Health check model for HouseCall.
"""

from abc import ABC, abstractmethod
from datetime import datetime, timedelta, timezone

from housecall.exceptions import APIError, ConfigurationError

from .diagnostics import Diagnostic
from .scanner import scan


# ============================================================================
# Base Classes
# ============================================================================


class HealthCheck(ABC):
    """Base class for all health checks."""

    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def run(self) -> Diagnostic:
        """Run the health check and return a Diagnostic."""


# ============================================================================
# Configuration Checks
# ============================================================================

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


# ============================================================================
# Entity State Checks
# ============================================================================


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


class StaleEntitiesHealthCheck(HealthCheck):
    """Checks for entities that have not updated recently."""

    STALE_DAYS = 7

    def __init__(self):
        super().__init__("Stale Entities")

    def run(self) -> Diagnostic:
        results = scan()
        states = results["states"]

        stale = []

        cutoff = datetime.now(timezone.utc) - timedelta(days=self.STALE_DAYS)

        for state in states:
            entity_id = state.get("entity_id")
            last_updated = state.get("last_updated")

            if not entity_id or not last_updated:
                continue

            updated = datetime.fromisoformat(
                last_updated.replace("Z", "+00:00")
            )

            if updated < cutoff:
                stale.append(entity_id)

        if stale:
            return Diagnostic(
                self.name,
                False,
                f"{len(stale)} entities have not updated in over {self.STALE_DAYS} days",
            )

        return Diagnostic(
            self.name,
            True,
            "All active entities have updated recently",
        )


# ============================================================================
# Entity Registry Checks
# ============================================================================


class DisabledEntitiesHealthCheck(HealthCheck):
    """Checks for disabled Home Assistant entities."""

    def __init__(self):
        super().__init__("Disabled Entities")

    def run(self) -> Diagnostic:
        inventory = scan()

        disabled = inventory["summary"]["disabled_entities"]

        if disabled:
            return Diagnostic(
                self.name,
                False,
                f"{len(disabled)} disabled entities detected",
            )

        return Diagnostic(
            self.name,
            True,
            "None found",
        )


class OrphanedEntitiesHealthCheck(HealthCheck):
    """Checks for orphaned Home Assistant entities."""

    def __init__(self):
        super().__init__("Orphaned Entities")

    def run(self) -> Diagnostic:
        inventory = scan()

        orphaned = inventory["summary"]["orphaned_entities"]

        if orphaned:
            return Diagnostic(
                self.name,
                False,
                f"{len(orphaned)} orphaned entities detected",
            )

        return Diagnostic(
            self.name,
            True,
            "None found",
        )


# ============================================================================
# Helper Checks
# ============================================================================


class DuplicateHelpersHealthCheck(HealthCheck):
    """Checks for duplicate Home Assistant helpers."""

    def __init__(self):
        super().__init__("Duplicate Helpers")

    def run(self) -> Diagnostic:
        inventory = scan()

        duplicates = inventory["summary"]["duplicate_helpers"]

        if duplicates:
            return Diagnostic(
                self.name,
                False,
                f"{len(duplicates)} duplicate helpers detected",
            )

        return Diagnostic(
            self.name,
            True,
            "None found",
        )


# ============================================================================
# Area Registry Checks
# ============================================================================


class EmptyAreasHealthCheck(HealthCheck):
    """Checks for empty Home Assistant areas."""

    def __init__(self):
        super().__init__("Empty Areas")

    def run(self) -> Diagnostic:
        inventory = scan()

        empty = inventory["summary"]["empty_areas"]

        if empty:
            return Diagnostic(
                self.name,
                False,
                f"{len(empty)} empty areas detected",
            )

        return Diagnostic(
            self.name,
            True,
            "None found",
        )


# ============================================================================
# Label Registry Checks
# ============================================================================


class EmptyLabelsHealthCheck(HealthCheck):
    """Checks for empty Home Assistant labels."""

    def __init__(self):
        super().__init__("Empty Labels")

    def run(self) -> Diagnostic:
        inventory = scan()

        empty = inventory["summary"]["empty_labels"]

        if empty:
            return Diagnostic(
                self.name,
                False,
                f"{len(empty)} empty labels detected",
            )

        return Diagnostic(
            self.name,
            True,
            "None found",
        )


# ============================================================================
# Health Check Registry
# ============================================================================


HEALTH_CHECKS = [
    ConfigurationHealthCheck(),
    ConnectionHealthCheck(),
    UnavailableEntitiesHealthCheck(),
    UnknownEntitiesHealthCheck(),
    MissingFriendlyNamesHealthCheck(),
    DuplicateEntityNamesHealthCheck(),
    StaleEntitiesHealthCheck(),
    DisabledEntitiesHealthCheck(),
    OrphanedEntitiesHealthCheck(),
    DuplicateHelpersHealthCheck(),
    EmptyAreasHealthCheck(),
    EmptyLabelsHealthCheck(),
]