from __future__ import annotations

from pydantic import BaseModel

from vex.intelligence.consensus import ConsensusProposal


class RiskQualification(BaseModel):
    is_approved: bool
    reason: str
    max_risk_per_trade: float
    projected_r_multiple: float
    side: str


class RiskEngine:
    def __init__(self, max_risk_per_trade: float, min_projected_r_multiple: float) -> None:
        self.max_risk_per_trade = max_risk_per_trade
        self.min_projected_r_multiple = min_projected_r_multiple

    def qualify(self, proposal: ConsensusProposal) -> RiskQualification:
        if proposal.projected_r_multiple < self.min_projected_r_multiple:
            return RiskQualification(
                is_approved=False,
                reason="Projected R multiple below minimum threshold.",
                max_risk_per_trade=self.max_risk_per_trade,
                projected_r_multiple=proposal.projected_r_multiple,
                side=proposal.side,
            )
        return RiskQualification(
            is_approved=True,
            reason="Approved by deterministic risk checks.",
            max_risk_per_trade=self.max_risk_per_trade,
            projected_r_multiple=proposal.projected_r_multiple,
            side=proposal.side,
        )
