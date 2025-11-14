# Catálogo de Eventos del Sistema

Este directorio contiene la especificación completa de todos los eventos que se publican y consumen en el sistema de microservicios.

## Propósito

El catálogo de eventos sirve como:
- **Contrato entre servicios**: Define la estructura que todos deben respetar
- **Documentación centralizada**: Un solo lugar para ver todos los eventos
- **Versionado**: Rastrea cambios en eventos a través del tiempo
- **Descubrimiento**: Facilita encontrar eventos existentes antes de crear nuevos

## Estructura

Cada evento está documentado con:
- **Nombre del evento**
- **Productor**: Qué servicio lo publica
- **Consumidores**: Qué servicios lo consumen
- **Schema**: Estructura del payload (JSON Schema)
- **Versión**: Versionado semántico
- **Cuándo se publica**: Trigger del evento
- **Ejemplo**: Payload de ejemplo

## Eventos por Servicio

### Orders API

#### Eventos Publicados

| Evento | Versión | Consumidores |
|--------|---------|--------------|
| [OrderCreatedEvent](orders/OrderCreatedEvent.md) | v1.0 | Inventory, Payments, Notifications |
| [OrderConfirmedEvent](orders/OrderConfirmedEvent.md) | v1.0 | Notifications |
| [OrderCancelledEvent](orders/OrderCancelledEvent.md) | v1.0 | Inventory, Notifications |
| [OrderShippedEvent](orders/OrderShippedEvent.md) | v1.0 | Inventory, Notifications |

#### Eventos Consumidos

| Evento | Productor |
|--------|-----------|
| PaymentApprovedEvent | Payments API |
| PaymentRejectedEvent | Payments API |
| InventoryReservedEvent | Inventory API |
| InventoryReservationFailedEvent | Inventory API |

---

### Inventory API

#### Eventos Publicados

| Evento | Versión | Consumidores |
|--------|---------|--------------|
| [InventoryReservedEvent](inventory/InventoryReservedEvent.md) | v1.0 | Orders, Payments |
| [InventoryReservationFailedEvent](inventory/InventoryReservationFailedEvent.md) | v1.0 | Orders, Payments |
| [InventoryReleasedEvent](inventory/InventoryReleasedEvent.md) | v1.0 | Orders |
| [LowStockEvent](inventory/LowStockEvent.md) | v1.0 | Notifications |
| [OutOfStockEvent](inventory/OutOfStockEvent.md) | v1.0 | Notifications |

#### Eventos Consumidos

| Evento | Productor |
|--------|-----------|
| OrderCreatedEvent | Orders API |
| OrderCancelledEvent | Orders API |
| OrderShippedEvent | Orders API |
| PaymentRejectedEvent | Payments API |

---

### Payments API

#### Eventos Publicados

| Evento | Versión | Consumidores |
|--------|---------|--------------|
| [PaymentApprovedEvent](payments/PaymentApprovedEvent.md) | v1.0 | Orders, Notifications |
| [PaymentRejectedEvent](payments/PaymentRejectedEvent.md) | v1.0 | Orders, Inventory, Notifications |
| [PaymentPendingEvent](payments/PaymentPendingEvent.md) | v1.0 | Orders, Notifications |
| [RefundProcessedEvent](payments/RefundProcessedEvent.md) | v1.0 | Orders, Notifications |
| [RefundFailedEvent](payments/RefundFailedEvent.md) | v1.0 | Notifications |

#### Eventos Consumidos

| Evento | Productor |
|--------|-----------|
| OrderCreatedEvent | Orders API |
| OrderCancelledEvent | Orders API |
| InventoryReservationFailedEvent | Inventory API |

---

### Notifications API

#### Eventos Publicados

| Evento | Versión | Consumidores |
|--------|---------|--------------|
| [NotificationSentEvent](notifications/NotificationSentEvent.md) | v1.0 | Analytics |
| [NotificationFailedEvent](notifications/NotificationFailedEvent.md) | v1.0 | Support System |

#### Eventos Consumidos

| Evento | Productor |
|--------|-----------|
| OrderCreatedEvent | Orders API |
| OrderConfirmedEvent | Orders API |
| OrderCancelledEvent | Orders API |
| OrderShippedEvent | Orders API |
| PaymentApprovedEvent | Payments API |
| PaymentRejectedEvent | Payments API |
| RefundProcessedEvent | Payments API |
| LowStockEvent | Inventory API |

---

## Convenciones de Eventos

### Nombrado

- **Formato**: `{Entity}{Action}Event`
- **Tiempo verbal**: Pasado (representa algo que ya ocurrió)
- **Ejemplos**: 
  - ✅ `OrderCreatedEvent`
  - ✅ `PaymentApprovedEvent`
  - ❌ `CreateOrderEvent` (imperativo)
  - ❌ `OrderCreate` (sin sufijo Event)

### Estructura Base

Todos los eventos deben incluir:

```json
{
  "eventId": "guid",           // Identificador único del evento
  "eventType": "string",       // Tipo de evento (ej: OrderCreatedEvent)
  "eventVersion": "string",    // Versión del schema (ej: v1.0)
  "timestamp": "datetime",     // Cuándo ocurrió el evento
  "correlationId": "guid",     // Para rastreo end-to-end
  "causationId": "guid",       // ID del evento que causó este
  "source": "string",          // Servicio que publicó (ej: orders-api)
  "data": {                    // Payload específico del evento
    // ... datos del evento
  }
}
```

### Versionado

- **Formato**: Semver (`v{major}.{minor}`)
- **Major**: Breaking changes (campos removidos, tipos cambiados)
- **Minor**: Cambios backwards compatible (campos nuevos opcionales)

**Estrategia de cambios**:
1. **Non-breaking**: Agregar campos opcionales al final
2. **Breaking**: Crear nueva versión del evento con sufijo (ej: `OrderCreatedEventV2`)
3. Mantener versión anterior por período de migración (mínimo 3 meses)

### Tamaño de Eventos

- **Máximo recomendado**: 256 KB
- **Ideal**: < 10 KB
- Para datos grandes: Incluir referencia/URL, no el dato completo

### Datos Sensibles

❌ **NO incluir**:
- Contraseñas
- Números completos de tarjeta de crédito
- CVV
- SSN u otros identificadores personales sensibles

✅ **Permitido**:
- IDs (UUID)
- Tokens
- Últimos 4 dígitos de tarjeta
- Datos ofuscados/hasheados

## Patrones de Comunicación

### 1. Event Notification
Notificar que algo ocurrió sin incluir todos los detalles.
```
Uso: Notificaciones, triggers simples
Ejemplo: OrderShippedEvent
```

### 2. Event-Carried State Transfer
Incluir toda la información necesaria en el evento.
```
Uso: Cuando consumidores necesitan los datos completos
Ejemplo: OrderCreatedEvent con todos los items
```

### 3. Event Sourcing
Serie de eventos que representan el estado completo.
```
Uso: Auditoría completa, reconstrucción de estado
Ejemplo: Historial de cambios de estado de Order
```

## Garantías de Entrega

### At-Least-Once Delivery
- Los eventos pueden ser entregados más de una vez
- **Handlers deben ser idempotentes**
- Usar `eventId` para deduplicación

### Orden de Eventos
- No se garantiza orden global
- Se garantiza orden por partition key (ej: OrderId)
- Diseñar handlers para manejar eventos desordenados

## Testing de Eventos

### Contract Tests
- Validar schema de eventos
- Verificar backwards compatibility
- Ejecutar en CI para cada cambio

### Integration Tests
- Publicar evento de prueba
- Verificar que consumidores lo procesan correctamente
- End-to-end flow testing

## Monitoreo de Eventos

Métricas clave:
- Eventos publicados por tipo
- Eventos consumidos por servicio
- Latencia de procesamiento
- Tasa de errores
- Dead letter queue size

## Herramientas

### AsyncAPI
Considerar usar AsyncAPI para documentación estructurada de eventos (futuro).

### Schema Registry
Usar un schema registry para validación automática (futuro).

## Migration Guide

Cuando cambias un evento existente:

1. **Análisis de impacto**: Identificar todos los consumidores
2. **Comunicación**: Notificar a equipos afectados
3. **Versionado**: Incrementar versión apropiadamente
4. **Migración gradual**: 
   - Publicar ambas versiones temporalmente
   - Migrar consumidores uno por uno
   - Deprecar versión antigua
5. **Documentación**: Actualizar este catálogo

## Referencias

- [Architecture Overview](../architecture/README.md)
- [Saga Pattern](../guides/saga-pattern.md)
- [Event-Driven Patterns](../guides/event-driven-patterns.md)
- [Testing Guide](../guides/testing.md)
