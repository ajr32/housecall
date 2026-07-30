from housecall.exceptions import ConfigurationError
from housecall.health import ConfigurationHealthCheck


def test_configuration_success(monkeypatch):
    def fake_validate():
        pass

    monkeypatch.setattr(
        "housecall.health.validate_configuration",
        fake_validate,
    )

    result = ConfigurationHealthCheck().run()

    assert result.passed is True
    assert result.name == "Configuration"
    assert result.message == "OK"


def test_configuration_failure(monkeypatch):
    def fake_validate():
        raise ConfigurationError("Missing HA_TOKEN")

    monkeypatch.setattr(
        "housecall.health.validate_configuration",
        fake_validate,
    )

    result = ConfigurationHealthCheck().run()

    assert result.passed is False
    assert result.name == "Configuration"
    assert result.message == "Missing HA_TOKEN"
