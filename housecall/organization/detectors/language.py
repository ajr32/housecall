"""
Language detectors.
"""

from collections import defaultdict

from ..models import NamingIssue

ABBREVIATIONS = {
    "temp": "temperature",
    "tmp": "temperature",
    "humid": "humidity",
    "tv": "television",
    "lr": "living room",
    "br": "bedroom",
    "dr": "dining room",
    "rm": "room",
}


def detect_abbreviations(items):
    """
    Detect abbreviation inconsistencies.

    eg: Temperature, Temp, TMP
    """

    def normalize_abbreviations(item_name):
        """Expand known abbreviations."""

        words = []

        for word in item_name.casefold().split():
            words.append(ABBREVIATIONS.get(word, word))

        return " ".join(words)

    groups = defaultdict(set)

    for item in items:
        item_name = item.get("name")

        if item_name:
            groups[normalize_abbreviations(item_name)].add(item_name)

    issues = []

    for variants in groups.values():
        if len(variants) > 1:
            issues.append(
                NamingIssue(
                    category="Abbreviations",
                    severity="Low",
                    message="Inconsistent abbreviations detected.",
                    recommendation="Use abbreviations consistently.",
                    items=sorted(variants),
                )
            )

    return issues


def detect_pluralization(items):
    """
    Detect pluralization inconsistencies.

    eg: Camera, Cameras
    """

    def normalize_pluralization(item_name):
        """Normalize singular and plural forms."""

        words = []

        for word in item_name.casefold().split():
            if len(word) > 2 and word.endswith("s"):
                word = word[:-1]

            words.append(word)

        return " ".join(words)

    groups = defaultdict(set)

    for item in items:
        item_name = item.get("name")

        if item_name:
            groups[normalize_pluralization(item_name)].add(item_name)

    issues = []

    for variants in groups.values():
        if len(variants) > 1:
            issues.append(
                NamingIssue(
                    category="Pluralization",
                    severity="Low",
                    message="Inconsistent pluralization detected.",
                    recommendation="Use singular or plural names consistently.",
                    items=sorted(variants),
                )
            )

    return issues


def detect_word_order(items):
    """
    Detect word order inconsistencies.

    eg: Kitchen Light, Light Kitchen
    """

    def normalize_word_order(item_name):
        """Normalize word order for comparison."""

        words = item_name.casefold().split()
        words.sort()

        return " ".join(words)

    groups = defaultdict(set)

    for item in items:
        item_name = item.get("name")

        if item_name:
            groups[normalize_word_order(item_name)].add(item_name)

    issues = []

    for variants in groups.values():
        if len(variants) > 1:
            issues.append(
                NamingIssue(
                    category="Word Order",
                    severity="Low",
                    message="Inconsistent word order detected.",
                    recommendation="Use a consistent word order.",
                    items=sorted(variants),
                )
            )

    return issues
