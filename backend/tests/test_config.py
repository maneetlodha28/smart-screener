from app.core.config import get_settings


def _clear_cache() -> None:
    get_settings.cache_clear()  # type: ignore[attr-defined]


def test_settings_defaults(monkeypatch) -> None:
    monkeypatch.delenv("APP_ENV", raising=False)
    monkeypatch.delenv("LOG_LEVEL", raising=False)
    monkeypatch.delenv("DATABASE_URL", raising=False)
    monkeypatch.delenv("AI_PROVIDER", raising=False)
    monkeypatch.delenv("AI_API_KEY", raising=False)
    _clear_cache()
    settings = get_settings()
    assert settings.APP_ENV == "development"
    assert settings.LOG_LEVEL == "INFO"
    assert settings.DATABASE_URL == "sqlite:///:memory:"
    assert settings.AI_PROVIDER == "mock"
    assert settings.AI_API_KEY is None


def test_settings_env_overrides(monkeypatch) -> None:
    monkeypatch.setenv("APP_ENV", "production")
    monkeypatch.setenv("LOG_LEVEL", "DEBUG")
    monkeypatch.setenv("DATABASE_URL", "postgresql://db")
    monkeypatch.setenv("AI_PROVIDER", "openai")
    monkeypatch.setenv("AI_API_KEY", "token")
    _clear_cache()
    settings = get_settings()
    assert settings.APP_ENV == "production"
    assert settings.LOG_LEVEL == "DEBUG"
    assert settings.DATABASE_URL == "postgresql://db"
    assert settings.AI_PROVIDER == "openai"
    assert settings.AI_API_KEY == "token"
