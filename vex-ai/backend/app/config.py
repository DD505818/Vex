from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    app_name: str = "VEX AI ELITE"
    trading_mode: str = Field(default="PAPER", pattern="^(PAPER|LIVE)$")
    jwt_secret: str = Field(..., env="JWT_SECRET")
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60
    live_arm_duration_minutes: int = 10
    database_url: str = "sqlite:///./vex.db"

    model_config = SettingsConfigDict(env_prefix="", case_sensitive=False)


def get_settings() -> Settings:
    return Settings()
