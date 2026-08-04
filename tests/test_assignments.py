from housecall.organization.detectors.assignments import (
    detect_unused_labels,
)


def test_detect_unused_labels():
    labels = [
        {"label_id": "favorite", "name": "Favorite"},
        {"label_id": "holiday", "name": "Holiday"},
    ]

    devices = [
        {"name": "Kitchen Light", "label_ids": ["favorite"]},
    ]

    entities = []

    issues = detect_unused_labels(labels, devices, entities)

    assert len(issues) == 1
    assert issues[0].category == "Unused Labels"
    assert issues[0].items == ["Holiday"]


def test_no_unused_labels():
    labels = [
        {"label_id": "favorite", "name": "Favorite"},
    ]

    devices = [
        {"name": "Kitchen Light", "label_ids": ["favorite"]},
    ]

    entities = []

    issues = detect_unused_labels(labels, devices, entities)

    assert issues == []