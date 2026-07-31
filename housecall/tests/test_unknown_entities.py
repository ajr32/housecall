import pytest

from housecall.health import UnknownEntitiesHealthCheck


def test_unknown_entities_pass(monkeypatch):
    def mock_scan():
        return {
            "summary": {
                "unknown_entities": [],
            }
        }

    monkeypatch.setattr("housecall.health.scan", mock_scan)

    result = UnknownEntitiesHealthCheck().run()

    assert result.passed is True
    assert result.message == "None found"


def test_unknown_entities_fail(monkeypatch):
    def mock_scan():
        return {
            "summary": {
                "unknown_entities": [
                    "sensor.one",
                    "sensor.two",
                ],
            }
        }

    monkeypatch.setattr("housecall.health.scan", mock_scan)

    result = UnknownEntitiesHealthCheck().run()

    assert result.passed is False
    assert result.message == "2 unknown entities detected"