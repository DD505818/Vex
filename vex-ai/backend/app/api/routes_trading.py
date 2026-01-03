from fastapi import APIRouter, Depends, HTTPException

from app.auth.deps import require_role
from app.execution.router import ExecutionRouter
from app.engine.intents import TradeIntent
from app.risk.cost_engine import CostEngine
from app.risk.risk_engine import RiskEngine

router = APIRouter(prefix="/trading", tags=["trading"])


router_extra = {
    "exec_router": ExecutionRouter,
    "cost_engine": CostEngine,
    "risk_engine": RiskEngine,
}


def get_exec_router() -> ExecutionRouter:
    return router_extra["exec_router"]


def get_cost_engine() -> CostEngine:
    return router_extra["cost_engine"]


def get_risk_engine() -> RiskEngine:
    return router_extra["risk_engine"]


@router.post("/intent")
async def submit_intent(
    intent: TradeIntent,
    router_exec: ExecutionRouter = Depends(get_exec_router),
    cost_engine: CostEngine = Depends(get_cost_engine),
    risk_engine: RiskEngine = Depends(get_risk_engine),
    user=Depends(require_role("TRADER")),
):
    cost = cost_engine.estimate(intent, {"spread": 0.01, "volatility": 1, "latency": 10})
    assessment = risk_engine.assess(intent, cost)
    if not assessment.approved:
        raise HTTPException(status_code=400, detail=assessment.reason)
    result = await router_exec.route(intent, cost)
    risk_engine.record_fill(intent, result)
    return {"result": result, "net_edge_bps": assessment.net_edge_bps}
