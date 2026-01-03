from pydantic import BaseModel


class RiskLimits(BaseModel):
    max_drawdown: float = 0.25
    max_exposure_per_symbol: float = 0.2
    max_open_positions: int = 5
    min_r_multiple_paper: float = 2.0
    min_r_multiple_live: float = 3.0
    safety_margin_bps: float = 5.0
