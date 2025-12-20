from .models import RiskQualificationRequest, RiskQualificationResponse


def qualify_trade(request: RiskQualificationRequest) -> RiskQualificationResponse:
    reasons: list[str] = []

    if request.projected_r < request.limits.min_projected_r:
        reasons.append("Projected R below minimum requirement.")

    if request.risk_amount / request.state.equity > request.limits.per_trade_risk:
        reasons.append("Per-trade risk exceeds limit.")

    if request.state.portfolio_risk > request.limits.max_portfolio_risk:
        reasons.append("Portfolio risk exceeds limit.")

    if request.state.current_drawdown > request.limits.max_drawdown:
        reasons.append("Current drawdown exceeds limit.")

    return RiskQualificationResponse(approved=not reasons, reasons=reasons)
