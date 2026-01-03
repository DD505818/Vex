from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, JSON
from sqlalchemy.sql import func

from app.storage.db import Base


class Trade(Base):
    __tablename__ = "trades"
    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, index=True)
    side = Column(String)
    size = Column(Float)
    price = Column(Float)
    pnl = Column(Float, default=0.0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class EquitySnapshot(Base):
    __tablename__ = "equity_snapshots"
    id = Column(Integer, primary_key=True)
    equity = Column(Float)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())


class IntentRecord(Base):
    __tablename__ = "intents"
    id = Column(Integer, primary_key=True)
    symbol = Column(String)
    side = Column(String)
    expected_edge_bps = Column(Float)
    expected_hold_seconds = Column(Float)
    confidence = Column(Float)
    approved = Column(Boolean)
    reason = Column(String)
    intent_metadata = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
