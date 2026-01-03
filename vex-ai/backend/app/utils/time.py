import time
from datetime import datetime


def now_ts() -> float:
    return time.time()


def iso_now() -> str:
    return datetime.utcnow().isoformat() + "Z"
