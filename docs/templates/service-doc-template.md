---
title: "Service Name"
domain: "domain-key"
description: "Short summary of the service purpose."
keywords: [service, api, reference]
responsible: ["AgentName"]
status: draft
last_updated: 2026-01-06
---

# Service Name

> **Service**: `service_name`
> **Owner**: AgentName
> **Default Port**: `0000`

## Overview

Describe what the service does and who depends on it.

## Architecture

- Key components
- Data stores
- External dependencies

## API Endpoints

### `GET /health`

Describe the health check behavior.

**Response**:
```json
{
  "status": "ok"
}
```

## Configuration

List environment variables or config files.

## Dependencies

- Service A
- Service B

## Testing

- `make test-service SERVICE=service_name`

## Deployment

Explain how to deploy or restart the service.

## Related Documentation

- [Domain Index](../domains/DOMAIN/INDEX.md)
