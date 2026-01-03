import secrets
import time
from typing import Optional

from app.config import get_settings


class LiveGuard:
    def __init__(self):
        self.armed_until: Optional[float] = None
        self.one_time_token: Optional[str] = None
        self.settings = get_settings()

    def issue_token(self) -> str:
        self.one_time_token = secrets.token_hex(8)
        return self.one_time_token

    def confirm(self, token: str, phrase: str) -> bool:
        if token != self.one_time_token or phrase != "ARM LIVE":
            return False
        self.armed_until = time.time() + (self.settings.live_arm_duration_minutes * 60)
        self.one_time_token = None
        return True

    def is_armed(self) -> bool:
        if self.settings.trading_mode != "LIVE":
            return False
        return self.armed_until is not None and self.armed_until > time.time()
