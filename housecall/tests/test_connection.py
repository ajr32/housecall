from housecall.health import ConnectionHealthCheck


def test_connection_success(monkeypatch):
    def fake_connection():
        pass

    monkeypatch.setattr(
        "housecall.health.client.test_connection",
        fake_connection,
    )

    result = ConnectionHealthCheck().run()

    assert result.passed is True
    assert result.name == "Connection"
    assert result.message == "Connected"


def test_connection_failure(monkeypatch):
    def fake_connection():
        raise ConnectionError("Unable to connect")

    monkeypatch.setattr(
        "housecall.health.client.test_connection",
        fake_connection,
    )

    result = ConnectionHealthCheck().run()

    assert result.passed is False
    assert result.name == "Connection"
    assert result.message == "Unable to connect"