import random
from typing import Dict

from app.engine.intents import TradeIntent
from app.risk.cost_engine import CostBreakdown


class PaperBroker:
    async def execute(self, intent: TradeIntent, cost: CostBreakdown) -> Dict:
        slip = cost.slippage_bps / 10000 * intent.entry
        fill_price = intent.entry + (slip if intent.side == "BUY" else -slip)
        pnl = (intent.take_profit - fill_price) if intent.side == "BUY" else (fill_price - intent.take_profit)
        return {"status": "filled", "fill_price": fill_price, "pnl": pnl}
