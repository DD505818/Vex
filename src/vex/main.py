from fastapi import FastAPI

from vex.control.orchestrator import Orchestrator
from vex.models.settings import AppSettings


settings = AppSettings()
app = FastAPI(title="VEX Ultimate Trading Terminal")
controller = Orchestrator(settings=settings)


@app.get("/health")
def health_check() -> dict:
    return {
        "status": "ok",
        "environment": settings.environment,
        "decision_interval_seconds": settings.decision_interval_seconds,
    }


@app.post("/cycle")
def run_cycle() -> dict:
    result = controller.run_cycle()
    return result
