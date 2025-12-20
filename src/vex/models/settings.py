from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    """Application configuration loaded from environment variables."""

    environment: str = "local"
    redis_url: str = "redis://localhost:6379/0"
    database_url: str = "postgresql+psycopg://vex:vex@localhost:5432/vex"
    decision_interval_seconds: int = 5
    max_risk_per_trade: float = 0.005
    min_projected_r_multiple: float = 5.0

    model_config = SettingsConfigDict(env_prefix="VEX_")
