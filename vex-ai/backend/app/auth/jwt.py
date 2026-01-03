import base64
import json
import hmac
import hashlib
from datetime import datetime, timedelta
from typing import Optional

from app.config import get_settings

settings = get_settings()


def _sign(payload: bytes) -> str:
    sig = hmac.new(settings.jwt_secret.encode(), payload, hashlib.sha256).digest()
    return base64.urlsafe_b64encode(sig).decode()


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.access_token_expire_minutes))
    to_encode.update({"exp": expire.timestamp()})
    payload = json.dumps(to_encode).encode()
    token = base64.urlsafe_b64encode(payload).decode()
    signature = _sign(payload)
    return f"{token}.{signature}"


def decode_token(token: str) -> dict:
    payload_part, signature = token.split(".")
    payload = base64.urlsafe_b64decode(payload_part.encode())
    expected_sig = _sign(payload)
    if not hmac.compare_digest(signature, expected_sig):
        raise ValueError("Invalid signature")
    data = json.loads(payload)
    if data.get("exp") and datetime.utcnow().timestamp() > data["exp"]:
        raise ValueError("Token expired")
    return data
