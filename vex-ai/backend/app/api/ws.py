import asyncio
from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.market.feed import tick_stream

router = APIRouter()


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    stream = tick_stream()
    try:
        async for tick in stream:
            await websocket.send_json(tick)
    except WebSocketDisconnect:
        pass
    except asyncio.CancelledError:
        pass
