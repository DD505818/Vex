"""
VEX AI ELITE — SCHEMAS

This module defines all JSON schemas used by the AI layer.
Every AI response that includes structured data MUST conform
 to one of these schemas before being accepted by the system.

Invalid schema == rejected output.
"""

from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field, field_validator


# =========================
# TOOL CALL SCHEMAS
# =========================


class QuoteRequest(BaseModel):
    symbol: str = Field(..., min_length=1, max_length=20, description="Asset symbol, e.g. AAPL, BTCUSDT")

    @field_validator("symbol")
    @classmethod
    def validate_symbol(cls, v: str) -> str:
        if not v or len(v) > 20:
            raise ValueError("Symbol must be 1-20 characters")
        return v.upper().strip()


class OHLCRequest(BaseModel):
    symbol: str = Field(..., min_length=1, max_length=20, description="Asset symbol")
    timeframe: Literal["1", "5", "15", "30", "60", "240", "D"]

    @field_validator("symbol")
    @classmethod
    def validate_symbol(cls, v: str) -> str:
        if not v or len(v) > 20:
            raise ValueError("Symbol must be 1-20 characters")
        return v.upper().strip()


class NewsRequest(BaseModel):
    symbol: Optional[str] = Field(default=None, min_length=1, max_length=20)
    limit: int = Field(default=5, ge=1, le=20)

    @field_validator("symbol")
    @classmethod
    def validate_symbol(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return None
        if not v or len(v) > 20:
            raise ValueError("Symbol must be 1-20 characters")
        return v.upper().strip()


class MetricExplanationRequest(BaseModel):
    metric: str = Field(..., min_length=1, max_length=50, description="Metric name, e.g. ATR, VWAP")

    @field_validator("metric")
    @classmethod
    def validate_metric(cls, v: str) -> str:
        if not v or len(v) > 50:
            raise ValueError("Metric must be 1-50 characters")
        return v.upper().strip()


# =========================
# UI INTENT SCHEMAS
# =========================


class ChartIntent(BaseModel):
    type: Literal["chart"]
    symbol: str = Field(..., min_length=1, max_length=20)
    interval: str = Field(..., description="Interval: 1, 5, 15, 30, 60, 240, or D")

    @field_validator("symbol")
    @classmethod
    def validate_symbol(cls, v: str) -> str:
        if not v or len(v) > 20:
            raise ValueError("Symbol must be 1-20 characters")
        return v.upper().strip()

    @field_validator("interval")
    @classmethod
    def validate_interval(cls, v: str) -> str:
        valid_intervals = {"1", "5", "15", "30", "60", "240", "D"}
        if v not in valid_intervals:
            raise ValueError(f"Interval must be one of {valid_intervals}")
        return v


class NewsIntent(BaseModel):
    type: Literal["news"]
    symbol: Optional[str] = Field(default=None, min_length=1, max_length=20)
    limit: int = Field(default=5, ge=1, le=20)

    @field_validator("symbol")
    @classmethod
    def validate_symbol(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return None
        if not v or len(v) > 20:
            raise ValueError("Symbol must be 1-20 characters")
        return v.upper().strip()


class MetricsIntent(BaseModel):
    type: Literal["metrics"]
    items: List[str] = Field(..., min_items=1, max_items=10)

    @field_validator("items")
    @classmethod
    def validate_items(cls, v: List[str]) -> List[str]:
        if not v or len(v) == 0:
            raise ValueError("Must have at least 1 metric")
        if len(v) > 10:
            raise ValueError("Maximum 10 metrics allowed")
        for item in v:
            if not item or len(item) == 0 or len(item) > 50:
                raise ValueError("Each metric must be 1-50 characters")
        return [item.upper().strip() for item in v]


class DebateIntent(BaseModel):
    type: Literal["debate"]
    topic: str = Field(..., min_length=5, max_length=200)
    bullish_summary: str = Field(..., min_length=10, max_length=500)
    bearish_summary: str = Field(..., min_length=10, max_length=500)
    conclusion: Optional[str] = Field(default=None, min_length=5, max_length=500)

    @field_validator("topic")
    @classmethod
    def validate_topic(cls, v: str) -> str:
        if not v or len(v) < 5 or len(v) > 200:
            raise ValueError("Topic must be 5-200 characters")
        return v.strip()

    @field_validator("bullish_summary")
    @classmethod
    def validate_bullish(cls, v: str) -> str:
        if not v or len(v) < 10 or len(v) > 500:
            raise ValueError("Bullish summary must be 10-500 characters")
        return v.strip()

    @field_validator("bearish_summary")
    @classmethod
    def validate_bearish(cls, v: str) -> str:
        if not v or len(v) < 10 or len(v) > 500:
            raise ValueError("Bearish summary must be 10-500 characters")
        return v.strip()

    @field_validator("conclusion")
    @classmethod
    def validate_conclusion(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return None
        if len(v) < 5 or len(v) > 500:
            raise ValueError("Conclusion must be 5-500 characters")
        return v.strip()


UIIntent = Literal["chart", "news", "metrics", "debate"]
UIIntentModel = Union[ChartIntent, NewsIntent, MetricsIntent, DebateIntent]


# =========================
# AI RESPONSE SCHEMA
# =========================


class AIResponse(BaseModel):
    text: str = Field(..., min_length=5, max_length=5000, description="Human-readable explanation")
    ui: Optional[List[UIIntentModel]] = Field(
        default=None, description="Optional list of UI intents"
    )

    @field_validator("text")
    @classmethod
    def validate_text(cls, v: str) -> str:
        if not v or len(v.strip()) < 5 or len(v) > 5000:
            raise ValueError("Text explanation must be 5-5000 characters")
        return v.strip()


# =========================
# VALIDATION HELPERS
# =========================


def validate_ui_intent(intent: dict) -> UIIntentModel:
    """Validate and coerce a dict into a UIIntentModel."""
    if not isinstance(intent, dict):
        raise ValueError("Intent must be a dictionary")
    
    intent_type = intent.get("type")
    
    if not intent_type:
        raise ValueError("Intent must have 'type' field")

    if intent_type == "chart":
        return ChartIntent(**intent)
    elif intent_type == "news":
        return NewsIntent(**intent)
    elif intent_type == "metrics":
        return MetricsIntent(**intent)
    elif intent_type == "debate":
        return DebateIntent(**intent)
    else:
        raise ValueError(f"Unknown UI intent type: {intent_type}. Must be one of: chart, news, metrics, debate")