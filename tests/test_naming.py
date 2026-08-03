from housecall.organization.naming import find_naming_issues


def test_detect_duplicate_names():
    items = [
        {"name": "Kitchen Light"},
        {"name": "Kitchen Light"},
        {"name": "Garage Light"},
    ]

    issues = find_naming_issues(items)

    assert len(issues) == 1

    issue = issues[0]

    assert issue.category == "Duplicate Names"
    assert issue.severity == "Medium"
    assert len(issue.items) == 2
    assert "Kitchen Light" in issue.items