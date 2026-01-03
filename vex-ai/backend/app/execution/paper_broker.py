import random
from typing import Dict

from app.engine.intents import TradeIntent
from app.risk.cost_engine import CostBreakdown


class PaperBroker:
    async def execute(self, intent: TradeIntent, cost: CostBreakdown) -> Dict:
        slip = cost.slippage_bps / 10000 * intent.entry
        fill_price = intent.entry + (slip if intent.side == "BUY" else -slip)
        return {"status": "filled", "fill_price": fill_price, "pnl": 0.0}
