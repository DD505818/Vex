# VEX AI ELITE Backend

## Running locally

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Risk + Live Guard Highlights
- Risk engine enforces edge-over-cost, min R, drawdown caps, exposure per symbol, and open position limits using a shared `PortfolioState`.
- Successful routes update portfolio equity/positions to keep risk accounting in sync.
- Live trading remains locked behind `TRADING_MODE=LIVE` plus `/system/arm-live` token and `/system/confirm-live` phrase.
