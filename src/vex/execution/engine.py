from __future__ import annotations

from pydantic import BaseModel

from vex.risk.engine import RiskQualification


class ExecutionPlan(BaseModel):
    side: str
    size: float
    order_type: str
    stop_loss: float | None
    take_profit: float | None


class ExecutionEngine:
    def prepare_order(self, qualification: RiskQualification) -> ExecutionPlan:
        return ExecutionPlan(
            side=qualification.side,
            size=0.0,
            order_type="post_only_limit",
            stop_loss=None,
            take_profit=None,
        )
