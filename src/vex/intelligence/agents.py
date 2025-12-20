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
        return AgentSignal(
            agent=self.name,
            direction="flat",
            confidence=0.0,
            invalidation_price=market_state.last_price,
            volatility_context=market_state.volatility,
        )


class MeanReversionAgent(SignalAgent):
    name = "mean_reversion"

    def generate(self, market_state: MarketState) -> AgentSignal:
        return AgentSignal(
            agent=self.name,
            direction="flat",
            confidence=0.0,
            invalidation_price=market_state.last_price,
            volatility_context=market_state.volatility,
        )


class BreakoutAgent(SignalAgent):
    name = "breakout"

    def generate(self, market_state: MarketState) -> AgentSignal:
        return AgentSignal(
            agent=self.name,
            direction="flat",
            confidence=0.0,
            invalidation_price=market_state.last_price,
            volatility_context=market_state.volatility,
        )
