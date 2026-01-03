import asyncio
import random
from typing import AsyncIterator, Dict

from app.market.symbols import SYMBOLS


async def tick_stream() -> AsyncIterator[Dict]:
    prices = {s: 100.0 + i * 10 for i, s in enumerate(SYMBOLS)}
    while True:
        for symbol in SYMBOLS:
            drift = random.uniform(-0.5, 0.5)
            spread = random.uniform(0.01, 0.05)
            vol = random.uniform(0.5, 2.0)
            latency = random.uniform(5, 50)
            prices[symbol] = max(1.0, prices[symbol] + drift)
            yield {
                "symbol": symbol,
                "price": round(prices[symbol], 2),
                "volume": random.uniform(10, 1000),
                "spread": round(spread, 4),
                "volatility": vol,
                "latency": latency,
            }
            await asyncio.sleep(0.25)
