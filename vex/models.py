from enum import Enum

from pydantic import BaseModel, Field, PositiveFloat


class Direction(str, Enum):
    long = "long"
    short = "short"
    flat = "flat"


class Signal(BaseModel):
    agent: str = Field(min_length=1)
    direction: Direction
    confidence: float = Field(ge=0, le=1)
    invalidation_price: PositiveFloat
    volatility_context: float = Field(ge=0)
    weight: float = Field(default=1.0, gt=0)


class ConsensusRequest(BaseModel):
    signals: list[Signal]
    min_quorum: int = Field(default=2, ge=1)
    confidence_threshold: float = Field(default=0.6, ge=0, le=1)
    min_projected_r: float = Field(default=5.0, ge=0)


class ConsensusResponse(BaseModel):
    side: Direction
    strength: float = Field(ge=0, le=1)
    max_size: float = Field(ge=0)
    ttl_seconds: int = Field(ge=0)
    projected_r: float = Field(ge=0)


class RiskLimits(BaseModel):
    per_trade_risk: float = Field(default=0.01, gt=0)
    max_portfolio_risk: float = Field(default=0.1, gt=0)
    max_drawdown: float = Field(default=0.2, gt=0)
    min_projected_r: float = Field(default=5.0, ge=0)


class RiskState(BaseModel):
    equity: PositiveFloat = Field(default=100000)
    current_drawdown: float = Field(default=0, ge=0)
    portfolio_risk: float = Field(default=0, ge=0)


class RiskQualificationRequest(BaseModel):
    risk_amount: PositiveFloat
    projected_r: float = Field(ge=0)
    state: RiskState
    limits: RiskLimits = Field(default_factory=RiskLimits)


class RiskQualificationResponse(BaseModel):
    approved: bool
    reasons: list[str] = Field(default_factory=list)
