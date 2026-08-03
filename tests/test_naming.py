"""
Tests for HouseCall naming consistency detectors.
"""

from housecall.organization.naming import find_naming_issues


#
# Duplicate Names
#


def test_detect_duplicate_names():
    items = [
        {"name": "Kitchen Light"},
        {"name": "Kitchen Light"},
        {"name": "Garage Light"},
    ]

    issues = find_naming_issues(items)

    duplicate = [
        issue for issue in issues
        if issue.category == "Duplicate Names"
    ]

    assert len(duplicate) == 1


def test_no_duplicate_names():
    items = [
        {"name": "Kitchen Light"},
        {"name": "Garage Light"},
    ]

    issues = find_naming_issues(items)

    duplicate = [
        issue for issue in issues
        if issue.category == "Duplicate Names"
    ]

    assert duplicate == []


#
# Capitalization
#


def test_detect_capitalization():
    items = [
        {"name": "Kitchen Light"},
        {"name": "kitchen light"},
    ]

    issues = find_naming_issues(items)

    capitalization = [
        issue for issue in issues
        if issue.category == "Capitalization"
    ]

    assert len(capitalization) == 1


def test_no_capitalization():
    items = [
        {"name": "Kitchen Light"},
        {"name": "Garage Light"},
    ]

    issues = find_naming_issues(items)

    capitalization = [
        issue for issue in issues
        if issue.category == "Capitalization"
    ]

    assert capitalization == []


#
# Spacing
#


def test_detect_spacing():
    items = [
        {"name": "LivingRoom"},
        {"name": "Living Room"},
        {"name": "Living_Room"},
    ]

    issues = find_naming_issues(items)

    spacing = [
        issue for issue in issues
        if issue.category == "Spacing"
    ]

    assert len(spacing) == 1


def test_no_spacing():
    items = [
        {"name": "Kitchen"},
        {"name": "Garage"},
    ]

    issues = find_naming_issues(items)

    spacing = [
        issue for issue in issues
        if issue.category == "Spacing"
    ]

    assert spacing == []


#
# Punctuation
#


def test_detect_punctuation():
    items = [
        {"name": "Front Door"},
        {"name": "Front.Door"},
        {"name": "Front:Door"},
    ]

    issues = find_naming_issues(items)

    punctuation = [
        issue for issue in issues
        if issue.category == "Punctuation"
    ]

    assert len(punctuation) == 1


def test_no_punctuation():
    items = [
        {"name": "Kitchen"},
        {"name": "Garage"},
    ]

    issues = find_naming_issues(items)

    punctuation = [
        issue for issue in issues
        if issue.category == "Punctuation"
    ]

    assert punctuation == []


#
# Numbering
#


def test_detect_numbering():
    items = [
        {"name": "Camera1"},
        {"name": "Camera 1"},
        {"name": "Camera-1"},
        {"name": "Camera_1"},
    ]

    issues = find_naming_issues(items)

    numbering = [
        issue for issue in issues
        if issue.category == "Numbering"
    ]

    assert len(numbering) == 1


def test_no_numbering():
    items = [
        {"name": "Camera1"},
        {"name": "Camera2"},
    ]

    issues = find_naming_issues(items)

    numbering = [
        issue for issue in issues
        if issue.category == "Numbering"
    ]

    assert numbering == []


#
# Abbreviations
#


def test_detect_abbreviations():
    items = [
        {"name": "Living Room Temperature"},
        {"name": "Living Room Temp"},
        {"name": "Living Room TMP"},
    ]

    issues = find_naming_issues(items)

    abbreviations = [
        issue for issue in issues
        if issue.category == "Abbreviations"
    ]

    assert len(abbreviations) == 1


def test_no_abbreviations():
    items = [
        {"name": "Kitchen Temperature"},
        {"name": "Garage Temperature"},
    ]

    issues = find_naming_issues(items)

    abbreviations = [
        issue for issue in issues
        if issue.category == "Abbreviations"
    ]

    assert abbreviations == []


#
# Pluralization
#


def test_detect_pluralization():
    items = [
        {"name": "Camera"},
        {"name": "Cameras"},
    ]

    issues = find_naming_issues(items)

    pluralization = [
        issue for issue in issues
        if issue.category == "Pluralization"
    ]

    assert len(pluralization) == 1


def test_no_pluralization():
    items = [
        {"name": "Camera"},
        {"name": "Sensor"},
    ]

    issues = find_naming_issues(items)

    pluralization = [
        issue for issue in issues
        if issue.category == "Pluralization"
    ]

    assert pluralization == []


#
# Mixed Naming Styles
#


def test_detect_mixed_naming_styles():
    items = [
        {"name": "Kitchen Light"},
        {"name": "living_room"},
        {"name": "officeLight"},
        {"name": "Garage-Door"},
    ]

    issues = find_naming_issues(items)

    styles = [
        issue for issue in issues
        if issue.category == "Naming Style"
    ]

    assert len(styles) == 1


def test_no_mixed_naming_styles():
    items = [
        {"name": "Kitchen Light"},
        {"name": "Garage Door"},
        {"name": "Living Room"},
    ]

    issues = find_naming_issues(items)

    styles = [
        issue for issue in issues
        if issue.category == "Naming Style"
    ]

    assert styles == []


#
# Word Order
#


def test_detect_word_order():
    items = [
        {"name": "Kitchen Light"},
        {"name": "Light Kitchen"},
    ]

    issues = find_naming_issues(items)

    order = [
        issue for issue in issues
        if issue.category == "Word Order"
    ]

    assert len(order) == 1


def test_no_word_order():
    items = [
        {"name": "Kitchen Light"},
        {"name": "Garage Door"},
    ]

    issues = find_naming_issues(items)

    order = [
        issue for issue in issues
        if issue.category == "Word Order"
    ]

    assert order == []