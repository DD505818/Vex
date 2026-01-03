from pydantic import BaseModel


class CostBreakdown(BaseModel):
    fee_bps: float
    spread_bps: float
    slippage_bps: float
    latency_tax_bps: float

    @property
    def total_bps(self) -> float:
        return self.fee_bps + self.spread_bps + self.slippage_bps + self.latency_tax_bps


class CostEngine:
    def __init__(self, maker_fee_bps: float = 1.0, taker_fee_bps: float = 2.0):
        self.maker_fee_bps = maker_fee_bps
        self.taker_fee_bps = taker_fee_bps

    def estimate(self, intent, market_tick) -> CostBreakdown:
        spread_half = market_tick.get("spread", 0.01) * 10000 / 2
        fee = self.taker_fee_bps
        slippage = max(1.0, intent.capital_at_risk / 100000)
        latency_tax = market_tick.get("volatility", 1) * market_tick.get("latency", 10) / 100
        return CostBreakdown(
            fee_bps=fee,
            spread_bps=spread_half,
            slippage_bps=slippage,
            latency_tax_bps=latency_tax,
        )
