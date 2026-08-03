"""
Duplicate name detector.
"""

import re
from collections import defaultdict

from ..models import NamingIssue


def detect_duplicate_names(items):
    """
    Detect duplicate names.
    eg: Kitchen Light, Kitchen Light, Garage Light
    """

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


def detect_mixed_naming_styles(items):
    """
    Detect mixed naming styles.

    eg: Kitchen Light, living_room, Garage-Door, officeLight
    """

    styles = {}

    for item in items:
        name = item.get("name")

        if not name:
            continue

        style = classify_style(name)

        styles.setdefault(style, []).append(name)

    if len(styles) <= 1:
        return []

    return [
        NamingIssue(
            category="Naming Style",
            severity="Low",
            message="Multiple naming styles detected.",
            recommendation="Use a single naming convention throughout Home Assistant.",
            items=[
                f"{style}: {', '.join(sorted(names))}"
                for style, names in sorted(styles.items())
            ],
        )
    ]


def classify_style(name):
    """Classify a naming style."""

    if "_" in name:
        return "snake_case"

    if "-" in name:
        return "kebab-case"

    if re.search(r"[a-z][A-Z]", name):
        return "camelCase"

    if name == name.upper():
        return "UPPER CASE"

    if re.match(r"^[A-Z][A-Za-z0-9]*( [A-Z][A-Za-z0-9]*)*$", name):
        return "Title Case"

    return "Other"
