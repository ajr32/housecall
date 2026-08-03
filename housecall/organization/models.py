"""
Organization models.
"""

from dataclasses import dataclass


@dataclass
class NamingIssue:
    """Represents a detected naming inconsistency."""

    category: str
    severity: str
    message: str
    recommendation: str
    items: list[str]
