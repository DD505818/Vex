from fastapi import APIRouter

router = APIRouter(prefix="/portfolio", tags=["portfolio"])


@router.get("/")
async def portfolio_state():
    return {"equity": 100000, "positions": []}
