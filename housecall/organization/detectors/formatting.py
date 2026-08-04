import re
from collections import defaultdict

from ..models import OrganizationIssue


def detect_capitalization(items):
    """
    Capitalization detector.
        eg: Kitchen Light, kitchen light, KITCHEN LIGHT
    """

    groups = defaultdict(set)

    for item in items:
        name = item.get("name")

        if name:
            groups[name.casefold()].add(name)

    issues = []

    for variants in groups.values():
        if len(variants) > 1:
            issues.append(
                OrganizationIssue(
                    category="Capitalization",
                    severity="Low",
                    message="Inconsistent capitalization detected.",
                    recommendation="Use a consistent capitalization style.",
                    items=sorted(variants),
                )
            )

    return issues


def normalize_spacing(name):
    """
    Normalize spacing conventions.
        eg: LivingRoom, Living Room, Living_Room, Living-Room
    """
    return re.sub(r"[\s_-]+", "", name).casefold()


def detect_spacing(items):
    """
    Spacing detector - Detect spacing inconsistencies
        eg: LivingRoom, Living Room, Living_Room, Living-Room
    """

    groups = defaultdict(set)

    for item in items:
        name = item.get("name")

        if name:
            groups[normalize_spacing(name)].add(name)

    issues = []

    for variants in groups.values():
        if len(variants) > 1:
            issues.append(
                OrganizationIssue(
                    category="Spacing",
                    severity="Low",
                    message="Inconsistent spacing detected.",
                    recommendation=("Use a consistent spacing convention."),
                    items=sorted(variants),
                )
            )

    return issues


def detect_numbering(items):
    """
    Numbering detector - Detect numbering inconsistencies.
        eg: Camera1, Camera 1, Camera-1, Camera_1
    """

    def normalize_numbering(name):
        """Normalize numbering conventions."""

        name = name.casefold()

        # Remove spaces, hyphens, and underscores immediately before numbers
        return re.sub(r"[\s_-]+(?=\d)", "", name)

    groups = defaultdict(set)

    for item in items:
        name = item.get("name")

        if name:
            groups[normalize_numbering(name)].add(name)

    issues = []

    for variants in groups.values():
        if len(variants) > 1:
            issues.append(
                OrganizationIssue(
                    category="Numbering",
                    severity="Low",
                    message="Inconsistent numbering detected.",
                    recommendation="Use a consistent numbering convention.",
                    items=sorted(variants),
                )
            )

    return issues


def detect_punctuation(items):
    """
    Punctuation detector. Detect punctuation inconsistencies.
        eg: Front Door, Front.Door, Front:Door, Front/Door
    """

    def normalize_punctuation(name):
        """Remove punctuation for comparison."""

        return re.sub(r"[\W_]+", "", name).casefold()

    groups = defaultdict(set)

    for item in items:
        name = item.get("name")

        if name:
            groups[normalize_punctuation(name)].add(name)

    issues = []

    for variants in groups.values():
        if len(variants) > 1:
            issues.append(
                OrganizationIssue(
                    category="Punctuation",
                    severity="Low",
                    message="Inconsistent punctuation detected.",
                    recommendation="Use a consistent punctuation style.",
                    items=sorted(variants),
                )
            )

    return issues
