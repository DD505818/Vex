from __future__ import annotations

from datetime import datetime, timezone

from pydantic import BaseModel, Field


class MarketState(BaseModel):
    as_of: str
    regime: str
    volatility: float
    vwap: float
    last_price: float


class MarketStateBuilder:
    def build(self) -> MarketState:
        now = datetime.now(timezone.utc).isoformat()
        return MarketState(
            as_of=now,
            regime="neutral",
            volatility=0.0,
            vwap=0.0,
            last_price=0.0,
        )
