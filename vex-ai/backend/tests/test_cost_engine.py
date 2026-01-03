from app.risk.cost_engine import CostEngine
from app.engine.intents import TradeIntent


def test_cost_engine_total():
    engine = CostEngine(maker_fee_bps=1.0, taker_fee_bps=2.0)
    intent = TradeIntent(
        symbol="BTCUSD",
        side="BUY",
        entry=100,
        stop=99,
        take_profit=102,
        expected_edge_bps=30,
        expected_hold_seconds=60,
        confidence=0.5,
    )
    tick = {"spread": 0.02, "volatility": 1.0, "latency": 10}
    cost = engine.estimate(intent, tick)
    assert cost.total_bps > 0
    assert round(cost.total_bps, 2) == round(cost.fee_bps + cost.spread_bps + cost.slippage_bps + cost.latency_tax_bps, 2)
