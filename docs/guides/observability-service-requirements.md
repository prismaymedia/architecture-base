# Observability Requirements for Services

> **Note**: This document defines the **mandatory observability requirements** for ALL microservices in this framework. Include a reference to this document in every service's `.copilot-context.md` file.

## 🔍 Observability is Mandatory

Every service **MUST** implement complete observability following [ADR-010: Observability-First Architecture](../adr/010-observability-first-architecture.md).

A service is **NOT considered complete** without full observability implementation.

## Stack Components

- **OpenTelemetry SDK**: Unified instrumentation for traces, metrics, and logs
- **Prometheus**: Metrics collection (exposed at `/metrics` endpoint)
- **Grafana**: Dashboard visualization
- **Jaeger**: Distributed tracing
- **Loki + Promtail**: Log aggregation

## 1. Traces (OpenTelemetry)

### Required Spans

Every service must instrument:
- ✅ All HTTP endpoints (automatic with FastAPI instrumentor)
- ✅ All external API calls (Spotify API, other services)
- ✅ All database operations
- ✅ All event publishing operations
- ✅ All event handler functions
- ✅ Business-critical operations

### Example Implementation

```python
from opentelemetry import trace

tracer = trace.get_tracer(__name__)

@tracer.start_as_current_span("process_payment")
async def process_payment(payment_id: str):
    span = trace.get_current_span()
    span.set_attribute("payment.id", payment_id)
    span.set_attribute("payment.amount", amount)
    
    # Business logic
    result = await payment_service.process(payment_id)
    
    span.set_attribute("payment.status", result.status)
    return result
```

### Context Propagation

**Mandatory**: Propagate trace context across:
- HTTP requests (via `traceparent`, `tracestate` headers)
- Events (include `trace_context` in event payload)
- Logs (link logs to traces via `trace_id` and `span_id`)

## 2. Metrics (Prometheus)

### RED Metrics (Required for All Services)

```python
from prometheus_client import Counter, Histogram, Gauge

# Request Rate
http_requests_total = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

# Error Rate
# Derived from http_requests_total with status='error'

# Duration
http_request_duration_seconds = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration',
    ['method', 'endpoint'],
    buckets=[0.001, 0.01, 0.05, 0.1, 0.5, 1.0, 5.0, 10.0]
)

# In-Progress Requests
http_requests_in_progress = Gauge(
    'http_requests_in_progress',
    'HTTP requests currently being processed',
    ['method', 'endpoint']
)
```

### Event Processing Metrics (Required if Service Publishes/Consumes Events)

```python
# Events Published
events_published_total = Counter(
    'events_published_total',
    'Total events published',
    ['event_type', 'status']
)

# Events Consumed
events_consumed_total = Counter(
    'events_consumed_total',
    'Total events consumed',
    ['event_type', 'status']
)

# Event Processing Duration
event_processing_duration_seconds = Histogram(
    'event_processing_duration_seconds',
    'Event processing duration',
    ['event_type'],
    buckets=[0.01, 0.05, 0.1, 0.5, 1.0, 5.0]
)
```

### Database Metrics (Required if Service Has Database)

```python
# Query Duration
db_query_duration_seconds = Histogram(
    'db_query_duration_seconds',
    'Database query duration',
    ['operation'],  # SELECT, INSERT, UPDATE, DELETE
    buckets=[0.001, 0.01, 0.05, 0.1, 0.5, 1.0]
)

# Active Connections
db_connections_active = Gauge(
    'db_connections_active',
    'Number of active database connections'
)

# Connection Pool Usage
db_connection_pool_usage = Gauge(
    'db_connection_pool_usage',
    'Database connection pool usage percentage'
)
```

### External API Metrics (Required if Service Calls External APIs)

```python
# External API Calls
external_api_calls_total = Counter(
    'external_api_calls_total',
    'Total external API calls',
    ['service', 'endpoint', 'status']
)

# External API Duration
external_api_duration_seconds = Histogram(
    'external_api_duration_seconds',
    'External API call duration',
    ['service', 'endpoint'],
    buckets=[0.1, 0.5, 1.0, 2.0, 5.0, 10.0]
)
```

### Business Metrics (Service-Specific)

Each service should expose business-relevant metrics:

**Examples**:
- `orders_created_total` (Orders API)
- `payments_processed_total` (Payments API)
- `spotify_tracks_played_total` (Playback Control API)
- `user_authentications_total` (Spotify Integration API)

## 3. Structured Logs

### Required Format

All logs must be in **JSON format** with standard fields:

```python
import structlog
from opentelemetry import trace

logger = structlog.get_logger()

# Configure correlation context
structlog.contextvars.bind_contextvars(
    service="service-name",
    correlation_id=request.headers.get("X-Correlation-ID"),
    user_id=request.user.id
)

# Log with trace context
span = trace.get_current_span()
logger.info(
    "operation_completed",
    operation="process_order",
    order_id=order_id,
    duration_ms=duration,
    trace_id=format(span.get_span_context().trace_id, '032x'),
    span_id=format(span.get_span_context().span_id, '016x')
)
```

### Output Example

```json
{
  "timestamp": "2025-11-14T22:05:36.209Z",
  "level": "info",
  "service": "playback-control-api",
  "correlation_id": "abc-123-def",
  "trace_id": "8e42f1a2b3c4d5e6f7g8h9i0j1k2l3m4",
  "span_id": "f7g8h9i0j1k2l3m4",
  "user_id": "user456",
  "event": "playback_started",
  "track_id": "spotify:track:123",
  "device_id": "device456",
  "duration_ms": 142
}
```

### Required Fields

- `timestamp` (ISO 8601)
- `level` (debug, info, warning, error, critical)
- `service` (service name)
- `correlation_id` (request correlation ID)
- `trace_id` (OpenTelemetry trace ID)
- `span_id` (OpenTelemetry span ID)
- `event` (log message in snake_case)

### Log Levels

| Level | Usage | Example |
|-------|-------|---------|
| **DEBUG** | Development details | `logger.debug("cache_lookup", key=cache_key)` |
| **INFO** | Normal business events | `logger.info("order_created", order_id=id)` |
| **WARNING** | Unexpected but handled | `logger.warning("rate_limit_approaching", usage=90)` |
| **ERROR** | Recoverable errors | `logger.error("payment_failed", error=str(e))` |
| **CRITICAL** | System failures | `logger.critical("database_unavailable")` |

### Security: Never Log Sensitive Data

❌ **Never log**:
- Passwords
- API tokens
- Credit card numbers
- Social security numbers
- Full email addresses (can log domain only)
- Session IDs
- Private keys

## 4. Dashboards (Grafana)

### Required Dashboard: "Service Overview"

Every service must have a Grafana dashboard with these panels:

#### Essential Panels

1. **Request Rate**
   ```promql
   rate(http_requests_total{service="service-name"}[5m])
   ```

2. **Error Rate (%)**
   ```promql
   rate(http_requests_total{service="service-name",status="error"}[5m]) / 
   rate(http_requests_total{service="service-name"}[5m]) * 100
   ```

3. **Latency (P50, P95, P99)**
   ```promql
   histogram_quantile(0.50, rate(http_request_duration_seconds_bucket{service="service-name"}[5m]))
   histogram_quantile(0.95, rate(http_request_duration_seconds_bucket{service="service-name"}[5m]))
   histogram_quantile(0.99, rate(http_request_duration_seconds_bucket{service="service-name"}[5m]))
   ```

4. **Active Requests**
   ```promql
   http_requests_in_progress{service="service-name"}
   ```

5. **Event Processing Rate** (if applicable)
   ```promql
   rate(events_consumed_total{service="service-name"}[5m])
   ```

6. **Error Types** (if applicable)
   ```promql
   sum by (error_type) (rate(errors_total{service="service-name"}[5m]))
   ```

### Dashboard Template Location

`/dashboards/service-overview-template.json` - Copy and customize for each service

## 5. Alerts (Prometheus)

### Required Alerts

Every service must configure these alerts:

#### 1. High Error Rate

```yaml
- alert: HighErrorRate
  expr: |
    rate(http_requests_total{service="$SERVICE_NAME",status="error"}[5m]) / 
    rate(http_requests_total{service="$SERVICE_NAME"}[5m]) > 0.05
  for: 5m
  labels:
    severity: warning
    service: $SERVICE_NAME
  annotations:
    summary: "High error rate on {{ $labels.service }}"
    description: "Error rate is {{ $value | humanizePercentage }} (threshold: 5%)"
```

#### 2. High Latency

```yaml
- alert: HighLatency
  expr: |
    histogram_quantile(0.95, 
      rate(http_request_duration_seconds_bucket{service="$SERVICE_NAME"}[5m])
    ) > 1.0
  for: 5m
  labels:
    severity: warning
    service: $SERVICE_NAME
  annotations:
    summary: "High latency on {{ $labels.service }}"
    description: "P95 latency is {{ $value }}s (threshold: 1s)"
```

#### 3. Service Down

```yaml
- alert: ServiceDown
  expr: up{service="$SERVICE_NAME"} == 0
  for: 1m
  labels:
    severity: critical
    service: $SERVICE_NAME
  annotations:
    summary: "Service {{ $labels.service }} is down"
    description: "Service has been down for more than 1 minute"
```

#### 4. Event Processing Failures (if applicable)

```yaml
- alert: HighEventProcessingFailureRate
  expr: |
    rate(events_consumed_total{service="$SERVICE_NAME",status="error"}[5m]) / 
    rate(events_consumed_total{service="$SERVICE_NAME"}[5m]) > 0.10
  for: 5m
  labels:
    severity: warning
    service: $SERVICE_NAME
  annotations:
    summary: "High event processing failure rate"
    description: "Event failure rate is {{ $value | humanizePercentage }} (threshold: 10%)"
```

## 6. Health Check Endpoint

### Required Endpoint: `GET /health`

Every service must expose a health check endpoint:

```python
from fastapi import APIRouter, status
from typing import Dict, Any

router = APIRouter()

@router.get("/health", status_code=status.HTTP_200_OK)
async def health_check() -> Dict[str, Any]:
    """
    Health check endpoint that verifies service and dependencies status.
    """
    checks = {
        "database": await check_database(),
        "pubsub": await check_pubsub(),
        "cache": await check_cache(),
        "external_api": await check_external_api()
    }
    
    all_healthy = all(check == "healthy" for check in checks.values())
    
    return {
        "status": "healthy" if all_healthy else "degraded",
        "service": "service-name",
        "version": "1.0.0",
        "checks": checks,
        "timestamp": datetime.utcnow().isoformat()
    }
```

### Health Check Response Format

**Healthy**:
```json
{
  "status": "healthy",
  "service": "playback-control-api",
  "version": "1.0.0",
  "checks": {
    "database": "healthy",
    "pubsub": "healthy",
    "cache": "healthy",
    "spotify_api": "healthy"
  },
  "timestamp": "2025-11-14T22:05:36.209Z"
}
```

**Degraded**:
```json
{
  "status": "degraded",
  "service": "playback-control-api",
  "version": "1.0.0",
  "checks": {
    "database": "healthy",
    "pubsub": "healthy",
    "cache": "unhealthy",
    "spotify_api": "healthy"
  },
  "timestamp": "2025-11-14T22:05:36.209Z"
}
```

## 7. Testing Observability

### Required Tests

Every service must include tests for observability:

#### Test Metric Emission

```python
def test_http_request_counter_incremented():
    """Verify that metrics are emitted correctly"""
    from app.core.metrics import http_requests_total
    
    initial = http_requests_total.labels(
        method='GET',
        endpoint='/api/test',
        status='success'
    )._value.get()
    
    # Trigger operation
    response = client.get("/api/test")
    
    final = http_requests_total.labels(
        method='GET',
        endpoint='/api/test',
        status='success'
    )._value.get()
    
    assert final == initial + 1
```

#### Test Trace Creation

```python
def test_span_created_for_operation(span_exporter):
    """Verify that spans are created"""
    from app.api.orders import create_order
    
    await create_order(order_data)
    
    spans = span_exporter.get_finished_spans()
    assert len(spans) > 0
    assert any(span.name == "create_order" for span in spans)
```

#### Test Structured Logs

```python
def test_logs_are_structured_json():
    """Verify logs are in JSON format with required fields"""
    import json
    
    # Capture log output
    log_output = capture_logs()
    
    # Parse as JSON
    log_entry = json.loads(log_output)
    
    # Verify required fields
    assert "timestamp" in log_entry
    assert "level" in log_entry
    assert "service" in log_entry
    assert "correlation_id" in log_entry
    assert "trace_id" in log_entry
    assert "span_id" in log_entry
```

## 8. Definition of Done for Observability

A service is **COMPLETE** only when:

- [x] **OpenTelemetry SDK integrated**
  - Tracer configured
  - Meter configured
  - Structured logging configured

- [x] **Traces Implemented**
  - All endpoints instrumented
  - External calls instrumented
  - Context propagation working
  - Tests for traces passing

- [x] **Metrics Implemented**
  - RED metrics exposed
  - Service-specific metrics defined
  - `/metrics` endpoint returning data
  - Tests for metrics passing

- [x] **Logs Implemented**
  - JSON structured format
  - Standard fields included
  - Trace context linked
  - No sensitive data logged
  - Tests for log format passing

- [x] **Dashboard Created**
  - Grafana dashboard deployed
  - Essential panels configured
  - Service-specific visualizations added

- [x] **Alerts Configured**
  - Error rate alert
  - Latency alert
  - Service down alert
  - Service-specific alerts

- [x] **Health Check Implemented**
  - `/health` endpoint working
  - All dependencies checked
  - Appropriate status codes

- [x] **Documentation Updated**
  - Metrics documented
  - Traces documented
  - Runbooks created
  - Troubleshooting guide updated

## 9. Implementation Checklist

Use this checklist when implementing observability for a service:

### Setup Phase
- [ ] Install OpenTelemetry dependencies
- [ ] Configure tracer provider
- [ ] Configure meter provider
- [ ] Configure structured logging (structlog)
- [ ] Set up correlation context

### Instrumentation Phase
- [ ] Instrument FastAPI with FastAPIInstrumentor
- [ ] Add spans to business operations
- [ ] Define and implement metrics
- [ ] Add structured logging to key operations
- [ ] Implement context propagation

### Infrastructure Phase
- [ ] Create Grafana dashboard
- [ ] Define Prometheus alerts
- [ ] Implement `/health` endpoint
- [ ] Implement `/metrics` endpoint
- [ ] Configure log shipping (Promtail)

### Testing Phase
- [ ] Write metric emission tests
- [ ] Write span creation tests
- [ ] Write structured log tests
- [ ] Write health check tests
- [ ] Validate in staging environment

### Documentation Phase
- [ ] Document metrics in service README
- [ ] Document traces in service README
- [ ] Create runbook for alerts
- [ ] Update troubleshooting guide

## References

- [ADR-010: Observability-First Architecture](../adr/010-observability-first-architecture.md)
- [Observability Best Practices](observability-best-practices.md)
- [OpenTelemetry Python Documentation](https://opentelemetry.io/docs/instrumentation/python/)
- [Prometheus Best Practices](https://prometheus.io/docs/practices/naming/)
- [Grafana Dashboard Best Practices](https://grafana.com/docs/grafana/latest/best-practices/dashboard-design/)

---

**Last Updated**: 2025-11-14  
**Maintained by**: Architecture Team
