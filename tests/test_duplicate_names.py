from housecall.health import DuplicateEntityNamesHealthCheck


def test_duplicate_names_pass(monkeypatch):
    def mock_scan():
        return {
            "states": [
                {
                    "entity_id": "media_player.apple_tv",
                    "attributes": {
                        "friendly_name": "Apple TV",
                    },
                },
                {
                    "entity_id": "remote.apple_tv",
                    "attributes": {
                        "friendly_name": "Apple TV",
                    },
                },
            ]
        }

    monkeypatch.setattr("housecall.health.scan", mock_scan)

    result = DuplicateEntityNamesHealthCheck().run()

    assert result.passed is True
    assert result.message == "No duplicate friendly names found"


def test_duplicate_names_fail(monkeypatch):
    def mock_scan():
        return {
            "states": [
                {
                    "entity_id": "sensor.temp_1",
                    "attributes": {
                        "friendly_name": "Temperature",
                    },
                },
                {
                    "entity_id": "sensor.temp_2",
                    "attributes": {
                        "friendly_name": "Temperature",
                    },
                },
            ]
        }

    monkeypatch.setattr("housecall.health.scan", mock_scan)

    result = DuplicateEntityNamesHealthCheck().run()

    assert result.passed is False
    assert result.message == "2 entities have duplicate friendly names"
