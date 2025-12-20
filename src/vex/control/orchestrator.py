from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone

from vex.data.market_state import MarketStateBuilder
from vex.execution.engine import ExecutionEngine
from vex.intelligence.consensus import ConsensusEngine
from vex.models.settings import AppSettings
from vex.risk.engine import RiskEngine


@dataclass
class Orchestrator:
    settings: AppSettings

    def __post_init__(self) -> None:
        self.market_state_builder = MarketStateBuilder()
        self.consensus_engine = ConsensusEngine(
            min_projected_r_multiple=self.settings.min_projected_r_multiple
        )
        self.risk_engine = RiskEngine(
            max_risk_per_trade=self.settings.max_risk_per_trade,
            min_projected_r_multiple=self.settings.min_projected_r_multiple,
        )
        self.execution_engine = ExecutionEngine()

    def run_cycle(self) -> dict:
        timestamp = datetime.now(timezone.utc).isoformat()
        market_state = self.market_state_builder.build()
        consensus = self.consensus_engine.form_consensus(market_state)
        qualification = self.risk_engine.qualify(consensus)
        execution = None
        if qualification.is_approved:
            execution = self.execution_engine.prepare_order(qualification)
        return {
            "timestamp": timestamp,
            "market_state": market_state.model_dump(),
            "consensus": consensus.model_dump(),
            "qualification": qualification.model_dump(),
            "execution": execution.model_dump() if execution else None,
        }
