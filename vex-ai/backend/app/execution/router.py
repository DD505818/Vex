from fastapi import HTTPException, status

from app.config import get_settings
from app.execution.live_guard import LiveGuard
from app.execution.paper_broker import PaperBroker
from app.risk.cost_engine import CostBreakdown
from app.engine.intents import TradeIntent


class ExecutionRouter:
    def __init__(self, live_guard: LiveGuard):
        self.settings = get_settings()
        self.live_guard = live_guard
        self.paper_broker = PaperBroker()

    async def route(self, intent: TradeIntent, cost: CostBreakdown):
        if self.settings.trading_mode == "LIVE":
            if not self.live_guard.is_armed():
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Live trading not armed")
            return {"status": "live_stub", "detail": "Live routing not implemented"}
        return await self.paper_broker.execute(intent, cost)
