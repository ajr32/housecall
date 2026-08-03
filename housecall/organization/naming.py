"""
HouseCall naming consistency engine.
"""

from .detectors.duplicates import detect_duplicates


def find_naming_issues(items):
    """Run all naming detectors."""

    issues = []

    issues.extend(detect_duplicates(items))

    return issues