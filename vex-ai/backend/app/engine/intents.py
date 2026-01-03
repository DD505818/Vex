from pydantic import BaseModel
from typing import Optional


class TradeIntent(BaseModel):
    symbol: str
    side: str
    entry: float
    stop: float
    take_profit: float
    expected_edge_bps: float
    expected_hold_seconds: float
    confidence: float
    capital_at_risk: float = 1000.0
    strategy: Optional[str] = None


class IntentResult(BaseModel):
    approved: bool
    reason: str
    net_edge_bps: float
