from fastapi import APIRouter, Depends, HTTPException

from app.auth.deps import require_role
from app.execution.live_guard import LiveGuard
from app.engine.engine import Engine


router = APIRouter(prefix="/system", tags=["system"])


class EngineWrapper:
    engine: Engine = None


def get_engine_wrapper():
    return EngineWrapper


def get_live_guard() -> LiveGuard:
    if not hasattr(router, "extra"):
        router.extra = {}
    guard = router.extra.get("live_guard")
    if guard is None:
        guard = LiveGuard()
        router.extra["live_guard"] = guard
    return guard


@router.post("/start")
async def start_engine(wrapper=Depends(get_engine_wrapper), user=Depends(require_role("TRADER"))):
    if wrapper.engine:
        await wrapper.engine.start()
    return {"status": "started"}


@router.post("/stop")
async def stop_engine(wrapper=Depends(get_engine_wrapper), user=Depends(require_role("TRADER"))):
    if wrapper.engine:
        await wrapper.engine.stop()
    return {"status": "stopped"}


@router.get("/status")
async def status(wrapper=Depends(get_engine_wrapper)):
    return {"running": bool(wrapper.engine and wrapper.engine.running)}


@router.post("/arm-live")
async def arm_live(user=Depends(require_role("ADMIN")), guard: LiveGuard = Depends(get_live_guard)):
    return {"token": guard.issue_token()}


@router.post("/confirm-live")
async def confirm_live(payload: dict, user=Depends(require_role("ADMIN")), guard: LiveGuard = Depends(get_live_guard)):
    token = payload.get("token")
    phrase = payload.get("phrase")
    if not guard.confirm(token, phrase):
        raise HTTPException(status_code=400, detail="Invalid confirmation")
    return {"status": "armed"}
