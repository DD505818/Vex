from dataclasses import dataclass

from .models import ConsensusRequest, ConsensusResponse, Direction, Signal


@dataclass
class ConsensusTotals:
    long_weight: float = 0
    short_weight: float = 0


def _count_direction(signals: list[Signal]) -> ConsensusTotals:
    totals = ConsensusTotals()
    for signal in signals:
        weighted = signal.confidence * signal.weight
        if signal.direction == Direction.long:
            totals.long_weight += weighted
        elif signal.direction == Direction.short:
            totals.short_weight += weighted
    return totals


def form_consensus(request: ConsensusRequest) -> ConsensusResponse:
    if len(request.signals) < request.min_quorum:
        return ConsensusResponse(
            side=Direction.flat, strength=0, max_size=0, ttl_seconds=0, projected_r=0
        )

    totals = _count_direction(request.signals)
    total_weight = totals.long_weight + totals.short_weight
    if total_weight == 0:
        return ConsensusResponse(
            side=Direction.flat, strength=0, max_size=0, ttl_seconds=0, projected_r=0
        )

    side = Direction.long if totals.long_weight >= totals.short_weight else Direction.short
    winning_weight = max(totals.long_weight, totals.short_weight)
    strength = winning_weight / total_weight

    if strength < request.confidence_threshold:
        return ConsensusResponse(
            side=Direction.flat, strength=strength, max_size=0, ttl_seconds=0, projected_r=0
        )

    projected_r = max(request.min_projected_r, request.min_projected_r * strength)
    max_size = strength

    return ConsensusResponse(
        side=side, strength=strength, max_size=max_size, ttl_seconds=30, projected_r=projected_r
    )
