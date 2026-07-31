from datetime import datetime, timedelta, timezone

from housecall.health import StaleEntitiesHealthCheck


def test_stale_entities_pass(monkeypatch):
    def mock_scan():
        return {
            "states": [
                {
                    "entity_id": "sensor.one",
                    "last_updated": datetime.now(timezone.utc).isoformat(),
                },
            ]
        }

    monkeypatch.setattr("housecall.health.scan", mock_scan)

    result = StaleEntitiesHealthCheck().run()

    assert result.passed is True
    assert result.message == "All active entities have updated recently"


def test_stale_entities_fail(monkeypatch):
    def mock_scan():
        return {
            "states": [
                {
                    "entity_id": "sensor.one",
                    "last_updated": (
                        datetime.now(timezone.utc)
                        - timedelta(days=30)
                    ).isoformat(),
                },
            ]
        }

    monkeypatch.setattr("housecall.health.scan", mock_scan)

    result = StaleEntitiesHealthCheck().run()

    assert result.passed is False
    assert result.message == "1 entities have not updated in over 7 days"