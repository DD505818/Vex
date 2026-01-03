import asyncio
from app.main import health


def test_health():
    resp = asyncio.get_event_loop().run_until_complete(health())
    assert resp["status"] == "ok"
