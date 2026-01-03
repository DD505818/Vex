from fastapi import APIRouter, Depends

from app.auth.deps import require_role
from app.risk.kill_switch import KillSwitch

router = APIRouter(prefix="/risk", tags=["risk"])
kill_switch = KillSwitch()


@router.post("/kill")
async def trigger_kill(user=Depends(require_role("ADMIN"))):
    kill_switch.kill()
    return {"status": "killed"}


@router.post("/resume")
async def resume(user=Depends(require_role("ADMIN"))):
    kill_switch.resume()
    return {"status": "resumed"}
