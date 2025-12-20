from collections import deque
from dataclasses import dataclass, field

from .models import ConsensusResponse, Signal


@dataclass
class InMemoryState:
    signals: deque[Signal] = field(default_factory=lambda: deque(maxlen=100))
    last_consensus: ConsensusResponse | None = None

    def add_signal(self, signal: Signal) -> None:
        self.signals.append(signal)

    def list_signals(self) -> list[Signal]:
        return list(self.signals)

    def update_consensus(self, consensus: ConsensusResponse) -> None:
        self.last_consensus = consensus
