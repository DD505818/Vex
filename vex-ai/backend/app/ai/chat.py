"""
VEX AI ELITE — AI CHAT

Lightweight chat handler that supports offline fallback and Groq.
"""

import os
from typing import Any, Dict, List, Optional

import httpx

AI_PROVIDER = os.getenv("AI_PROVIDER", "none")
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama3-70b-8192")
GROQ_ENDPOINT = os.getenv("GROQ_ENDPOINT", "https://api.groq.com/openai/v1/chat/completions")


def _format_response(text: str, provider: str, meta: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    return {
        "text": text,
        "ui": {"type": "message"},
        "tools": [],
        "meta": {"provider": provider, **(meta or {})},
    }


async def _groq_chat(message: str) -> Dict[str, Any]:
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": GROQ_MODEL,
        "messages": [{"role": "user", "content": message}],
        "temperature": 0.2,
    }
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(GROQ_ENDPOINT, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
    choices: List[Dict[str, Any]] = data.get("choices", [])
    content = ""
    if choices:
        content = choices[0].get("message", {}).get("content", "")
    return _format_response(content, "groq", {"model": GROQ_MODEL})


async def handle_chat(message: str) -> Dict[str, Any]:
    provider = (AI_PROVIDER or "none").strip().lower()
    message = message.strip()

    if provider == "none":
        return _format_response(
            f"Offline fallback: {message}",
            "none",
            {"mode": "offline_fallback"},
        )

    if provider == "groq":
        if not GROQ_API_KEY:
            return _format_response(
                "Groq provider is enabled but GROQ_API_KEY is missing.",
                "groq",
                {"error": "missing_api_key", "model": GROQ_MODEL},
            )
        try:
            return await _groq_chat(message)
        except httpx.HTTPError as exc:
            return _format_response(
                "Groq request failed.",
                "groq",
                {"error": str(exc), "model": GROQ_MODEL},
            )

    return _format_response(
        "Unknown AI_PROVIDER. Use AI_PROVIDER=none or AI_PROVIDER=groq.",
        provider,
        {"error": "unknown_provider"},
    )
