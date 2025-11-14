# Arquitectura del Sistema

## Visión General

Sistema de e-commerce distribuido basado en microservicios con arquitectura orientada a eventos. Cada servicio es independiente, escalable y se comunica mediante eventos asíncronos para garantizar bajo acoplamiento y alta cohesión.

## Diagrama de Arquitectura

```
┌─────────────────────────────────────────────────────────────┐
│                        API Gateway                          │
│                    (IIS Load Balancer)                      │
└────────┬──────────────┬──────────────┬──────────────────────┘
         │              │              │
         ▼              ▼              ▼
┌────────────────┐ ┌────────────────┐ ┌────────────────┐
│   Orders API   │ │ Inventory API  │ │  Payments API  │
│    (IIS)       │ │    (IIS)       │ │    (IIS)       │
└────────┬───────┘ └────────┬───────┘ └────────┬───────┘
         │                  │                  │
         └──────────────────┼──────────────────┘
                            │
                     ┌──────▼──────┐
                     │  Event Bus  │
                     │  (RabbitMQ/ │
                     │Service Bus) │
                     └──────┬──────┘
                            │
                     ┌──────▼──────────┐
                     │ Notifications   │
                     │     API         │
                     │    (IIS)        │
                     └─────────────────┘
```

## Microservicios

### 1. Orders API
**Responsabilidad**: Gestionar el ciclo de vida de pedidos

**Dominio**:
- Creación de órdenes
- Actualización de estado de órdenes
- Consulta de historial de pedidos
- Validación de datos de orden

**Eventos Publicados**:
- `OrderCreatedEvent`: Cuando se crea un nuevo pedido
- `OrderConfirmedEvent`: Cuando el pago es confirmado
- `OrderCancelledEvent`: Cuando se cancela un pedido
- `OrderShippedEvent`: Cuando se envía el pedido

**Eventos Consumidos**:
- `PaymentApprovedEvent`: Para confirmar la orden
- `PaymentRejectedEvent`: Para cancelar la orden
- `InventoryReservedEvent`: Para validar disponibilidad

**Base de Datos**: SQL Server (OrdersDB)

---

### 2. Inventory API
**Responsabilidad**: Gestionar inventario y disponibilidad de productos

**Dominio**:
- Control de stock
- Reserva de productos
- Liberación de inventario
- Actualización de cantidades

**Eventos Publicados**:
- `InventoryReservedEvent`: Cuando se reserva stock
- `InventoryReleasedEvent`: Cuando se libera stock
- `LowStockEvent`: Cuando el stock está bajo
- `OutOfStockEvent`: Cuando no hay stock

**Eventos Consumidos**:
- `OrderCreatedEvent`: Para reservar inventario
- `OrderCancelledEvent`: Para liberar inventario
- `OrderShippedEvent`: Para confirmar salida de stock

**Base de Datos**: SQL Server (InventoryDB)

---

### 3. Payments API
**Responsabilidad**: Procesar pagos y transacciones financieras

**Dominio**:
- Procesamiento de pagos
- Validación de medios de pago
- Gestión de reembolsos
- Integración con pasarelas de pago

**Eventos Publicados**:
- `PaymentApprovedEvent`: Cuando el pago es exitoso
- `PaymentRejectedEvent`: Cuando el pago falla
- `RefundProcessedEvent`: Cuando se procesa un reembolso
- `PaymentPendingEvent`: Cuando el pago está pendiente

**Eventos Consumidos**:
- `OrderCreatedEvent`: Para iniciar proceso de pago
- `OrderCancelledEvent`: Para procesar reembolso

**Base de Datos**: SQL Server (PaymentsDB)

---

### 4. Notifications API
**Responsabilidad**: Enviar notificaciones a usuarios y sistemas externos

**Dominio**:
- Envío de emails
- Notificaciones push
- SMS
- Webhooks a sistemas externos

**Eventos Publicados**:
- `NotificationSentEvent`: Cuando se envía una notificación
- `NotificationFailedEvent`: Cuando falla el envío

**Eventos Consumidos**:
- `OrderCreatedEvent`: Notificar al cliente
- `OrderConfirmedEvent`: Confirmar pedido
- `PaymentApprovedEvent`: Confirmar pago
- `PaymentRejectedEvent`: Notificar rechazo
- `OrderShippedEvent`: Notificar envío
- `OrderCancelledEvent`: Notificar cancelación

**Base de Datos**: SQL Server (NotificationsDB)

---

## Patrones Arquitectónicos

### Event-Driven Architecture

**Ventajas**:
- Desacoplamiento entre servicios
- Escalabilidad independiente
- Resiliencia ante fallos
- Facilita auditoría y trazabilidad

**Implementación**:
- Message broker: RabbitMQ / Azure Service Bus
- Event Store para Event Sourcing (opcional)
- Dead Letter Queue para eventos fallidos
- Retry policies automáticos

### Saga Pattern

Para transacciones distribuidas utilizamos el patrón Saga orquestado:

**Ejemplo: Proceso de Creación de Orden**

```
1. Orders API recibe request → Publica OrderCreatedEvent
2. Inventory API consume evento → Reserva stock → Publica InventoryReservedEvent
3. Payments API consume evento → Procesa pago → Publica PaymentApprovedEvent
4. Orders API consume evento → Confirma orden → Publica OrderConfirmedEvent
5. Notifications API consume evento → Envía confirmación
```

**Compensación en caso de fallo**:
```
Si Payment falla:
1. Payments API → Publica PaymentRejectedEvent
2. Inventory API → Libera stock → Publica InventoryReleasedEvent
3. Orders API → Cancela orden → Publica OrderCancelledEvent
4. Notifications API → Notifica cancelación
```

### CQRS (Command Query Responsibility Segregation)

Separación entre operaciones de escritura (commands) y lectura (queries):

- **Commands**: Modifican estado y publican eventos
- **Queries**: Consultas optimizadas desde read models

### Database per Service

Cada microservicio tiene su propia base de datos:
- Independencia de datos
- Sin acoplamiento a nivel de base de datos
- Cada servicio elige su tecnología de persistencia
- Consistencia eventual mediante eventos

## Tecnologías

### Desarrollo
- **.NET 8**: Framework principal
- **ASP.NET Core**: Web APIs
- **Entity Framework Core**: ORM
- **MassTransit/NServiceBus**: Mensajería
- **FluentValidation**: Validación
- **AutoMapper**: Mapeo de objetos
- **Serilog**: Logging estructurado

### Infraestructura
- **IIS**: Servidor web
- **SQL Server**: Base de datos relacional
- **RabbitMQ / Azure Service Bus**: Message broker
- **Redis**: Caché distribuido
- **Application Insights**: Monitoreo y telemetría

### BIT Components
- **Shared.Contracts**: Contratos de eventos y DTOs
- **Shared.Infrastructure**: Utilidades comunes
- **Shared.Domain**: Value objects compartidos
- **Shared.EventBus**: Abstracciones de mensajería

## Resiliencia y Confiabilidad

### Circuit Breaker
- Polly para implementar circuit breakers
- Timeout de 30 segundos por defecto
- 5 fallos consecutivos para abrir circuito
- 60 segundos para reintentar

### Retry Policies
- Exponential backoff
- Máximo 3 reintentos
- Dead Letter Queue después de fallos

### Health Checks
- Endpoint `/health` en cada servicio
- Verificación de dependencias (DB, message broker)
- Integración con monitoring

### Idempotencia
- Todos los event handlers son idempotentes
- Uso de `MessageId` para deduplicación
- Almacenamiento de eventos procesados

## Seguridad

- **Autenticación**: OAuth 2.0 / JWT
- **Autorización**: Role-based access control
- **Cifrado**: HTTPS para todas las comunicaciones
- **Secretos**: Azure Key Vault / AWS Secrets Manager
- **Rate Limiting**: Por servicio y por usuario

## Observabilidad

### Logging
- Logs estructurados con Serilog
- Correlation ID para rastreo end-to-end
- Niveles: Debug, Info, Warning, Error, Critical

### Métricas
- Contadores de eventos publicados/consumidos
- Latencia de procesamiento
- Tasa de errores
- Health metrics

### Tracing
- Distributed tracing con OpenTelemetry
- Correlación entre servicios
- Visualización en Application Insights

## Escalabilidad

- **Horizontal scaling**: Múltiples instancias por servicio en IIS
- **Particionamiento**: Por región, tipo de cliente, etc.
- **Caché**: Redis para datos frecuentes
- **Rate limiting**: Para proteger servicios

## Referencias

- [Catálogo de Eventos](../events/README.md)
- [Guías de Desarrollo](../guides/README.md)
- [ADRs](../adr/README.md)
