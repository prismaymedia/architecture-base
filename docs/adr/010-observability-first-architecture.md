# ADR-010: Observability-First Architecture

**Estado**: Aceptado  
**Fecha**: 2025-11-14  
**Contexto**: Arquitectura orientada a observabilidad  

## Contexto y Problema

Los sistemas distribuidos modernos, especialmente aquellos basados en microservicios y arquitectura orientada a eventos, presentan desafíos únicos en cuanto a monitoreo, diagnóstico y resolución de problemas. La complejidad inherente de estos sistemas requiere que la observabilidad sea un principio fundamental desde el diseño, no una consideración secundaria.

Este framework debe ser **observable por diseño**, utilizando tecnologías modernas, gratuitas y open-source para garantizar que cada componente, funcionalidad y servicio pueda ser monitoreado, rastreado y analizado de manera efectiva.

## Decisión

Adoptamos una **arquitectura orientada a observabilidad** como principio rector fundamental del framework. La observabilidad no es opcional: es un **requisito obligatorio** para considerar cualquier funcionalidad como completada.

### Principios Rectores

1. **Observabilidad Total**: Todo componente debe ser observable
2. **Tres Pilares Obligatorios**: Logs, Metrics, Traces en cada servicio
3. **Instrumentación desde el Diseño**: No como agregado posterior
4. **Stack Open-Source**: Solo tecnologías gratuitas y de código abierto
5. **Criterio de Finalización**: La capacidad de observar es criterio de "Done"

### Stack de Observabilidad

#### 1. OpenTelemetry (OTel)
- **Propósito**: Estándar unificado para instrumentación
- **Componentes**:
  - OTel SDK para Python (backend)
  - OTel SDK para JavaScript (frontend)
  - OTel Collector para agregación y exportación
- **Ventajas**:
  - Vendor-neutral
  - Soporta traces, metrics, logs
  - Amplia adopción en la industria
  - Integración nativa con Prometheus, Jaeger, Grafana

#### 2. Prometheus
- **Propósito**: Sistema de monitoreo y base de datos de métricas
- **Métricas a Recolectar**:
  - Request rate, error rate, duration (RED method)
  - Resource utilization (CPU, memory, disk)
  - Custom business metrics
  - Event processing metrics
- **Características**:
  - Pull-based metric collection
  - Powerful query language (PromQL)
  - Alerting con Alertmanager
  - Service discovery integrado

#### 3. Grafana
- **Propósito**: Visualización y dashboards
- **Uso**:
  - Dashboards en tiempo real
  - Alertas visuales
  - Múltiples fuentes de datos (Prometheus, Loki, Jaeger)
  - Templating para servicios similares
- **Dashboards Estándar**:
  - Service Overview (RED metrics)
  - Infrastructure Overview
  - Event Processing Dashboard
  - Business Metrics Dashboard

#### 4. Jaeger
- **Propósito**: Distributed tracing
- **Características**:
  - Rastreo de solicitudes end-to-end
  - Visualización de dependencias entre servicios
  - Análisis de latencia
  - Root cause analysis
- **Integración**:
  - Via OpenTelemetry Collector
  - Context propagation automático
  - Sampling configurable

#### 5. Loki
- **Propósito**: Log aggregation (similar a Prometheus para logs)
- **Características**:
  - Indexación eficiente por labels
  - Query language similar a PromQL (LogQL)
  - Integración nativa con Grafana
  - Storage eficiente

#### 6. Promtail
- **Propósito**: Agent para enviar logs a Loki
- **Características**:
  - Tail de archivos de log
  - Parsing y labeling automático
  - Integración con systemd, Docker, Kubernetes

## Implementación Obligatoria

### Para cada Microservicio Backend (Python/FastAPI)

```python
# Estructura obligatoria de instrumentación
from opentelemetry import trace, metrics
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from prometheus_client import Counter, Histogram, Gauge
import structlog

# 1. Configuración de Traces (Jaeger via OTel)
tracer = trace.get_tracer(__name__)

# 2. Configuración de Metrics (Prometheus)
http_requests_total = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

http_request_duration_seconds = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration',
    ['method', 'endpoint']
)

# 3. Configuración de Logs (Loki via structlog)
logger = structlog.get_logger()
```

### Para cada Endpoint REST

```python
@app.post("/api/orders")
@tracer.start_as_current_span("create_order")
async def create_order(order: OrderCreate):
    span = trace.get_current_span()
    span.set_attribute("order.id", order.id)
    
    # Logging estructurado con contexto
    logger.info("order_creation_started", 
                order_id=order.id,
                user_id=order.user_id)
    
    with http_request_duration_seconds.labels(
        method='POST', 
        endpoint='/api/orders'
    ).time():
        try:
            result = await order_service.create(order)
            http_requests_total.labels(
                method='POST',
                endpoint='/api/orders',
                status='success'
            ).inc()
            
            logger.info("order_creation_completed",
                       order_id=order.id,
                       duration_ms=span.elapsed_ms)
            return result
            
        except Exception as e:
            http_requests_total.labels(
                method='POST',
                endpoint='/api/orders',
                status='error'
            ).inc()
            
            logger.error("order_creation_failed",
                        order_id=order.id,
                        error=str(e),
                        exc_info=True)
            span.record_exception(e)
            raise
```

### Para Event Handlers

```python
@event_handler("OrderCreatedEvent")
@tracer.start_as_current_span("handle_order_created")
async def handle_order_created(event: OrderCreatedEvent):
    span = trace.get_current_span()
    span.set_attribute("event.type", "OrderCreatedEvent")
    span.set_attribute("event.id", event.id)
    span.set_attribute("correlation_id", event.correlation_id)
    
    logger.info("event_processing_started",
                event_type="OrderCreatedEvent",
                event_id=event.id,
                correlation_id=event.correlation_id)
    
    event_processing_duration.labels(
        event_type='OrderCreatedEvent'
    ).observe(time.time())
    
    try:
        await process_order_created(event)
        
        event_processing_total.labels(
            event_type='OrderCreatedEvent',
            status='success'
        ).inc()
        
        logger.info("event_processing_completed",
                   event_type="OrderCreatedEvent",
                   event_id=event.id)
    except Exception as e:
        event_processing_total.labels(
            event_type='OrderCreatedEvent',
            status='error'
        ).inc()
        
        logger.error("event_processing_failed",
                    event_type="OrderCreatedEvent",
                    event_id=event.id,
                    error=str(e),
                    exc_info=True)
        raise
```

### Para Frontend (React)

```typescript
// Instrumentación con OTel para navegador
import { WebTracerProvider } from '@opentelemetry/sdk-trace-web';
import { getWebAutoInstrumentations } from '@opentelemetry/auto-instrumentations-web';
import { ConsoleSpanExporter } from '@opentelemetry/sdk-trace-base';

// Custom metrics hook
function useMetrics() {
  const recordPageView = (pageName: string) => {
    // Send metric to backend or collection endpoint
    fetch('/api/metrics', {
      method: 'POST',
      body: JSON.stringify({
        metric: 'page_view',
        page: pageName,
        timestamp: Date.now()
      })
    });
  };
  
  return { recordPageView };
}
```

## Estándares de Observabilidad

### 1. Logs Estructurados

**Formato Obligatorio**:
```json
{
  "timestamp": "2025-11-14T22:05:36.209Z",
  "level": "info",
  "service": "spotify-integration-api",
  "correlation_id": "abc-123-def",
  "trace_id": "8e42f1a2b3c4d5e6",
  "span_id": "f7g8h9i0j1k2",
  "message": "user_authenticated",
  "user_id": "user123",
  "spotify_user_id": "spotify456",
  "duration_ms": 142
}
```

**Campos Obligatorios**:
- `timestamp`: ISO 8601
- `level`: debug, info, warning, error, critical
- `service`: Nombre del servicio
- `correlation_id`: ID de correlación para rastreo
- `trace_id`: OpenTelemetry trace ID
- `span_id`: OpenTelemetry span ID
- `message`: Mensaje descriptivo en snake_case

### 2. Métricas Obligatorias

#### RED Metrics (Request/Rate/Error/Duration)
```python
# Request Rate
http_requests_total

# Error Rate
http_requests_failed_total

# Duration
http_request_duration_seconds
```

#### Event Processing Metrics
```python
# Event rate
events_published_total{event_type="OrderCreatedEvent"}
events_consumed_total{event_type="OrderCreatedEvent"}

# Event processing duration
event_processing_duration_seconds{event_type="OrderCreatedEvent"}

# Event processing errors
event_processing_errors_total{event_type="OrderCreatedEvent"}
```

#### Business Metrics
```python
# Ejemplos específicos del dominio
orders_created_total
payment_approved_total
spotify_tracks_played_total
dj_sessions_active
```

#### Infrastructure Metrics (automáticas con exporters)
- CPU utilization
- Memory utilization
- Disk I/O
- Network I/O

### 3. Traces Obligatorias

**Contexto de Propagación**:
- Cada request HTTP debe tener un trace ID
- Los eventos deben propagar el trace context
- Correlation ID en todos los logs

**Spans Obligatorios**:
- HTTP request/response
- Database queries
- External API calls
- Event publish/consume
- Business operations

### 4. Dashboards Mínimos Requeridos

#### Service Dashboard
- Request rate (requests/sec)
- Error rate (%)
- P50, P95, P99 latency
- Active connections
- Event processing rate

#### Infrastructure Dashboard
- CPU usage per service
- Memory usage per service
- Disk usage
- Network throughput

#### Business Dashboard
- Domain-specific metrics
- User activity metrics
- Business KPIs

## Arquitectura de Despliegue

```
┌─────────────────────────────────────────────────────────────┐
│                     Application Layer                       │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │Service 1 │  │Service 2 │  │Service 3 │  │Service 4 │   │
│  │(OTel SDK)│  │(OTel SDK)│  │(OTel SDK)│  │(OTel SDK)│   │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘   │
│       │             │             │             │          │
│       └─────────────┴─────────────┴─────────────┘          │
│                          │                                  │
└──────────────────────────┼──────────────────────────────────┘
                           │
                           ▼
              ┌────────────────────────┐
              │  OpenTelemetry         │
              │  Collector             │
              │  (Aggregation Layer)   │
              └────────┬───────────────┘
                       │
         ┌─────────────┼─────────────┐
         │             │             │
         ▼             ▼             ▼
    ┌────────┐   ┌─────────┐   ┌────────┐
    │Promethe│   │ Jaeger  │   │  Loki  │
    │  us    │   │(Traces) │   │ (Logs) │
    │(Metrics│   └─────────┘   └────────┘
    │)       │         │             │
    └────┬───┘         │             │
         │             │             │
         └─────────────┴─────────────┘
                       │
                       ▼
              ┌─────────────────┐
              │    Grafana      │
              │  (Visualization)│
              └─────────────────┘
```

## Criterios de Éxito

Una funcionalidad o servicio solo se considera **COMPLETO** cuando:

### ✅ Criterios Obligatorios

1. **Traces Implementadas**:
   - [ ] Instrumentación con OpenTelemetry SDK
   - [ ] Trace propagation entre servicios
   - [ ] Spans en operaciones críticas
   - [ ] Context propagation en eventos

2. **Metrics Implementadas**:
   - [ ] RED metrics (rate, errors, duration)
   - [ ] Event processing metrics
   - [ ] Business metrics relevantes
   - [ ] Prometheus endpoint expuesto (`/metrics`)

3. **Logs Implementados**:
   - [ ] Logs estructurados con structlog (Python) o similar
   - [ ] Correlation IDs en todos los logs
   - [ ] Trace/Span IDs vinculados
   - [ ] Log levels apropiados

4. **Dashboards Creados**:
   - [ ] Dashboard de servicio en Grafana
   - [ ] Alertas configuradas para errores críticos
   - [ ] Visualizaciones de métricas clave

5. **Documentación**:
   - [ ] Métricas documentadas
   - [ ] Traces documentadas
   - [ ] Runbooks para alertas
   - [ ] Troubleshooting guide

6. **Testing de Observabilidad**:
   - [ ] Tests que validan emisión de metrics
   - [ ] Tests que validan creación de traces
   - [ ] Tests que validan logs estructurados

## Consecuencias

### Ventajas ✅

1. **Visibilidad Total**: Capacidad de observar el comportamiento de todo el sistema
2. **Debugging Eficiente**: Reducción de tiempo en resolución de problemas
3. **Proactividad**: Detección temprana de problemas antes de impactar usuarios
4. **Confiabilidad**: Métricas objetivas de SLOs/SLAs
5. **Optimización**: Identificación de bottlenecks y oportunidades de mejora
6. **Auditoría**: Trazabilidad completa de operaciones
7. **Open-Source**: Sin costos de licenciamiento, comunidad activa

### Desafíos ⚠️

1. **Overhead Inicial**: Más código y configuración al inicio
2. **Curva de Aprendizaje**: Equipo debe aprender las herramientas
3. **Infraestructura**: Necesidad de desplegar stack de observabilidad
4. **Storage**: Métricas, logs y traces consumen espacio
5. **Performance**: Instrumentación tiene overhead (mitigable con sampling)

### Mitigación de Desafíos

- **Templates y generadores**: Crear templates con instrumentación incluida
- **Capacitación**: Documentación y workshops sobre observabilidad
- **Automatización**: Scripts de despliegue del stack
- **Sampling inteligente**: Configurar sampling rates apropiados
- **Retention policies**: Políticas de retención de datos configurables

## Métricas de Adopción

Mediremos el éxito de esta decisión con:

1. **Coverage**: % de servicios con observabilidad completa
2. **MTTR**: Tiempo medio de resolución de problemas (debe reducirse)
3. **MTTD**: Tiempo medio de detección de problemas (debe reducirse)
4. **Adoption**: % del equipo capacitado en herramientas
5. **Usage**: % de incidents diagnosticados con herramientas de observabilidad

## Referencias

- [OpenTelemetry Documentation](https://opentelemetry.io/docs/)
- [Prometheus Best Practices](https://prometheus.io/docs/practices/naming/)
- [Grafana Dashboards](https://grafana.com/grafana/dashboards/)
- [Jaeger Architecture](https://www.jaegertracing.io/docs/latest/architecture/)
- [The Three Pillars of Observability](https://www.oreilly.com/library/view/distributed-systems-observability/9781492033431/)
- [RED Method](https://grafana.com/blog/2018/08/02/the-red-method-how-to-instrument-your-services/)
- [Observability Guide](../guides/observability-best-practices.md)

## Historial de Revisiones

- **2025-11-14**: Creación inicial - Establecimiento de arquitectura observability-first
