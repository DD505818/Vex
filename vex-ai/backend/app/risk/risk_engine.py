from app.engine.intents import TradeIntent, IntentResult
from app.engine.state import PortfolioState
from app.risk.cost_engine import CostBreakdown
from app.risk.limits import RiskLimits
from app.config import get_settings


class RiskEngine:
    def __init__(self, limits: RiskLimits):
        self.limits = limits
        self.settings = get_settings()
        self.state = PortfolioState(
            max_drawdown=limits.max_drawdown,
            max_exposure_per_symbol=limits.max_exposure_per_symbol,
            max_open_positions=limits.max_open_positions,
        )

    def assess(self, intent: TradeIntent, cost: CostBreakdown) -> IntentResult:
        self.state.prune_positions()
        if self.state.current_drawdown() >= self.limits.max_drawdown:
            return IntentResult(approved=False, reason="drawdown_limit", net_edge_bps=0)

        if len(self.state.open_positions) >= self.limits.max_open_positions:
            return IntentResult(approved=False, reason="open_positions_limit", net_edge_bps=0)

        projected_exposure = self.state.exposure(intent.symbol) + intent.capital_at_risk
        if projected_exposure > self.state.max_exposure_per_symbol * self.state.equity:
            return IntentResult(approved=False, reason="exposure_limit", net_edge_bps=0)

        total_cost = cost.total_bps + self.limits.safety_margin_bps
        expected_net = intent.expected_edge_bps - total_cost
        if expected_net <= 0:
            return IntentResult(approved=False, reason="edge_not_greater_than_cost", net_edge_bps=expected_net)

        reward = abs(intent.take_profit - intent.entry)
        risk = abs(intent.entry - intent.stop)
        expected_r = reward / max(risk, 1e-6)
        min_r = self.limits.min_r_multiple_live if self.settings.trading_mode == "LIVE" else self.limits.min_r_multiple_paper
        if expected_r < min_r:
            return IntentResult(approved=False, reason="r_multiple_too_low", net_edge_bps=expected_net)

        return IntentResult(approved=True, reason="approved", net_edge_bps=expected_net)

    def record_fill(self, intent: TradeIntent, fill_result: dict):
        pnl = float(fill_result.get("pnl", 0.0))
        self.state.register_fill(intent, pnl)
