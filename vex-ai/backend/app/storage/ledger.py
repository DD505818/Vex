import hashlib
from pathlib import Path
from typing import Dict

from app.utils.time import iso_now

LEDGER_PATH = Path("./ledger.log")


def append_entry(entry: Dict):
    LEDGER_PATH.touch(exist_ok=True)
    last_hash = ""
    if LEDGER_PATH.stat().st_size > 0:
        with LEDGER_PATH.open("rb") as f:
            *_, last_line = f.readlines()
            last_hash = last_line.decode().split("|")[-1].strip()
    payload = str(entry)
    new_hash = hashlib.sha256((payload + last_hash).encode()).hexdigest()
    with LEDGER_PATH.open("a") as f:
        f.write(f"{iso_now()}|{payload}|{new_hash}\n")
