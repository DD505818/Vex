import asyncio
import random
from typing import List

from app.engine.intents import TradeIntent
from app.engine.ranking import rank_intents
from app.execution.router import ExecutionRouter
from app.market.feed import tick_stream
from app.risk.cost_engine import CostEngine
from app.risk.risk_engine import RiskEngine
from app.storage.ledger import append_entry


class Engine:
    def __init__(self, router: ExecutionRouter, cost_engine: CostEngine, risk_engine: RiskEngine):
        self.router = router
        self.cost_engine = cost_engine
        self.risk_engine = risk_engine
        self.running = False
        self.broadcast_callbacks: List = []

    async def start(self):
        self.running = True
        asyncio.create_task(self._run())

    async def stop(self):
        self.running = False

    async def _run(self):
        async for tick in tick_stream():
            if not self.running:
                break
            intents = self._generate_intents(tick)
            costs = [self.cost_engine.estimate(intent, tick) for intent in intents]
            ranked = rank_intents(intents, costs)
            for _, intent, cost in ranked:
                assessment = self.risk_engine.assess(intent, cost)
                if assessment.approved:
                    result = await self.router.route(intent, cost)
                    self.risk_engine.record_fill(intent, result)
                    append_entry({"intent": intent.model_dump(), "cost": cost.model_dump(), "result": result})
                    await self._broadcast({"intent": intent.model_dump(), "cost": cost.model_dump(), "result": result})
            await asyncio.sleep(0)

    def _generate_intents(self, tick) -> List[TradeIntent]:
        direction = random.choice(["BUY", "SELL"])
        price = tick["price"]
        edge = random.uniform(5, 50)
        hold = random.uniform(10, 120)
        tp = price * (1.01 if direction == "BUY" else 0.99)
        stop = price * (0.99 if direction == "BUY" else 1.01)
        intent = TradeIntent(
            symbol=tick["symbol"],
            side=direction,
            entry=price,
            stop=stop,
            take_profit=tp,
            expected_edge_bps=edge,
            expected_hold_seconds=hold,
            confidence=random.uniform(0.3, 0.9),
            strategy="random",
        )
        return [intent]

    async def _broadcast(self, payload):
        for cb in self.broadcast_callbacks:
            await cb(payload)

    def register_callback(self, cb):
        self.broadcast_callbacks.append(cb)
