"""
VEX AI ELITE — AI ROUTES

Exposes:
- GET  /ai/health
- POST /ai/chat
- WS   /ai/stream  (skeleton; can be extended to token streaming)

All endpoints are READ-ONLY.
"""

from typing import Any, Dict

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from pydantic import BaseModel

from app.ai.health import ai_health
from app.ai.chat import handle_chat

router = APIRouter(prefix="/ai", tags=["ai"])


class ChatRequest(BaseModel):
    message: str


@router.get("/health")
async def get_ai_health() -> Dict[str, Any]:
    return ai_health()


@router.post("/chat")
async def post_ai_chat(req: ChatRequest) -> Dict[str, Any]:
    # Returns { text, ui, tools, meta }
    return await handle_chat(req.message)


@router.websocket("/stream")
async def ws_ai_stream(ws: WebSocket):
    """
    Minimal WS for streaming-like UX.

    Client sends: {"message":"..."}
    Server replies: {"type":"final","payload":{...handle_chat output...}}

    Extension path:
    - Token-level streaming
    - Tool-call partial updates
    - Heartbeat + reconnect hints
    """
    await ws.accept()

    try:
        while True:
            data = await ws.receive_json()
            msg = str(data.get("message", "")).strip()
            if not msg:
                await ws.send_json({"type": "error", "error": "Empty message"})
                continue

            out = await handle_chat(msg)
            await ws.send_json({"type": "final", "payload": out})
    except WebSocketDisconnect:
        return
    except Exception as exc:
        try:
            await ws.send_json({"type": "error", "error": str(exc)})
        except Exception:
            pass
