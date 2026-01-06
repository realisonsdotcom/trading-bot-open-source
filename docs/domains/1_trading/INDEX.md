---
domain: 1_trading
title: Trading & Strategies Domain Index
description: Trading strategies, algo engine, market data, screening, and live trading documentation
keywords: trading, strategies, algo-engine, backtesting, market-data, screening, inplay
last_updated: 2026-01-06
---

# 📊 Trading & Strategies Domain

> **Domain**: Trading strategy development, backtesting, execution, market data, and live monitoring

---

## 📑 Domain Overview

This domain covers all aspects of trading strategy development, execution, and monitoring:

- **Strategy Development**: Algorithm design, backtesting, and optimization
- **Execution Engine**: Strategy registry, plugin system, and signal generation
- **Market Data**: Real-time and historical data ingestion from multiple providers
- **Opportunity Detection**: Market scanning and screening capabilities
- **Live Monitoring**: Real-time tracking of active strategies and setups

---

## 📚 Core Documentation

### Strategy Execution

- **[Algo Engine Service](algo-engine.md)** ⭐
  - Strategy execution engine with plugin-based extensible registry
  - Visual designer, AI assistant, backtesting capabilities
  - Keywords: `algo-engine`, `strategies`, `plugins`, `backtesting`, `AI-assistant`

- **[Algo ↔ Order Router Contract](algo-order-contract.md)** ⭐
  - Strategy-order integration specification
  - REST API contract between algo engine and order router
  - Keywords: `algo-order`, `contract`, `integration`, `order-router`

- **[Strategies Documentation](strategies/README.md)**
  - Strategy development guides and examples
  - Plugin creation tutorials
  - Keywords: `strategy-development`, `plugins`, `examples`

### Market Data & Analysis

- **[Market Data Service](market-data.md)** ⭐
  - Real-time and historical market data ingestion
  - Data normalization and persistence
  - Multi-provider adapter system
  - Keywords: `market-data`, `real-time`, `historical`, `adapters`

- **[Screener Service](screener.md)** ⭐
  - Market scanning and opportunity detection
  - Third-party provider integration (Financial Modeling Prep)
  - Custom preset management
  - Keywords: `screener`, `market-scanning`, `filters`, `presets`

### Live Trading

- **[InPlay Monitoring Service](inplay.md)** ⭐
  - Real-time monitoring UI and WebSocket feed
  - Live setup detection and tracking
  - Dashboard integration
  - Keywords: `inplay`, `real-time`, `monitoring`, `websocket`, `setups`

---

## 🎯 Quick Start

### Running the Algo Engine

```bash
# Start the demo environment
make demo-up

# Access algo engine API
curl http://localhost:8020/strategies

# Import a strategy
curl -X POST http://localhost:8020/strategies/import \
  -H "Content-Type: application/json" \
  -d '{"strategy_key": "orb_strategy"}'
```

### Running a Screener

```bash
# Execute a screener
curl "http://localhost:8030/screener/run?preset=momentum"

# List available presets
curl http://localhost:8030/screener/presets
```

### Monitoring InPlay Setups

```bash
# Connect to WebSocket feed
wscat -c ws://localhost:8040/ws/inplay

# Or access via dashboard
open http://localhost:3000/dashboard
```

---

## 🔗 Related Domains

- **[2_architecture](../2_architecture/INDEX.md)** - Order Router, Streaming Service integration
- **[3_operations](../3_operations/INDEX.md)** - Deployment and monitoring setup
- **[6_quality](../6_quality/INDEX.md)** - Testing strategies and quality assurance

---

## 🛠️ Feature Status

| Feature | Status | Prerequisites |
|---------|--------|---------------|
| **Strategy Registry** | ✅ Delivered | `/strategies` endpoint available |
| **AI Assistant** | 🟡 Beta opt-in | `pip install -r services/algo_engine/requirements.txt`, `OPENAI_API_KEY` |
| **Backtesting** | ✅ Delivered | `data/backtests/` writable directory |
| **Visual Designer** | 🟡 Beta | `web-dashboard` service running |
| **Market Data Ingestion** | ✅ Delivered | Provider credentials configured |
| **Screener API** | ✅ Delivered | Financial Modeling Prep API key |
| **InPlay Monitoring** | ✅ Delivered | `INPLAY_SERVICE_TOKEN` configured |

---

## 📋 Documentation Gaps

### High Priority

- [ ] **Strategy Backtesting Guide** - Comprehensive backtesting tutorial
- [ ] **Market Connector Comparison** - Exchange capabilities matrix
- [ ] **Strategy Performance Metrics** - KPI definitions and tracking

### Medium Priority

- [ ] **Strategy Optimization Guide** - Parameter tuning best practices
- [ ] **Risk Management Integration** - Position sizing and limits
- [ ] **Data Provider Setup** - Multi-provider configuration guide

### Low Priority

- [ ] **Advanced Strategy Patterns** - Complex strategy examples
- [ ] **Custom Indicator Development** - Building custom technical indicators
- [ ] **Strategy Versioning** - Version control for strategy code

---

## 🎓 Learning Path

1. **Beginner**: Start with [Strategies README](strategies/README.md)
2. **Intermediate**: Read [Algo Engine Service](algo-engine.md) and create a simple plugin
3. **Advanced**: Study [Algo-Order Contract](algo-order-contract.md) and build integrated strategy
4. **Expert**: Implement custom market data adapter and advanced screening logic

---

## 🤖 AI Agent Notes

**Common Tasks**:
- **Add new strategy**: Extend `StrategyBase` in `services/algo_engine/app/strategies/`
- **Modify market data**: Edit `services/market_data/app/adapters/`
- **Update screener logic**: Modify `services/screener/app/api/routes.py`
- **Enhance InPlay**: Update `services/inplay/app/services/setup_detector.py`

**File Locations**:
```
services/
├── algo_engine/          # Strategy execution engine
│   ├── app/strategies/   # Strategy plugins
│   └── data/backtests/   # Backtest results
├── market_data/          # Market data service
│   └── app/adapters/     # Provider adapters
├── screener/             # Market screener
│   └── app/presets/      # Screener presets
└── inplay/               # Live monitoring
    └── app/services/     # Setup detection logic
```

**Testing**:
- Unit tests: `pytest services/{service}/app/tests/`
- Integration tests: `make test-trading-domain`
- Coverage requirement: ≥80%

---

**Domain Owner**: Trading Team  
**Last Reviewed**: 2026-01-06  
**Next Review**: 2026-02-06

---

[← Back to Main Index](../../../INDEX.md)
