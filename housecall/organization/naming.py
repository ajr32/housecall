"""
HouseCall naming consistency engine.
"""

from .detectors.formatting import (
    detect_capitalization,
    detect_numbering,
    detect_punctuation,
    detect_spacing,
)
from .detectors.language import (
    detect_abbreviations,
    detect_pluralization,
    detect_word_order,
)
from .detectors.structure import (
    detect_duplicate_names,
    detect_mixed_naming_styles,
)

DETECTORS = (
    detect_duplicate_names,
    detect_capitalization,
    detect_spacing,
    detect_punctuation,
    detect_numbering,
    detect_abbreviations,
    detect_pluralization,
    detect_mixed_naming_styles,
    detect_word_order,
)


def find_naming_issues(items):
    """Run all naming detectors."""

    issues = []

    for detector in DETECTORS:
        issues.extend(detector(items))

    return issues
