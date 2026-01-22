from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import routes_portfolio, routes_risk, routes_system, routes_trading, ws
from app.config import get_settings
from app.engine.engine import Engine
from app.execution.live_guard import LiveGuard
from app.execution.router import ExecutionRouter
from app.risk.cost_engine import CostEngine
from app.risk.limits import RiskLimits
from app.risk.risk_engine import RiskEngine
from app.utils.logging import setup_logging


logger = setup_logging()
live_guard = LiveGuard()
cost_engine = CostEngine()
risk_engine = RiskEngine(RiskLimits())
execution_router = ExecutionRouter(live_guard)
engine = Engine(execution_router, cost_engine, risk_engine)
routes_system.EngineWrapper.engine = engine
if not hasattr(routes_system.router, "extra"):
    routes_system.router.extra = {}
routes_system.router.extra["live_guard"] = live_guard
routes_trading.router_extra.update(
    {
        "exec_router": execution_router,
        "cost_engine": cost_engine,
        "risk_engine": risk_engine,
    }
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await engine.stop()


app = FastAPI(title="VEX AI ELITE", lifespan=lifespan)
settings = get_settings()
allowed_origins = settings.allowed_origins
allow_credentials = "*" not in allowed_origins
if "*" in allowed_origins:
    allowed_origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=allow_credentials,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(routes_system.router)
app.include_router(routes_trading.router)
app.include_router(routes_portfolio.router)
app.include_router(routes_risk.router)
app.include_router(ws.router)


@app.get("/health")
async def health():
    return {"status": "ok"}
