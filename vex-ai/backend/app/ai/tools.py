"""
VEX AI ELITE — AI TOOLS (READ-ONLY)

This module defines all tools the AI layer is allowed to call.
All tools are strictly read-only and side-effect free.

Any attempt to add execution, sizing, or portfolio mutation
to this module is a critical violation.
"""

from datetime import datetime
import random
from typing import Dict, List, Optional

# In production these would be adapters to real services.
# For now they are written to be deterministic and auditable.


# =========================
# MARKET DATA TOOLS
# =========================

def get_quote(symbol: str) -> Dict:
    """
    Return a lightweight quote snapshot for an asset.
    """
    symbol = symbol.upper().strip()

    # Placeholder deterministic mock (replace with real feed adapter)
    price = round(100 + random.uniform(-5, 5), 2)
    change = round(random.uniform(-2, 2), 2)

    return {
        "symbol": symbol,
        "price": price,
        "change_pct": change,
        "timestamp": datetime.utcnow().isoformat(),
    }


def get_ohlc(symbol: str, timeframe: str) -> Dict:
    """
    Return OHLC data summary for visualization.
    Timeframe is sanitized upstream via schema.
    """
    symbol = symbol.upper().strip()

    # Minimal OHLC structure for charting
    candles = []
    base_price = 100.0

    for i in range(50):
        open_p = base_price + random.uniform(-1, 1)
        close_p = open_p + random.uniform(-1, 1)
        high_p = max(open_p, close_p) + random.uniform(0, 0.5)
        low_p = min(open_p, close_p) - random.uniform(0, 0.5)

        candles.append(
            {
                "t": i,
                "o": round(open_p, 2),
                "h": round(high_p, 2),
                "l": round(low_p, 2),
                "c": round(close_p, 2),
            }
        )

        base_price = close_p

    return {
        "symbol": symbol,
        "timeframe": timeframe,
        "candles": candles,
    }


# =========================
# NEWS TOOL
# =========================

def get_news(symbol: Optional[str] = None, limit: int = 5) -> List[Dict]:
    """
    Return recent news headlines.
    """
    headlines = []

    for i in range(limit):
        headlines.append(
            {
                "headline": f"Market update {i + 1}",
                "symbol": symbol,
                "source": "MockNews",
                "timestamp": datetime.utcnow().isoformat(),
            }
        )

    return headlines


# =========================
# METRIC EXPLANATION TOOL
# =========================

def explain_metric(metric: str) -> Dict:
    """
    Return an explanation of a common market metric.
    """
    metric = metric.upper().strip()

    explanations = {
        "ATR": (
            "Average True Range measures volatility by capturing the average range "
            "of price movement."
        ),
        "VWAP": "Volume Weighted Average Price reflects the average price weighted by volume.",
        "RSI": (
            "Relative Strength Index measures momentum and potential overbought or oversold "
            "conditions."
        ),
        "VOLATILITY": "Volatility represents the magnitude of price fluctuations over time.",
    }

    return {
        "metric": metric,
        "description": explanations.get(metric, "Metric explanation not available."),
    }


# =========================
# UI INTENT HELPERS
# =========================

def render_chart_intent(symbol: str, interval: str) -> Dict:
    """
    Generate a UI intent instructing the frontend to render a chart.
    """
    return {
        "type": "chart",
        "symbol": symbol.upper().strip(),
        "interval": interval,
    }


def render_news_intent(symbol: Optional[str], limit: int = 5) -> Dict:
    """
    Generate a UI intent for a news panel.
    """
    return {
        "type": "news",
        "symbol": symbol.upper().strip() if symbol else None,
        "limit": limit,
    }


def render_metrics_intent(items: List[str]) -> Dict:
    """
    Generate a UI intent for metric cards.
    """
    return {
        "type": "metrics",
        "items": [item.upper().strip() for item in items],
    }
