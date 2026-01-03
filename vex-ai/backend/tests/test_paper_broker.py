import asyncio

from app.engine.intents import TradeIntent
from app.execution.paper_broker import PaperBroker
from app.risk.cost_engine import CostBreakdown
from app.risk.limits import RiskLimits
from app.risk.risk_engine import RiskEngine


def test_paper_broker_does_not_credit_unrealized_pnl_on_entry():
    broker = PaperBroker()
    intent = TradeIntent(
        symbol="ETHUSD",
        side="BUY",
        entry=1000.0,
        stop=950.0,
        take_profit=1100.0,
        expected_edge_bps=50,
        expected_hold_seconds=60,
        confidence=0.9,
        capital_at_risk=5000,
    )
    cost = CostBreakdown(fee_bps=0, spread_bps=0, slippage_bps=0, latency_tax_bps=0)

    fill = asyncio.run(broker.execute(intent, cost))

    assert fill["pnl"] == 0.0

    engine = RiskEngine(RiskLimits())
    starting_equity = engine.state.equity

    engine.record_fill(intent, fill)

    assert engine.state.equity == starting_equity
