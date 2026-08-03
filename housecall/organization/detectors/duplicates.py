"""
Duplicate name detector.
"""

from collections import defaultdict

from ..models import NamingIssue


def detect_duplicates(items):
    """Detect duplicate names."""

    groups = defaultdict(list)

    for item in items:
        name = item.get("name")

        if name:
            groups[name].append(name)

    issues = []

    for name, matches in groups.items():
        if len(matches) > 1:
            issues.append(
                NamingIssue(
                    category="Duplicate Names",
                    severity="Medium",
                    message=f'Duplicate name "{name}" found.',
                    recommendation="Rename one or more items to make them unique.",
                    items=matches,
                )
            )

    return issues