from housecall.health import UnavailableEntitiesHealthCheck


def test_unavailable_entities_pass(monkeypatch):
    def mock_scan():
        return {
            "summary": {
                "unavailable_entities": [],
            }
        }

    monkeypatch.setattr("housecall.health.scan", mock_scan)

    result = UnavailableEntitiesHealthCheck().run()

    assert result.passed is True
    assert result.message == "None found"


def test_unavailable_entities_fail(monkeypatch):
    def mock_scan():
        return {
            "summary": {
                "unavailable_entities": [
                    "sensor.one",
                    "sensor.two",
                ],
            }
        }

    monkeypatch.setattr("housecall.health.scan", mock_scan)

    result = UnavailableEntitiesHealthCheck().run()

    assert result.passed is False
    assert result.message == "2 unavailable entities detected"