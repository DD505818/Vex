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
        directional_signals = [signal for signal in signals if signal.direction != "flat"]
        long_votes = [signal for signal in directional_signals if signal.direction == "long"]
        short_votes = [signal for signal in directional_signals if signal.direction == "short"]
        side = "flat"
        winning_votes = []
        if len(long_votes) > len(short_votes):
            side = "long"
            winning_votes = long_votes
        elif len(short_votes) > len(long_votes):
            side = "short"
            winning_votes = short_votes
        strength = 0.0
        projected_r_multiple = 0.0
        if winning_votes:
            strength = sum(signal.confidence for signal in winning_votes) / len(winning_votes)
            projected_r_multiple = round(strength * 10, 2)
            if projected_r_multiple < self.min_projected_r_multiple:
                side = "flat"
        return ConsensusProposal(
            side=side,
            strength=strength,
            max_size=round(strength * 100, 2),
            ttl_seconds=10,
            projected_r_multiple=projected_r_multiple,
            signals=[signal.model_dump() for signal in signals],
        )
