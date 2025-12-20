from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "VEX Ultimate"
    min_projected_r: float = 5.0
    consensus_quorum: int = 2
    confidence_threshold: float = 0.6

    model_config = SettingsConfigDict(env_prefix="VEX_")
