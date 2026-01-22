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
    symbol: str = Field(..., description="Asset symbol, e.g. AAPL, BTCUSDT")

    @field_validator("symbol")
    @classmethod
    def validate_symbol(cls, v: str) -> str:
        if not v or len(v) > 20:
            raise ValueError("Invalid symbol")
        return v.upper()


class OHLCRequest(BaseModel):
    symbol: str
    timeframe: Literal["1", "5", "15", "30", "60", "240", "D"]

    @field_validator("symbol")
    @classmethod
    def validate_symbol(cls, v: str) -> str:
        return v.upper()


class NewsRequest(BaseModel):
    symbol: Optional[str] = None
    limit: int = Field(default=5, ge=1, le=20)


class MetricExplanationRequest(BaseModel):
    metric: str = Field(..., description="Metric name, e.g. ATR, VWAP")


# =========================
# UI INTENT SCHEMAS
# =========================


class ChartIntent(BaseModel):
    type: Literal["chart"]
    symbol: str
    interval: str

    @field_validator("symbol")
    @classmethod
    def validate_symbol(cls, v: str) -> str:
        return v.upper()


class NewsIntent(BaseModel):
    type: Literal["news"]
    symbol: Optional[str]
    limit: int = Field(default=5, ge=1, le=20)


class MetricsIntent(BaseModel):
    type: Literal["metrics"]
    items: List[str] = Field(..., min_items=1, max_items=10)


class DebateIntent(BaseModel):
    type: Literal["debate"]
    topic: str
    bullish_summary: str
    bearish_summary: str
    conclusion: Optional[str] = None


UIIntent = Literal["chart", "news", "metrics", "debate"]
UIIntentModel = Union[ChartIntent, NewsIntent, MetricsIntent, DebateIntent]


# =========================
# AI RESPONSE SCHEMA
# =========================


class AIResponse(BaseModel):
    text: str = Field(..., description="Human-readable explanation")
    ui: Optional[List[UIIntentModel]] = Field(
        default=None, description="Optional list of UI intents"
    )

    @field_validator("text")
    @classmethod
    def validate_text(cls, v: str) -> str:
        if not v or len(v.strip()) < 5:
            raise ValueError("Text explanation too short")
        return v


# =========================
# VALIDATION HELPERS
# =========================


def validate_ui_intent(intent: dict) -> UIIntentModel:
    intent_type = intent.get("type")

    if intent_type == "chart":
        return ChartIntent(**intent)
    if intent_type == "news":
        return NewsIntent(**intent)
    if intent_type == "metrics":
        return MetricsIntent(**intent)
    if intent_type == "debate":
        return DebateIntent(**intent)

    raise ValueError(f"Unknown UI intent type: {intent_type}")
