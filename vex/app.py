from fastapi import FastAPI

from .config import Settings
from .consensus import form_consensus
from .models import (
    ConsensusRequest,
    ConsensusResponse,
    RiskQualificationRequest,
    RiskQualificationResponse,
    Signal,
)
from .risk import qualify_trade
from .state import InMemoryState

settings = Settings()
state = InMemoryState()

app = FastAPI(title=settings.app_name)


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok", "service": settings.app_name}


@app.post("/signals", response_model=list[Signal])
def ingest_signal(signal: Signal) -> list[Signal]:
    state.add_signal(signal)
    return state.list_signals()


@app.get("/state", response_model=list[Signal])
def list_signals() -> list[Signal]:
    return state.list_signals()


@app.post("/consensus", response_model=ConsensusResponse)
def consensus(request: ConsensusRequest) -> ConsensusResponse:
    consensus_result = form_consensus(request)
    state.update_consensus(consensus_result)
    return consensus_result


@app.post("/risk/qualify", response_model=RiskQualificationResponse)
def risk_qualify(request: RiskQualificationRequest) -> RiskQualificationResponse:
    return qualify_trade(request)
