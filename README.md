# VEX Ultimate Trading Terminal

## Master PRD & Operational Specification

**Version:** Final  
**Audience:** Independent operator seeking institutional-grade execution, governance, and risk standards  
**Objective:** Design, deploy, and operate a high-survivability, high risk–adjusted return trading system optimized for short-horizon compounding, enforced through deterministic risk controls, rigorous process discipline, explicit failure handling, and full end-to-end observability.

---

## 1. Foundational Philosophy

VEX Ultimate is architected under the explicit premise that capital preservation is the dominant constraint governing long-term profitability. Rather than treating risk as a secondary consideration or a tunable parameter, the system elevates risk management to the role of the primary organizing principle around which all other components are structured. Profit generation is therefore modeled as a conditional and emergent outcome that materializes only when risk remains continuously bounded across time, market regimes, and operational states.

The system is intentionally constructed as a *risk-first capital management framework*. Every downstream decision—signal generation, position sizing, execution timing, trade management, and capital scaling—is subordinated to survivability. This design reflects the empirical reality observed across discretionary and systematic trading: most systems fail not because their signals lack theoretical merit, but because variance is mismanaged, losses compound faster than gains, or regimes shift faster than strategies adapt.

VEX Ultimate assumes that markets are adversarial, infrastructure is imperfect, and models are fallible. Accordingly, the design explicitly assumes the persistent presence of:

* Exchange microstructure instability, liquidity fragmentation, slippage, and intermittent venue outages
* API latency, partial failures, throttling, dropped messages, and stale or inconsistent data conditions
* Volatility regime shifts, structural breaks, and non-stationary price dynamics
* Strategy decay, signal invalidation, crowding effects, and transient loss of statistical edge

From these assumptions emerge the system’s governing axioms:

* No individual trade, signal, or market opportunity justifies irreversible capital impairment
* Risk constraints must be mechanically enforced rather than discretionarily applied or overridden
* Alpha signals are probabilistic hypotheses, not execution commands
* Positive expectancy requires asymmetric payoff distributions
* End-to-end system observability is a prerequisite for live operation, not a post hoc diagnostic convenience

---

## 2. System Architecture Overview

VEX Ultimate is decomposed into three tightly scoped, functionally isolated planes: control, data, and intelligence. Each plane is independently observable, explicitly stateful, and designed to fail safely without propagating undefined behavior or cascading errors across the system. No single subsystem possesses unilateral authority over capital deployment.

This separation of concerns ensures that analytical insight, execution authority, and risk governance remain distinct and independently auditable.

### 2.1 Control Plane

The control plane governs orchestration, execution authority, configuration, and state coordination across all runtime components:

* **FastAPI** provides deterministic REST and WebSocket interfaces for orchestration, supervision, configuration management, and external control
* **Redis** functions as the low-latency state layer supporting distributed locks, kill-switch enforcement, signal consensus tracking, throttling controls, and ephemeral runtime state
* **PostgreSQL** serves as the immutable system of record for trades, positions, equity states, configuration changes, and risk events

The control plane prioritizes correctness, determinism, and recoverability over raw throughput or architectural novelty.

### 2.2 Data Plane

The data plane is optimized for timeliness, internal consistency, and forensic replay. Every decision made by the system must be reconstructible after the fact:

* **CCXT** provides a unified abstraction over heterogeneous exchange APIs, symbol conventions, and market structures
* WebSocket ingestion supports OHLCV, trades, and order book snapshots where available
* Deterministic snapshot caching enables reproducible decision cycles, post-incident analysis, and historical replay

All incoming data is treated as potentially faulty until validated and time-aligned.

### 2.3 Intelligence Plane

Signal generation is performed by multiple independently designed agents, each targeting a distinct market inefficiency and operating under explicitly bounded assumptions:

* Momentum continuation agent
* Mean reversion agent
* Breakout expansion agent
* Volatility and regime classification agent

Each agent emits a normalized signal of the form:

```
{ direction, confidence, invalidation, volatility }
```

Agents possess no execution authority. Their outputs are advisory inputs subject to consensus formation and risk enforcement.

---

## 3. Full Trade Logic (Authoritative Specification)

This section defines the complete and deterministic trade decision lifecycle from market observation through position closure. No trade may be executed outside this sequence, and every stage is explicitly gatekept.

### 3.1 Market State Construction

At each decision interval, the system constructs a unified market state consisting of:

* Multi-timeframe OHLCV data (execution frame, context frame, higher-timeframe bias)
* Realized and proxy implied volatility estimates
* Session range, VWAP, value area, and recent liquidity conditions
* Regime classification (trend, range, expansion, contraction)

All indicators are derived exclusively from raw price and volume. No external forecasts, sentiment feeds, or discretionary inputs are consumed.

---

### 3.2 Strategy-Specific Signal Logic

#### Momentum Continuation Agent

**Objective:** Participate in established directional trends while extracting asymmetric payoff relative to defined risk.

Conditions:

* Alignment between execution and higher-timeframe trend structure
* Sustained price acceptance above or below VWAP or regime midpoint
* Volatility above minimum participation threshold
* Projected reward-to-risk ratio ≥ 5R based on structural targets

Invalidation:

* Structural break of the trend reference level
* Volatility compression or momentum divergence

---

#### Mean Reversion Agent

**Objective:** Capture statistically bounded reversion opportunities with convex payoff profiles.

Conditions:

* Range-bound regime classification
* Price deviation beyond a dynamic volatility-adjusted band
* Evidence of liquidity absorption, exhaustion, or failed continuation
* Distance to mean target ≥ 5× defined stop distance

Invalidation:

* Range expansion or confirmed regime transition
* Failure to revert within a predefined temporal window

---

#### Breakout Expansion Agent

**Objective:** Capture volatility expansion events with outsized reward relative to initial risk.

Conditions:

* Measurable volatility contraction and price compression
* Range resolution accompanied by volume confirmation
* Alignment with higher-timeframe directional context
* Measured expansion target ≥ 5R from entry

Invalidation:

* False breakout with immediate rejection
* Volume divergence or rapid mean reversion

---

### 3.3 Signal Normalization

Each agent outputs a standardized signal object:

```
{ direction, confidence ∈ [0,1], invalidation_price, volatility_context }
```

Confidence scores are internally calibrated to ensure comparability across agents and regimes.

---

### 3.4 Consensus Formation

Signals are aggregated using a weighted voting mechanism:

* Minimum directional quorum across agents
* Regime compatibility enforced
* Volatility-adjusted confidence threshold
* Mandatory projected reward-to-risk ≥ 5R

The consensus engine outputs a constrained execution proposal:

```
{ side, strength, max_size, ttl, projected_R }
```

Trades failing to meet the minimum +5R criterion are rejected regardless of signal strength.

---

### 3.5 Pre-Trade Risk Qualification

Before any order is generated, the risk engine verifies:

* Trade-level risk does not exceed the per-trade capital limit
* Portfolio exposure remains within predefined bounds
* Current drawdown state permits incremental risk
* Projected reward-to-risk ratio ≥ 5R after fees and slippage assumptions

Failure at any checkpoint aborts the trade.

---

### 3.6 Position Sizing

Position size is computed deterministically as:

```
size = min(
  risk_budget / stop_distance,
  consensus.max_size,
  portfolio_exposure_cap
)
```

Sizing is volatility-adjusted, invariant to discretionary intervention, and bounded by the +5R constraint.

---

### 3.7 Order Execution

* Post-only limit orders are attempted first to reduce adverse selection
* Fallback to aggressive orders occurs only when necessary
* Partial fills are tracked explicitly and reconciled deterministically

All orders include:

* A predefined stop-loss
* One or more profit targets structured to preserve ≥ 5R expectancy

---

### 3.8 Trade Management

While a position is active:

* Stops may trail only in the direction of profit
* Risk exposure may be reduced, never increased
* Partial profit-taking must not reduce remaining trade expectancy below +5R at inception
* Regime shifts trigger de-risking or forced exit

---

### 3.9 Exit Logic

Positions are closed upon:

* Stop-loss execution
* Final profit target achievement
* Signal invalidation
* Regime transition
* System kill-switch activation

---

## 4. Risk Management Engine (Deterministic Enforcement)

Risk management supersedes all signal generation and execution logic:

* Fixed fractional risk per trade
* Rolling VaR estimation at 95% and 99%
* Drawdown-based throttling and de-risking
* Hard kill-switch enforcement
* Enforcement of minimum +5R projected payoff on all initiated trades

---

## 5. Execution Engine

* Exchange-aware routing and order type selection
* Deterministic order lifecycle management
* Retry with bounded exponential backoff
* Immutable execution and fill logs

---

## 6. Terminal Interface and UX

* Multi-asset, multi-timeframe charts
* Live positions with SL/TP overlays and projected R-multiple display
* Risk dashboard and append-only trade blotter
* API health, latency, and system telemetry

---

## 7. Observability and Logging

* Structured, machine-parsable logs
* End-to-end trade lifecycle tracing
* Latency, error, and performance metrics
* Realized vs projected R-multiple attribution

---

## 8. Deployment Architecture

* Docker Compose for local and staging environments
* Ubuntu Server LTS for production deployment
* systemd-managed services with Nginx reverse proxy

---

## 9. CI/CD and Validation

Validation is treated as a continuous process rather than a one-time gate. The system is expected to demonstrate robustness across synthetic, historical, and live-simulated conditions prior to capital scaling.

Validation layers include:

* Static analysis and deterministic unit tests for all core components
* Historical backtesting emphasizing R-multiple distributions and tail behavior
* Paper trading in live market conditions to validate execution quality and realized R outcomes
* Ongoing forward performance monitoring to detect degradation or erosion of the +5R profile

No system transition to higher capital allocation occurs without successful validation at each preceding layer.

---

## 10. Capital Scaling Protocol

Capital scaling follows a strictly conditional and non-linear trajectory:

* Initial deployment at minimal capital to validate live +5R realization
* Gradual scaling only after statistically meaningful positive expectancy at ≥ 5R
* Logarithmic position size increases to control variance
* Immediate scale-down upon deviation from expected R-multiple distributions

Discretionary overrides are explicitly prohibited.

---

## 11. Projected Performance Trajectories (Non-Guaranteed)

The system’s expected behavior is best described in terms of possible trajectories rather than point forecasts:

* **Base Case:** Lower trade frequency with consistent positive expectancy driven by +5R asymmetry and strict selectivity
* **Upside Case:** Accelerated compounding during extended directional or volatility expansion regimes where +5R targets are frequently achieved
* **Adverse Case:** Extended flat or mildly negative periods characterized by trade abstention and capital preservation

These trajectories are probabilistic and conditional. They are not guarantees and are expected to vary across assets, venues, and time periods.

---

## 12. Closing Statement

VEX Ultimate is engineered for persistence under uncertainty through enforced asymmetry.

Persistence—and asymmetric payoff, not prediction—is the true compounding mechanism.
