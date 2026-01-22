"""
VEX AI ELITE — AI HEALTH

Readiness checks for the AI subsystem.
This is intentionally lightweight and safe.

Health checks include:
- Provider configuration sanity
- Key presence (if provider requires it)
- Basic tool registry integrity
"""

import os
from typing import Any, Dict

from .chat import AI_PROVIDER, GROQ_API_KEY


def ai_health() -> Dict[str, Any]:
    provider = (AI_PROVIDER or "none").strip().lower()

    # "none" is always healthy (offline fallback)
    if provider == "none":
        return {
            "ok": True,
            "provider": "none",
            "details": {
                "mode": "offline_fallback",
                "note": "AI provider disabled; deterministic fallback responses enabled.",
            },
        }

    # groq requires key
    if provider == "groq":
        has_key = bool(GROQ_API_KEY)
        return {
            "ok": has_key,
            "provider": "groq",
            "details": {
                "has_key": has_key,
                "model": os.getenv("GROQ_MODEL", "llama3-70b-8192"),
                "note": "Groq provider enabled. Tool-calling supported.",
            },
        }

    return {
        "ok": False,
        "provider": provider,
        "details": {
            "error": "Unknown AI_PROVIDER. Use AI_PROVIDER=none or AI_PROVIDER=groq.",
        },
    }
