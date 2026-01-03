import pytest
from app.execution.live_guard import LiveGuard
from app.config import Settings


def test_live_guard_flow(monkeypatch):
    # force live mode
    monkeypatch.setenv("TRADING_MODE", "LIVE")
    guard = LiveGuard()
    token = guard.issue_token()
    assert guard.is_armed() is False
    assert guard.confirm(token, "ARM LIVE") is True
    assert guard.is_armed() is True


def test_guard_rejects_wrong_token(monkeypatch):
    monkeypatch.setenv("TRADING_MODE", "LIVE")
    guard = LiveGuard()
    guard.issue_token()
    assert guard.confirm("bad", "ARM LIVE") is False
