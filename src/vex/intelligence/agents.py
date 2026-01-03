from __future__ import annotations

from abc import ABC, abstractmethod

from pydantic import BaseModel

from vex.data.market_state import MarketState


class AgentSignal(BaseModel):
    agent: str
    direction: str
    confidence: float
    invalidation_price: float
    volatility_context: float


class SignalAgent(ABC):
    name: str

    @abstractmethod
    def generate(self, market_state: MarketState) -> AgentSignal:
        raise NotImplementedError


class MomentumAgent(SignalAgent):
    name = "momentum"

    def generate(self, market_state: MarketState) -> AgentSignal:
        direction = "flat"
        confidence = 0.0
        if market_state.regime in {"trend", "expansion"} and market_state.vwap > 0:
            delta = (market_state.last_price - market_state.vwap) / market_state.vwap
            if delta > market_state.volatility:
                direction = "long"
                confidence = min(1.0, delta * 5)
            elif delta < -market_state.volatility:
                direction = "short"
                confidence = min(1.0, abs(delta) * 5)
        return AgentSignal(
            agent=self.name,
            direction=direction,
            confidence=confidence,
            invalidation_price=market_state.last_price,
            volatility_context=market_state.volatility,
        )


class MeanReversionAgent(SignalAgent):
    name = "mean_reversion"

    def generate(self, market_state: MarketState) -> AgentSignal:
        direction = "flat"
        confidence = 0.0
        if market_state.regime in {"range", "neutral"} and market_state.vwap > 0:
            delta = (market_state.last_price - market_state.vwap) / market_state.vwap
            threshold = market_state.volatility * 1.5
            if delta > threshold:
                direction = "short"
                confidence = min(1.0, delta * 4)
            elif delta < -threshold:
                direction = "long"
                confidence = min(1.0, abs(delta) * 4)
        return AgentSignal(
            agent=self.name,
            direction=direction,
            confidence=confidence,
            invalidation_price=market_state.last_price,
            volatility_context=market_state.volatility,
        )


class BreakoutAgent(SignalAgent):
    name = "breakout"

    def generate(self, market_state: MarketState) -> AgentSignal:
        direction = "flat"
        confidence = 0.0
        if market_state.regime in {"compression", "expansion"} and market_state.vwap > 0:
            delta = (market_state.last_price - market_state.vwap) / market_state.vwap
            if abs(delta) > market_state.volatility * 2:
                direction = "long" if delta > 0 else "short"
                confidence = min(1.0, abs(delta) * 6)
        return AgentSignal(
            agent=self.name,
            direction=direction,
            confidence=confidence,
            invalidation_price=market_state.last_price,
            volatility_context=market_state.volatility,
        )
