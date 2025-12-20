from __future__ import annotations

from pydantic import BaseModel

from vex.data.market_state import MarketState
from vex.intelligence.agents import BreakoutAgent, MeanReversionAgent, MomentumAgent


class ConsensusProposal(BaseModel):
    side: str
    strength: float
    max_size: float
    ttl_seconds: int
    projected_r_multiple: float
    signals: list[dict]


class ConsensusEngine:
    def __init__(self, min_projected_r_multiple: float) -> None:
        self.min_projected_r_multiple = min_projected_r_multiple
        self.agents = [MomentumAgent(), MeanReversionAgent(), BreakoutAgent()]

    def form_consensus(self, market_state: MarketState) -> ConsensusProposal:
        signals = [agent.generate(market_state) for agent in self.agents]
        projected_r_multiple = 0.0
        strength = sum(signal.confidence for signal in signals)
        side = "flat"
        if projected_r_multiple >= self.min_projected_r_multiple:
            side = "long"
        return ConsensusProposal(
            side=side,
            strength=strength,
            max_size=0.0,
            ttl_seconds=10,
            projected_r_multiple=projected_r_multiple,
            signals=[signal.model_dump() for signal in signals],
        )
