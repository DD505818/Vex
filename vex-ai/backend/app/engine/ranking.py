from typing import List

from app.engine.intents import TradeIntent
from app.risk.cost_engine import CostBreakdown


def rank_intents(intents: List[TradeIntent], costs: List[CostBreakdown]):
    scored = []
    for intent, cost in zip(intents, costs):
        expected_net = intent.expected_edge_bps - cost.total_bps
        density = expected_net / max(intent.expected_hold_seconds, 1) / max(intent.capital_at_risk, 1)
        scored.append((density, intent, cost))
    scored.sort(key=lambda x: x[0], reverse=True)
    return scored
