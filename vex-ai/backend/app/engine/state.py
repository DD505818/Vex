import time
from typing import Dict, List
from pydantic import BaseModel, Field

from app.storage.models import Trade


class PortfolioState(BaseModel):
    equity: float = 100000.0
    peak_equity: float = 100000.0
    open_positions: List[Dict] = Field(default_factory=list)
    max_drawdown: float = 0.2
    max_exposure_per_symbol: float = 0.2
    max_open_positions: int = 5

    def exposure(self, symbol: str) -> float:
        return sum(pos.get("notional", 0) for pos in self.open_positions if pos.get("symbol") == symbol)

    def current_drawdown(self) -> float:
        if self.peak_equity <= 0:
            return 0.0
        return max(0.0, (self.peak_equity - self.equity) / self.peak_equity)

    def register_fill(self, intent, pnl: float):
        size = intent.capital_at_risk / max(intent.entry, 1e-6)
        notional = abs(size * intent.entry)
        expiry = time.time() + intent.expected_hold_seconds
        self.open_positions.append(
            {
                "symbol": intent.symbol,
                "side": intent.side,
                "notional": notional,
                "expires_at": expiry,
                "strategy": intent.strategy,
            }
        )
        self.equity += pnl
        self.peak_equity = max(self.peak_equity, self.equity)

    def prune_positions(self):
        now = time.time()
        self.open_positions = [pos for pos in self.open_positions if pos.get("expires_at", 0) > now]


async def snapshot_from_trades(trades: List[Trade]) -> PortfolioState:
    equity = 100000.0 + sum(t.pnl for t in trades)
    return PortfolioState(equity=equity)
