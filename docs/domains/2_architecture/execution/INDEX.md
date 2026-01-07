---
domain: 2_architecture
title: Execution Domain Documentation
description: Order execution, routing, and broker integration documentation.
keywords: execution, order-routing, brokers, risk, index
last_updated: 2026-01-06
---

# Execution Domain Documentation

> **Domain**: Order execution, routing, and broker integration

**Keywords**: execution, orders, order-router, brokers, risk-rules, Binance, IBKR, ExecutionIntent, ExecutionReport, sandbox

---

## Overview

The Execution domain covers all aspects of order routing, broker integration, and order execution within the trading bot platform. This includes the order router service, broker adapters, risk rules, and the contract between algorithms and the execution layer.

---

## Documentation Index

### Core Services

#### [Order Router Service](order-router.md)

The **Order Router** service centralizes order routing to multiple brokers and applies risk rules.

**Key Features**:
- Multi-broker support (Binance, IBKR)
- Risk rule engine (MaxNotionalRule, MaxDailyLossRule)
- Order logging and tracking
- Execution state management

**API Endpoints**:
- `GET /health` - Service status
- `GET /brokers` - Available brokers list
- `POST /orders` - Route order with risk validation
- `POST /orders/{broker}/cancel` - Cancel order
- `GET /orders/log` - Order log with filters
- `GET /executions` - Aggregated executions
- `GET /state` - Execution state (paper/live mode)
- `PUT /state` - Update mode and daily limits

**Related Code**: `services/order-router/`

---

#### [Algo-Order Contract](algo-order-contract.md)

REST contract specification between algorithms and the `order-router` service for standardized order submission in the sandbox environment.

**Key Components**:
- `ExecutionIntent` - Request payload (order + risk context)
- `ExecutionReport` - Response payload (execution acknowledgment)

**Contract Details**:
- Method: `POST`
- Path: `/orders`
- Success: `201 Created`
- Error codes: `400`, `403`, `404`, `500`

**Schema Location**: `schemas/order_router.py`

---

## Broker Adapters

### Binance Adapter
- **Status**: Production-ready (GA)
- **Behavior**: Immediate confirmation, full execution
- **Implementation**: `BinanceAdapter` class

### Interactive Brokers (IBKR) Adapter
- **Status**: Production-ready (GA)
- **Behavior**: Simulator with partial fills
- **Implementation**: `IBKRAdapter` class

Both adapters inherit from `BrokerAdapter` and implement `place_order`.

---

## Risk Rules

The order router includes a configurable risk rule engine (`risk_rules.py`):

- **MaxNotionalRule**: Notional cap per symbol
- **MaxDailyLossRule**: Daily aggregated stop-loss
- **RiskEngine**: Sequentially applies rules

Each rule returns a `RiskSignal` with level:
- `alert`: Logged, retrievable via `GET /risk/alerts`
- `lock`: Stops order immediately, surfaces reason via API

---

## Related Domains

- **[1_trading](../../1_trading/INDEX.md)**: Strategy execution and algo engine
- **[4_security](../../4_security/INDEX.md)**: Entitlements and permissions (`can.route_orders`)
- **[6_quality](../../6_quality/INDEX.md)**: Risk management documentation

---

## Quick Links

| Document | Description |
|----------|-------------|
| [Order Router](order-router.md) | Service documentation and API reference |
| [Algo-Order Contract](algo-order-contract.md) | REST contract specification |

---

## Code References

- **Service**: `services/order-router/`
- **Schemas**: `schemas/order_router.py`
- **Risk Rules**: `services/order-router/app/risk_rules.py`
- **Broker Adapters**: `services/order-router/app/adapters/`

---

**Last Updated**: 2026-01-06  
**Domain**: 2_architecture  
**Maintained By**: Trading Bot Team
