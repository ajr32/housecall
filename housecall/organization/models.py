"""
Organization models.
"""

from dataclasses import dataclass


@dataclass
class OrganizationIssue:
    """Represents a detected naming inconsistency."""

    category: str
    severity: str
    message: str
    recommendation: str
    items: list[str]
