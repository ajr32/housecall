from housecall.health import MissingFriendlyNamesHealthCheck


def test_friendly_names_pass(monkeypatch):
    def mock_scan():
        return {
            "states": [
                {
                    "entity_id": "sensor.one",
                    "attributes": {
                        "friendly_name": "Sensor One",
                    },
                },
                {
                    "entity_id": "sensor.two",
                    "attributes": {
                        "friendly_name": "Sensor Two",
                    },
                },
            ]
        }

    monkeypatch.setattr("housecall.health.scan", mock_scan)

    result = MissingFriendlyNamesHealthCheck().run()

    assert result.passed is True
    assert result.message == "All entities have friendly names"


def test_friendly_names_fail(monkeypatch):
    def mock_scan():
        return {
            "states": [
                {
                    "entity_id": "sensor.one",
                    "attributes": {
                        "friendly_name": "Sensor One",
                    },
                },
                {
                    "entity_id": "sensor.two",
                    "attributes": {},
                },
            ]
        }

    monkeypatch.setattr("housecall.health.scan", mock_scan)

    result = MissingFriendlyNamesHealthCheck().run()

    assert result.passed is False
    assert result.message == "1 entities missing friendly names"