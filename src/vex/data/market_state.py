from __future__ import annotations

from datetime import datetime, timezone

from pydantic import BaseModel

from vex.models.settings import AppSettings

class MarketState(BaseModel):
    as_of: str
    regime: str
    volatility: float
    vwap: float
    last_price: float


class MarketStateBuilder:
    def __init__(self, settings: AppSettings) -> None:
        self.settings = settings

    def build(self) -> MarketState:
        now = datetime.now(timezone.utc).isoformat()
        return MarketState(
            as_of=now,
            regime=self.settings.default_market_regime,
            volatility=self.settings.default_volatility,
            vwap=self.settings.default_vwap,
            last_price=self.settings.default_last_price,
        )
