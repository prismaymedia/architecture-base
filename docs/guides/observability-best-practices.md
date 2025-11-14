# Guía de Mejores Prácticas de Observabilidad

Esta guía proporciona lineamientos prácticos y ejemplos concretos para implementar observabilidad en todos los componentes del framework.

## Tabla de Contenidos

1. [Principios Fundamentales](#principios-fundamentales)
2. [Configuración del Stack](#configuración-del-stack)
3. [Instrumentación de Servicios](#instrumentación-de-servicios)
4. [Logs Estructurados](#logs-estructurados)
5. [Métricas](#métricas)
6. [Distributed Tracing](#distributed-tracing)
7. [Dashboards y Alertas](#dashboards-y-alertas)
8. [Testing de Observabilidad](#testing-de-observabilidad)
9. [Troubleshooting](#troubleshooting)
10. [Checklist de Implementación](#checklist-de-implementación)

## Principios Fundamentales

### 1. Observabilidad es Obligatoria

> **Regla de Oro**: Si no es observable, no está completo.

La observabilidad no es opcional. Cada componente debe permitir responder:
- ¿Está funcionando correctamente?
- ¿Qué tan rápido responde?
- ¿Dónde están los errores?
- ¿Cómo llegamos a este estado?

### 2. Instrumentación desde el Diseño

No agregues observabilidad como un "afterthought". Desde la primera línea de código:
```python
# ❌ MAL: Código sin instrumentación
def process_order(order_id: str):
    order = get_order(order_id)
    return process(order)

# ✅ BIEN: Código con instrumentación desde el inicio
@tracer.start_as_current_span("process_order")
def process_order(order_id: str):
    logger.info("processing_order_started", order_id=order_id)
    
    with metrics.timer("order_processing_duration"):
        try:
            order = get_order(order_id)
            result = process(order)
            
            metrics.increment("orders_processed_total", tags=["status:success"])
            logger.info("processing_order_completed", order_id=order_id)
            
            return result
        except Exception as e:
            metrics.increment("orders_processed_total", tags=["status:error"])
            logger.error("processing_order_failed", order_id=order_id, error=str(e))
            raise
```

### 3. Estandarización

Todos los servicios deben seguir los mismos patrones:
- Mismo formato de logs
- Mismas convenciones de naming para métricas
- Misma estructura de traces
- Mismos dashboards base

### 4. Minimal Performance Impact

La instrumentación debe tener overhead mínimo:
- Sampling inteligente para traces (no 100%)
- Métricas agregadas, no raw data
- Async logging cuando sea posible
- Buffering de eventos

## Configuración del Stack

### Componentes del Stack

```yaml
# docker-compose.yml para stack de observabilidad local
version: '3.8'

services:
  # OpenTelemetry Collector
  otel-collector:
    image: otel/opentelemetry-collector:latest
    command: ["--config=/etc/otel-collector-config.yaml"]
    volumes:
      - ./otel-collector-config.yaml:/etc/otel-collector-config.yaml
    ports:
      - "4317:4317"   # OTLP gRPC receiver
      - "4318:4318"   # OTLP HTTP receiver
      - "8888:8888"   # Prometheus metrics
      - "13133:13133" # Health check

  # Prometheus
  prometheus:
    image: prom/prometheus:latest
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus-data:/prometheus
    ports:
      - "9090:9090"
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
      - '--web.enable-lifecycle'

  # Grafana
  grafana:
    image: grafana/grafana:latest
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
      - GF_INSTALL_PLUGINS=grafana-clock-panel
    volumes:
      - grafana-data:/var/lib/grafana
      - ./grafana/dashboards:/etc/grafana/provisioning/dashboards
      - ./grafana/datasources:/etc/grafana/provisioning/datasources

  # Jaeger
  jaeger:
    image: jaegertracing/all-in-one:latest
    ports:
      - "16686:16686" # UI
      - "14268:14268" # Collector HTTP
      - "14250:14250" # Collector gRPC
    environment:
      - COLLECTOR_OTLP_ENABLED=true

  # Loki
  loki:
    image: grafana/loki:latest
    ports:
      - "3100:3100"
    command: -config.file=/etc/loki/local-config.yaml
    volumes:
      - loki-data:/loki

  # Promtail
  promtail:
    image: grafana/promtail:latest
    volumes:
      - /var/log:/var/log
      - ./promtail-config.yaml:/etc/promtail/config.yaml
    command: -config.file=/etc/promtail/config.yaml

volumes:
  prometheus-data:
  grafana-data:
  loki-data:
```

### Configuración de OpenTelemetry Collector

```yaml
# otel-collector-config.yaml
receivers:
  otlp:
    protocols:
      grpc:
        endpoint: 0.0.0.0:4317
      http:
        endpoint: 0.0.0.0:4318

processors:
  batch:
    timeout: 10s
    send_batch_size: 1024
  
  # Sampling para reducir volumen
  probabilistic_sampler:
    sampling_percentage: 10  # 10% de traces

  # Enriquecimiento con atributos
  attributes:
    actions:
      - key: environment
        value: development
        action: insert

exporters:
  # Exportar traces a Jaeger
  jaeger:
    endpoint: jaeger:14250
    tls:
      insecure: true

  # Exportar metrics a Prometheus
  prometheus:
    endpoint: "0.0.0.0:8889"

  # Exportar logs a Loki
  loki:
    endpoint: http://loki:3100/loki/api/v1/push

  # Logging para debugging
  logging:
    loglevel: info

service:
  pipelines:
    traces:
      receivers: [otlp]
      processors: [probabilistic_sampler, batch, attributes]
      exporters: [jaeger, logging]
    
    metrics:
      receivers: [otlp]
      processors: [batch]
      exporters: [prometheus, logging]
    
    logs:
      receivers: [otlp]
      processors: [batch, attributes]
      exporters: [loki, logging]
```

### Configuración de Prometheus

```yaml
# prometheus.yml
global:
  scrape_interval: 15s
  evaluation_interval: 15s
  external_labels:
    cluster: 'development'
    environment: 'dev'

scrape_configs:
  # Prometheus self-monitoring
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']

  # OpenTelemetry Collector metrics
  - job_name: 'otel-collector'
    static_configs:
      - targets: ['otel-collector:8888']

  # Services - Auto-discovery en producción
  - job_name: 'services'
    static_configs:
      - targets:
        - 'spotify-integration-api:8000'
        - 'playback-control-api:8000'
        - 'sync-service:8000'
        - 'dj-console-integration-api:8000'
    
    relabel_configs:
      - source_labels: [__address__]
        target_label: instance
```

## Instrumentación de Servicios

### Setup Inicial (Python/FastAPI)

#### 1. Instalar Dependencias

```bash
# requirements.txt
opentelemetry-api==1.21.0
opentelemetry-sdk==1.21.0
opentelemetry-instrumentation-fastapi==0.42b0
opentelemetry-instrumentation-httpx==0.42b0
opentelemetry-instrumentation-sqlalchemy==0.42b0
opentelemetry-exporter-otlp==1.21.0
prometheus-client==0.19.0
structlog==23.2.0
```

#### 2. Configurar OpenTelemetry

```python
# app/core/observability.py
from opentelemetry import trace, metrics
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
import structlog
import os

def setup_observability(app, service_name: str):
    """
    Configura observabilidad completa para un servicio FastAPI.
    
    Args:
        app: Instancia de FastAPI
        service_name: Nombre del servicio (e.g., "spotify-integration-api")
    """
    
    # 1. Configurar recursos (atributos comunes)
    resource = Resource.create({
        "service.name": service_name,
        "service.version": os.getenv("SERVICE_VERSION", "1.0.0"),
        "deployment.environment": os.getenv("ENVIRONMENT", "development"),
    })
    
    # 2. Configurar Traces
    trace_provider = TracerProvider(resource=resource)
    otlp_trace_exporter = OTLPSpanExporter(
        endpoint=os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "http://otel-collector:4317"),
        insecure=True
    )
    trace_provider.add_span_processor(BatchSpanProcessor(otlp_trace_exporter))
    trace.set_tracer_provider(trace_provider)
    
    # 3. Configurar Metrics
    metric_reader = PeriodicExportingMetricReader(
        OTLPMetricExporter(
            endpoint=os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "http://otel-collector:4317"),
            insecure=True
        ),
        export_interval_millis=60000  # Export every 60 seconds
    )
    meter_provider = MeterProvider(resource=resource, metric_readers=[metric_reader])
    metrics.set_meter_provider(meter_provider)
    
    # 4. Instrumentar FastAPI automáticamente
    FastAPIInstrumentor.instrument_app(
        app,
        tracer_provider=trace_provider,
        meter_provider=meter_provider,
        excluded_urls="/health,/metrics"  # No instrumentar endpoints de monitoring
    )
    
    # 5. Configurar Logs Estructurados
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.JSONRenderer()
        ],
        wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=True,
    )
    
    return trace.get_tracer(__name__), metrics.get_meter(__name__)
```

#### 3. Integrar en Aplicación

```python
# app/main.py
from fastapi import FastAPI
from prometheus_client import make_asgi_app
from app.core.observability import setup_observability
import structlog

app = FastAPI(title="Spotify Integration API")

# Setup observability
tracer, meter = setup_observability(app, "spotify-integration-api")
logger = structlog.get_logger()

# Exponer métricas de Prometheus
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

# Health check endpoint
@app.get("/health")
async def health():
    return {"status": "healthy", "service": "spotify-integration-api"}

# Example instrumented endpoint
@app.get("/api/users/{user_id}")
async def get_user(user_id: str):
    # El trace se crea automáticamente por FastAPIInstrumentor
    # Podemos agregar atributos personalizados
    with tracer.start_as_current_span("fetch_user_details") as span:
        span.set_attribute("user.id", user_id)
        
        logger.info("fetching_user", user_id=user_id)
        
        try:
            # Lógica de negocio
            user = await user_service.get(user_id)
            
            logger.info("user_fetched", user_id=user_id, username=user.username)
            return user
            
        except UserNotFoundError as e:
            logger.warning("user_not_found", user_id=user_id)
            span.set_status(Status(StatusCode.ERROR, "User not found"))
            raise HTTPException(status_code=404, detail="User not found")
        
        except Exception as e:
            logger.error("user_fetch_failed", user_id=user_id, error=str(e), exc_info=True)
            span.record_exception(e)
            span.set_status(Status(StatusCode.ERROR, str(e)))
            raise
```

## Logs Estructurados

### Principios

1. **Siempre JSON**: Logs en formato JSON para parsing automatizado
2. **Campos Consistentes**: Mismos campos en todos los servicios
3. **Contexto Rico**: Incluir toda la información relevante
4. **No Secrets**: Nunca loguear información sensible

### Formato Estándar

```python
import structlog
from opentelemetry import trace

logger = structlog.get_logger()

# Configurar contexto global (en cada request)
structlog.contextvars.bind_contextvars(
    correlation_id=request.headers.get("X-Correlation-ID"),
    user_id=request.user.id,
    service="spotify-integration-api"
)

# Logging con contexto automático
logger.info(
    "spotify_authentication_completed",
    spotify_user_id="user123",
    access_token_expires_in=3600,
    scopes=["user-read-playback-state", "user-modify-playback-state"],
    duration_ms=234
)

# Output:
# {
#   "event": "spotify_authentication_completed",
#   "timestamp": "2025-11-14T22:05:36.209Z",
#   "level": "info",
#   "service": "spotify-integration-api",
#   "correlation_id": "abc-123-def",
#   "trace_id": "8e42f1a2b3c4d5e6",
#   "span_id": "f7g8h9i0j1k2",
#   "user_id": "user456",
#   "spotify_user_id": "user123",
#   "access_token_expires_in": 3600,
#   "scopes": ["user-read-playback-state", "user-modify-playback-state"],
#   "duration_ms": 234
# }
```

### Niveles de Log

| Nivel | Uso | Ejemplo |
|-------|-----|---------|
| **DEBUG** | Información de desarrollo, troubleshooting detallado | `logger.debug("sql_query_executed", query=query, params=params)` |
| **INFO** | Eventos de negocio normales | `logger.info("order_created", order_id=order_id)` |
| **WARNING** | Situaciones inesperadas pero manejables | `logger.warning("rate_limit_approaching", current_rate=90)` |
| **ERROR** | Errores que impactan operación pero son recuperables | `logger.error("payment_failed", order_id=order_id, error=str(e))` |
| **CRITICAL** | Errores que requieren atención inmediata | `logger.critical("database_connection_lost")` |

### Patrones Comunes

```python
# 1. Logging de operaciones con duración
import time

start_time = time.time()
try:
    result = await long_operation()
    duration_ms = (time.time() - start_time) * 1000
    
    logger.info(
        "operation_completed",
        operation="long_operation",
        duration_ms=duration_ms,
        status="success"
    )
except Exception as e:
    duration_ms = (time.time() - start_time) * 1000
    
    logger.error(
        "operation_failed",
        operation="long_operation",
        duration_ms=duration_ms,
        status="error",
        error=str(e),
        exc_info=True
    )
    raise

# 2. Logging de eventos procesados
logger.info(
    "event_received",
    event_type="OrderCreatedEvent",
    event_id=event.id,
    correlation_id=event.correlation_id,
    order_id=event.order_id
)

# 3. Logging con sampling (para operaciones de alto volumen)
if random.random() < 0.01:  # Log 1% of requests
    logger.debug("high_volume_operation", details=data)

# 4. Logging de external API calls
logger.info(
    "external_api_call",
    service="spotify_api",
    endpoint="/v1/me/player/play",
    method="PUT",
    status_code=response.status_code,
    duration_ms=response.elapsed.total_seconds() * 1000
)
```

## Métricas

### Tipos de Métricas

#### 1. Counter (monotónico, solo incrementa)

```python
from prometheus_client import Counter

# Definición
http_requests_total = Counter(
    'http_requests_total',
    'Total de requests HTTP',
    ['method', 'endpoint', 'status']
)

# Uso
http_requests_total.labels(
    method='POST',
    endpoint='/api/orders',
    status='success'
).inc()
```

#### 2. Gauge (valor que puede subir y bajar)

```python
from prometheus_client import Gauge

# Definición
active_connections = Gauge(
    'active_connections',
    'Número de conexiones activas'
)

# Uso
active_connections.inc()  # Incrementar
active_connections.dec()  # Decrementar
active_connections.set(42)  # Setear valor absoluto
```

#### 3. Histogram (distribución de valores)

```python
from prometheus_client import Histogram

# Definición
request_duration_seconds = Histogram(
    'request_duration_seconds',
    'Duración de requests HTTP',
    ['method', 'endpoint'],
    buckets=[0.01, 0.05, 0.1, 0.5, 1.0, 5.0]  # Customizable
)

# Uso
with request_duration_seconds.labels(
    method='GET',
    endpoint='/api/orders'
).time():
    # Operación a medir
    result = await process_request()
```

#### 4. Summary (similar a Histogram, con percentiles)

```python
from prometheus_client import Summary

# Definición
request_latency_seconds = Summary(
    'request_latency_seconds',
    'Latencia de requests',
    ['endpoint']
)

# Uso
with request_latency_seconds.labels(endpoint='/api/orders').time():
    result = await process_request()
```

### Métricas Obligatorias por Servicio

```python
# app/core/metrics.py
from prometheus_client import Counter, Histogram, Gauge

# RED Metrics
http_requests_total = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

http_request_duration_seconds = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration in seconds',
    ['method', 'endpoint'],
    buckets=[0.001, 0.01, 0.05, 0.1, 0.5, 1.0, 5.0, 10.0]
)

http_requests_in_progress = Gauge(
    'http_requests_in_progress',
    'Number of HTTP requests in progress',
    ['method', 'endpoint']
)

# Event Processing Metrics
events_published_total = Counter(
    'events_published_total',
    'Total events published',
    ['event_type', 'status']
)

events_consumed_total = Counter(
    'events_consumed_total',
    'Total events consumed',
    ['event_type', 'status']
)

event_processing_duration_seconds = Histogram(
    'event_processing_duration_seconds',
    'Event processing duration',
    ['event_type'],
    buckets=[0.01, 0.05, 0.1, 0.5, 1.0, 5.0]
)

# Database Metrics
db_query_duration_seconds = Histogram(
    'db_query_duration_seconds',
    'Database query duration',
    ['query_type'],
    buckets=[0.001, 0.01, 0.05, 0.1, 0.5, 1.0]
)

db_connections_active = Gauge(
    'db_connections_active',
    'Number of active database connections'
)

# External API Metrics
external_api_requests_total = Counter(
    'external_api_requests_total',
    'Total external API requests',
    ['service', 'endpoint', 'status']
)

external_api_duration_seconds = Histogram(
    'external_api_duration_seconds',
    'External API request duration',
    ['service', 'endpoint'],
    buckets=[0.1, 0.5, 1.0, 2.0, 5.0, 10.0]
)
```

### Naming Conventions

**Formato**: `{namespace}_{subsystem}_{name}_{unit}`

Ejemplos:
- `http_requests_total` (counter)
- `http_request_duration_seconds` (histogram)
- `database_connections_active` (gauge)
- `spotify_api_calls_total` (counter)

**Reglas**:
- Snake_case
- Plurales para contadores
- Incluir unidad al final (`_seconds`, `_bytes`, `_total`)
- Labels para dimensiones variables (method, endpoint, status)

## Distributed Tracing

### Context Propagation

```python
# 1. En HTTP requests salientes (a otros servicios o APIs externas)
import httpx
from opentelemetry.propagate import inject

async def call_external_service(url: str):
    headers = {}
    inject(headers)  # Inyecta trace context en headers
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
    
    return response

# 2. En eventos publicados
from dataclasses import dataclass
from opentelemetry import trace

@dataclass
class OrderCreatedEvent:
    order_id: str
    trace_context: dict  # Para propagar context
    
def publish_event(event: OrderCreatedEvent):
    # Inyectar trace context en el evento
    carrier = {}
    inject(carrier)
    event.trace_context = carrier
    
    # Publicar evento
    event_bus.publish("OrderCreatedEvent", event)

# 3. En consumidores de eventos
from opentelemetry.propagate import extract
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator

def consume_event(event: OrderCreatedEvent):
    # Extraer trace context del evento
    ctx = extract(event.trace_context)
    
    # Usar context en el span
    with tracer.start_as_current_span(
        "handle_order_created",
        context=ctx
    ) as span:
        span.set_attribute("event.type", "OrderCreatedEvent")
        span.set_attribute("event.id", event.id)
        
        # Procesar evento
        process_order_created(event)
```

### Attributes y Tags

```python
from opentelemetry import trace
from opentelemetry.trace import Status, StatusCode

with tracer.start_as_current_span("process_payment") as span:
    # Atributos de negocio
    span.set_attribute("payment.id", payment_id)
    span.set_attribute("payment.amount", amount)
    span.set_attribute("payment.currency", "USD")
    span.set_attribute("user.id", user_id)
    
    # Atributos técnicos
    span.set_attribute("db.system", "postgresql")
    span.set_attribute("db.operation", "INSERT")
    
    try:
        result = await process_payment()
        
        # Marcar span como exitoso
        span.set_status(Status(StatusCode.OK))
        span.set_attribute("payment.status", "approved")
        
        return result
        
    except PaymentDeclinedError as e:
        # Error de negocio (no es error del sistema)
        span.set_status(Status(StatusCode.OK))
        span.set_attribute("payment.status", "declined")
        span.set_attribute("payment.decline_reason", str(e))
        raise
        
    except Exception as e:
        # Error técnico
        span.record_exception(e)
        span.set_status(Status(StatusCode.ERROR, str(e)))
        span.set_attribute("error.type", type(e).__name__)
        raise
```

### Sampling Strategies

```python
# Configurar sampling rate según caso de uso
from opentelemetry.sdk.trace.sampling import (
    ParentBasedTraceIdRatioBased,
    TraceIdRatioBased,
    ALWAYS_ON,
    ALWAYS_OFF
)

# 1. Sampling probabilístico (10% de traces)
sampler = ParentBasedTraceIdRatioBased(
    root=TraceIdRatioBased(0.1)  # 10%
)

# 2. Sampling basado en condiciones
class CustomSampler(Sampler):
    def should_sample(self, context, trace_id, name, attributes, ...):
        # Siempre sample errores
        if attributes.get("error") is True:
            return ALWAYS_ON
        
        # Sample 100% de operaciones críticas
        if name in ["process_payment", "authenticate_user"]:
            return ALWAYS_ON
        
        # Sample 1% de operaciones de lectura
        if name.startswith("get_") or name.startswith("list_"):
            return TraceIdRatioBased(0.01)
        
        # Default 10%
        return TraceIdRatioBased(0.1)

trace_provider = TracerProvider(sampler=CustomSampler())
```

## Dashboards y Alertas

### Dashboard de Servicio (Template)

```json
{
  "dashboard": {
    "title": "Service Overview - ${service_name}",
    "panels": [
      {
        "title": "Request Rate (req/s)",
        "targets": [
          {
            "expr": "rate(http_requests_total{service=\"${service_name}\"}[5m])"
          }
        ]
      },
      {
        "title": "Error Rate (%)",
        "targets": [
          {
            "expr": "rate(http_requests_total{service=\"${service_name}\",status=\"error\"}[5m]) / rate(http_requests_total{service=\"${service_name}\"}[5m]) * 100"
          }
        ]
      },
      {
        "title": "Latency (P50, P95, P99)",
        "targets": [
          {
            "expr": "histogram_quantile(0.50, rate(http_request_duration_seconds_bucket{service=\"${service_name}\"}[5m]))",
            "legendFormat": "P50"
          },
          {
            "expr": "histogram_quantile(0.95, rate(http_request_duration_seconds_bucket{service=\"${service_name}\"}[5m]))",
            "legendFormat": "P95"
          },
          {
            "expr": "histogram_quantile(0.99, rate(http_request_duration_seconds_bucket{service=\"${service_name}\"}[5m]))",
            "legendFormat": "P99"
          }
        ]
      },
      {
        "title": "Event Processing Rate",
        "targets": [
          {
            "expr": "rate(events_consumed_total{service=\"${service_name}\"}[5m])"
          }
        ]
      }
    ]
  }
}
```

### Alertas Estándar

```yaml
# prometheus-alerts.yml
groups:
  - name: service_alerts
    interval: 30s
    rules:
      # Alta tasa de errores
      - alert: HighErrorRate
        expr: |
          rate(http_requests_total{status="error"}[5m]) / rate(http_requests_total[5m]) > 0.05
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High error rate on {{ $labels.service }}"
          description: "Error rate is {{ $value }}% (threshold: 5%)"
      
      # Alta latencia
      - alert: HighLatency
        expr: |
          histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m])) > 1.0
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High latency on {{ $labels.service }}"
          description: "P95 latency is {{ $value }}s (threshold: 1s)"
      
      # Servicio caído
      - alert: ServiceDown
        expr: up == 0
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "Service {{ $labels.instance }} is down"
          description: "Service has been down for more than 1 minute"
      
      # Event processing lag
      - alert: EventProcessingLag
        expr: |
          rate(events_consumed_total{status="error"}[5m]) / rate(events_consumed_total[5m]) > 0.10
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High event processing error rate"
          description: "Event error rate is {{ $value }}% (threshold: 10%)"
```

## Testing de Observabilidad

### Unit Tests para Métricas

```python
# tests/test_metrics.py
import pytest
from prometheus_client import REGISTRY
from app.core.metrics import http_requests_total

def test_http_request_counter_incremented():
    """Valida que el counter de requests se incremente correctamente"""
    
    # Obtener valor inicial
    initial_value = http_requests_total.labels(
        method='GET',
        endpoint='/api/test',
        status='success'
    )._value.get()
    
    # Realizar operación que incrementa métrica
    http_requests_total.labels(
        method='GET',
        endpoint='/api/test',
        status='success'
    ).inc()
    
    # Validar incremento
    final_value = http_requests_total.labels(
        method='GET',
        endpoint='/api/test',
        status='success'
    )._value.get()
    
    assert final_value == initial_value + 1

def test_metrics_endpoint_exposed():
    """Valida que el endpoint /metrics esté expuesto"""
    from fastapi.testclient import TestClient
    from app.main import app
    
    client = TestClient(app)
    response = client.get("/metrics")
    
    assert response.status_code == 200
    assert "http_requests_total" in response.text
    assert "# HELP" in response.text  # Prometheus format
```

### Integration Tests para Traces

```python
# tests/test_traces.py
import pytest
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from opentelemetry.sdk.trace.export.in_memory_span_exporter import InMemorySpanExporter

@pytest.fixture
def span_exporter():
    """Fixture para capturar spans en memoria"""
    exporter = InMemorySpanExporter()
    provider = TracerProvider()
    provider.add_span_processor(SimpleSpanProcessor(exporter))
    trace.set_tracer_provider(provider)
    
    yield exporter
    
    exporter.clear()

def test_span_created_for_operation(span_exporter):
    """Valida que se cree un span para una operación"""
    tracer = trace.get_tracer(__name__)
    
    with tracer.start_as_current_span("test_operation") as span:
        span.set_attribute("test.attribute", "value")
    
    spans = span_exporter.get_finished_spans()
    
    assert len(spans) == 1
    assert spans[0].name == "test_operation"
    assert spans[0].attributes["test.attribute"] == "value"

def test_trace_context_propagated(span_exporter):
    """Valida propagación de trace context"""
    tracer = trace.get_tracer(__name__)
    
    with tracer.start_as_current_span("parent") as parent_span:
        parent_trace_id = parent_span.get_span_context().trace_id
        
        with tracer.start_as_current_span("child") as child_span:
            child_trace_id = child_span.get_span_context().trace_id
    
    # Validar que parent y child tengan el mismo trace_id
    assert parent_trace_id == child_trace_id
    
    spans = span_exporter.get_finished_spans()
    assert len(spans) == 2
```

### Tests de Logs Estructurados

```python
# tests/test_logging.py
import pytest
import json
import structlog
from io import StringIO

def test_structured_logs_format():
    """Valida formato JSON de logs estructurados"""
    output = StringIO()
    
    # Configurar logger para escribir a StringIO
    structlog.configure(
        processors=[
            structlog.processors.JSONRenderer()
        ],
        wrapper_class=structlog.BoundLogger,
        logger_factory=structlog.PrintLoggerFactory(file=output),
    )
    
    logger = structlog.get_logger()
    logger.info("test_event", user_id="123", action="test")
    
    # Parsear output como JSON
    log_line = output.getvalue().strip()
    log_data = json.loads(log_line)
    
    # Validar estructura
    assert log_data["event"] == "test_event"
    assert log_data["user_id"] == "123"
    assert log_data["action"] == "test"
    assert "timestamp" in log_data

def test_correlation_id_in_logs():
    """Valida que correlation_id se incluya en logs"""
    output = StringIO()
    
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.JSONRenderer()
        ],
        logger_factory=structlog.PrintLoggerFactory(file=output),
    )
    
    logger = structlog.get_logger()
    
    # Bind correlation_id
    structlog.contextvars.bind_contextvars(correlation_id="abc-123")
    
    logger.info("test_event")
    
    log_data = json.loads(output.getvalue().strip())
    assert log_data["correlation_id"] == "abc-123"
```

## Troubleshooting

### Herramientas y Queries Comunes

#### Prometheus Queries

```promql
# Top 10 endpoints con más errores
topk(10, sum by (endpoint) (rate(http_requests_total{status="error"}[5m])))

# Latencia P95 por endpoint
histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))

# Tasa de errores por servicio
sum by (service) (rate(http_requests_total{status="error"}[5m])) /
sum by (service) (rate(http_requests_total[5m]))

# Throughput total del sistema
sum(rate(http_requests_total[5m]))

# Eventos con mayor tiempo de procesamiento
topk(10, rate(event_processing_duration_seconds_sum[5m]) /
         rate(event_processing_duration_seconds_count[5m]))
```

#### Loki Queries (LogQL)

```logql
# Todos los errores en últimas 1h
{service="spotify-integration-api"} |= "level=error" | json

# Errores específicos de autenticación
{service="spotify-integration-api"} 
  |= "spotify_authentication_failed" 
  | json 
  | user_id != ""

# Requests lentos (>1s)
{service="playback-control-api"} 
  | json 
  | duration_ms > 1000

# Contar errores por tipo
sum by (error_type) (
  rate({service="spotify-integration-api"} 
    |= "level=error" 
    | json 
    | __error__="" [5m])
)
```

### Debugging de Problemas Comunes

#### 1. Alta Latencia

```python
# Checklist:
# - Revisar P95/P99 latency en dashboard
# - Identificar endpoint lento en Grafana
# - Buscar trace específico en Jaeger
# - Analizar spans dentro del trace
# - Revisar queries DB lentas
# - Verificar external API calls lentas

# Query Prometheus para identificar slow endpoints:
# topk(5, histogram_quantile(0.95, 
#   rate(http_request_duration_seconds_bucket[5m])))
```

#### 2. Errores Frecuentes

```python
# Checklist:
# - Revisar error rate en dashboard
# - Filtrar logs por level=error
# - Agrupar errores por tipo
# - Buscar patrones comunes (correlation_id, user_id)
# - Revisar traces de requests fallidos

# Query Loki para agrupar errores:
# sum by (error_type) (count_over_time(
#   {service="api"} |= "level=error" | json [1h]))
```

#### 3. Performance Degradation

```python
# Checklist:
# - Comparar métricas actuales vs baseline
# - Revisar resource utilization (CPU, memory)
# - Analizar distributed traces para bottlenecks
# - Verificar database connection pool
# - Revisar external dependencies

# Query para comparar latency vs semana pasada:
# histogram_quantile(0.95, 
#   rate(http_request_duration_seconds_bucket[5m]))
# vs
# histogram_quantile(0.95, 
#   rate(http_request_duration_seconds_bucket[5m] offset 7d))
```

## Checklist de Implementación

### ✅ Setup Inicial

- [ ] Stack de observabilidad desplegado (Prometheus, Grafana, Jaeger, Loki)
- [ ] OpenTelemetry Collector configurado
- [ ] Service discovery configurado en Prometheus
- [ ] Dashboards base importados en Grafana
- [ ] Alertas básicas configuradas

### ✅ Por Servicio

#### Instrumentación
- [ ] OpenTelemetry SDK instalado
- [ ] Tracer configurado y tracer provider registrado
- [ ] Meter configurado para métricas
- [ ] Logs estructurados con structlog configurados
- [ ] FastAPI auto-instrumentado

#### Endpoints
- [ ] `/metrics` endpoint expuesto para Prometheus
- [ ] `/health` endpoint para health checks
- [ ] Todos los endpoints REST instrumentados con traces
- [ ] RED metrics implementadas (rate, errors, duration)

#### Event Handlers
- [ ] Event handlers instrumentados con spans
- [ ] Trace context propagado en eventos
- [ ] Metrics de event processing implementadas
- [ ] Logs estructurados en procesamiento de eventos

#### Database
- [ ] Queries instrumentadas con spans
- [ ] Connection pool metrics expuestas
- [ ] Query duration metrics implementadas

#### External APIs
- [ ] Llamadas a APIs externas instrumentadas
- [ ] Timeouts y retries medidos
- [ ] Errores trackeados

### ✅ Documentación

- [ ] Métricas documentadas en README del servicio
- [ ] Dashboard de servicio creado en Grafana
- [ ] Runbooks para alertas creados
- [ ] Troubleshooting guide actualizado
- [ ] **API Documentation** (Backend):
  - [ ] OpenAPI/Swagger accesible en `/docs` y `/redoc`
  - [ ] Todos los endpoints tienen docstrings descriptivos
  - [ ] Modelos Pydantic con descriptions y ejemplos
  - [ ] Tags para agrupar endpoints relacionados
  - [ ] Documentación adicional en Reflect u otra herramienta (opcional)
- [ ] **Component Documentation** (Frontend):
  - [ ] Storybook configurado con todos los componentes públicos
  - [ ] Props documentadas con JSDoc/TSDoc
  - [ ] Stories para variantes comunes

### ✅ Testing

- [ ] Unit tests para métricas
- [ ] Integration tests para traces
- [ ] Tests de logs estructurados
- [ ] Tests de propagación de context

### ✅ Monitoreo

- [ ] Alertas configuradas en Prometheus
- [ ] Notificaciones configuradas (Slack, email, PagerDuty)
- [ ] SLOs definidos
- [ ] Dashboard de equipo configurado

## Referencias

- [OpenTelemetry Python Documentation](https://opentelemetry.io/docs/instrumentation/python/)
- [Prometheus Best Practices](https://prometheus.io/docs/practices/naming/)
- [Grafana Dashboard Best Practices](https://grafana.com/docs/grafana/latest/best-practices/dashboard-design/)
- [Structlog Documentation](https://www.structlog.org/)
- [The RED Method](https://www.weave.works/blog/the-red-method-key-metrics-for-microservices-architecture/)
- [Distributed Tracing Best Practices](https://www.jaegertracing.io/docs/latest/best-practices/)

---

**Última actualización**: 2025-11-14  
**Mantenido por**: Architecture Team
