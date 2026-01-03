from app.risk.risk_engine import RiskEngine
from app.risk.limits import RiskLimits
from app.risk.cost_engine import CostBreakdown
from app.engine.intents import TradeIntent


def test_edge_must_exceed_cost():
    engine = RiskEngine(RiskLimits())
    intent = TradeIntent(
        symbol="BTCUSD",
        side="BUY",
        entry=100,
        stop=99,
        take_profit=102,
        expected_edge_bps=2,
        expected_hold_seconds=60,
        confidence=0.5,
    )
    cost = CostBreakdown(fee_bps=2, spread_bps=2, slippage_bps=1, latency_tax_bps=1)
    result = engine.assess(intent, cost)
    assert result.approved is False
    assert result.reason == "edge_not_greater_than_cost"


def test_exposure_and_drawdown_limits_block_trades():
    limits = RiskLimits(max_exposure_per_symbol=0.1, max_drawdown=0.1, max_open_positions=1)
    engine = RiskEngine(limits)
    # Simulate drawdown
    engine.state.equity = 85000
    engine.state.peak_equity = 100000

    intent = TradeIntent(
        symbol="ETHUSD",
        side="BUY",
        entry=100,
        stop=95,
        take_profit=110,
        expected_edge_bps=50,
        expected_hold_seconds=60,
        confidence=0.8,
        capital_at_risk=20000,
    )
    cost = CostBreakdown(fee_bps=2, spread_bps=2, slippage_bps=1, latency_tax_bps=1)
    result = engine.assess(intent, cost)
    assert result.approved is False
    assert result.reason == "drawdown_limit"

    # Recover equity to allow gating to progress to exposure check
    engine.state.equity = 100000
    engine.state.peak_equity = 100000
    result = engine.assess(intent, cost)
    assert result.approved is False
    assert result.reason == "exposure_limit"

    # Record a small fill to consume open position slot
    intent.capital_at_risk = 5000
    result = engine.assess(intent, cost)
    assert result.approved is True
    engine.record_fill(intent, {"pnl": 100})

    # Additional intent should now trip open position limit
    next_intent = TradeIntent(
        symbol="BTCUSD",
        side="SELL",
        entry=100,
        stop=101,
        take_profit=90,
        expected_edge_bps=50,
        expected_hold_seconds=60,
        confidence=0.8,
        capital_at_risk=5000,
    )
    result = engine.assess(next_intent, cost)
    assert result.approved is False
    assert result.reason == "open_positions_limit"
