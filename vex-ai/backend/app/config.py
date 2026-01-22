from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, field_validator

from typing import List


class Settings(BaseSettings):
    app_name: str = "VEX AI ELITE"
    trading_mode: str = Field(default="PAPER", pattern="^(PAPER|LIVE)$")
    jwt_secret: str = "vex-secret"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60
    live_arm_duration_minutes: int = 10
    database_url: str = "sqlite:///./vex.db"
    allowed_origins: List[str] = Field(default_factory=lambda: ["*"])

    model_config = SettingsConfigDict(env_prefix="", case_sensitive=False)

    @field_validator("allowed_origins", mode="before")
    @classmethod
    def parse_allowed_origins(cls, value):
        if value is None or value == "":
            return ["*"]
        if isinstance(value, str):
            if value.strip() == "*":
                return ["*"]
            return [origin.strip() for origin in value.split(",") if origin.strip()]
        return value


def get_settings() -> Settings:
    return Settings()
