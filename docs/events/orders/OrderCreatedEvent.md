# OrderCreatedEvent

## Metadata

- **Event Type**: `OrderCreatedEvent`
- **Version**: `v1.0`
- **Producer**: Orders API
- **Consumers**: Inventory API, Payments API, Notifications API
- **Status**: Active

## Descripción

Este evento se publica cuando un cliente crea un nuevo pedido en el sistema. Contiene toda la información del pedido incluyendo items, dirección de envío y datos del cliente.

## Cuándo se Publica

- Un cliente completa el checkout y crea un pedido
- El pedido se guarda exitosamente en la base de datos de Orders
- Antes de que se procese el pago o se reserve inventario

## Schema

### Envelope (Base Event Structure)

```json
{
  "eventId": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "eventType": "OrderCreatedEvent",
  "eventVersion": "v1.0",
  "timestamp": "2025-11-14T10:30:00Z",
  "correlationId": "7c9e6679-7425-40de-944b-e07fc1f90ae7",
  "causationId": null,
  "source": "orders-api",
  "data": {
    // Ver estructura abajo
  }
}
```

### Data Payload

```json
{
  "orderId": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "customerId": "b2c3d4e5-f6a7-8901-bcde-f12345678901",
  "orderNumber": "ORD-2025-001234",
  "orderDate": "2025-11-14T10:30:00Z",
  "status": "Pending",
  "currency": "USD",
  "subtotal": 150.00,
  "tax": 15.00,
  "shipping": 10.00,
  "discount": 0.00,
  "totalAmount": 175.00,
  "items": [
    {
      "orderItemId": "c3d4e5f6-a7b8-9012-cdef-123456789012",
      "productId": "d4e5f6a7-b8c9-0123-def1-234567890123",
      "productName": "Product Name",
      "sku": "PROD-001",
      "quantity": 2,
      "unitPrice": 50.00,
      "totalPrice": 100.00
    },
    {
      "orderItemId": "e5f6a7b8-c9d0-1234-ef12-345678901234",
      "productId": "f6a7b8c9-d0e1-2345-f123-456789012345",
      "productName": "Another Product",
      "sku": "PROD-002",
      "quantity": 1,
      "unitPrice": 50.00,
      "totalPrice": 50.00
    }
  ],
  "shippingAddress": {
    "recipientName": "John Doe",
    "addressLine1": "123 Main Street",
    "addressLine2": "Apt 4B",
    "city": "New York",
    "state": "NY",
    "postalCode": "10001",
    "country": "USA",
    "phoneNumber": "+1-555-0123"
  },
  "billingAddress": {
    "recipientName": "John Doe",
    "addressLine1": "123 Main Street",
    "addressLine2": "Apt 4B",
    "city": "New York",
    "state": "NY",
    "postalCode": "10001",
    "country": "USA"
  },
  "paymentMethod": {
    "type": "CreditCard",
    "lastFourDigits": "4242",
    "cardBrand": "Visa"
  },
  "customerEmail": "john.doe@example.com",
  "customerPhone": "+1-555-0123",
  "notes": "Please ring doorbell"
}
```

## JSON Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": [
    "orderId",
    "customerId",
    "orderNumber",
    "orderDate",
    "status",
    "totalAmount",
    "items",
    "shippingAddress",
    "customerEmail"
  ],
  "properties": {
    "orderId": {
      "type": "string",
      "format": "uuid",
      "description": "Identificador único del pedido"
    },
    "customerId": {
      "type": "string",
      "format": "uuid",
      "description": "Identificador del cliente"
    },
    "orderNumber": {
      "type": "string",
      "pattern": "^ORD-[0-9]{4}-[0-9]{6}$",
      "description": "Número de pedido legible"
    },
    "orderDate": {
      "type": "string",
      "format": "date-time",
      "description": "Fecha y hora de creación del pedido"
    },
    "status": {
      "type": "string",
      "enum": ["Pending"],
      "description": "Estado del pedido (siempre Pending al crear)"
    },
    "currency": {
      "type": "string",
      "default": "USD",
      "description": "Moneda del pedido"
    },
    "subtotal": {
      "type": "number",
      "minimum": 0,
      "description": "Subtotal antes de impuestos y envío"
    },
    "tax": {
      "type": "number",
      "minimum": 0,
      "description": "Monto de impuestos"
    },
    "shipping": {
      "type": "number",
      "minimum": 0,
      "description": "Costo de envío"
    },
    "discount": {
      "type": "number",
      "minimum": 0,
      "description": "Descuentos aplicados"
    },
    "totalAmount": {
      "type": "number",
      "minimum": 0,
      "description": "Monto total del pedido"
    },
    "items": {
      "type": "array",
      "minItems": 1,
      "description": "Items del pedido"
    },
    "shippingAddress": {
      "type": "object",
      "required": ["recipientName", "addressLine1", "city", "country"],
      "description": "Dirección de envío"
    },
    "customerEmail": {
      "type": "string",
      "format": "email",
      "description": "Email del cliente"
    }
  }
}
```

## Acciones de Consumidores

### Inventory API
1. Recibe el evento `OrderCreatedEvent`
2. Valida disponibilidad de todos los productos en `items`
3. Si hay stock:
   - Reserva el inventario
   - Publica `InventoryReservedEvent`
4. Si no hay stock:
   - Publica `InventoryReservationFailedEvent`

### Payments API
1. Recibe el evento `OrderCreatedEvent`
2. Valida método de pago
3. Espera confirmación de que inventario está reservado
4. Procesa el pago con la pasarela
5. Publica `PaymentApprovedEvent` o `PaymentRejectedEvent`

### Notifications API
1. Recibe el evento `OrderCreatedEvent`
2. Envía email de confirmación de pedido al `customerEmail`
3. Envía push notification si el usuario tiene app móvil
4. Publica `NotificationSentEvent`

## Idempotencia

Los consumidores deben verificar si ya procesaron este `orderId` para evitar duplicados.

**Estrategia recomendada**:
```
- Usar orderId como deduplication key
- Almacenar en cache/DB los eventos procesados
- TTL de 24 horas para la cache
```

## Ejemplo de Uso

### Publicación (C#)
```csharp
// NOTA: Este es un ejemplo conceptual, no código real
var orderCreatedEvent = new OrderCreatedEvent
{
    EventId = Guid.NewGuid(),
    EventType = "OrderCreatedEvent",
    EventVersion = "v1.0",
    Timestamp = DateTime.UtcNow,
    CorrelationId = correlationId,
    Source = "orders-api",
    Data = new OrderCreatedData
    {
        OrderId = order.Id,
        CustomerId = order.CustomerId,
        // ... otros campos
    }
};

await eventBus.PublishAsync(orderCreatedEvent);
```

### Consumo (C#)
```csharp
// NOTA: Este es un ejemplo conceptual, no código real
public class OrderCreatedEventHandler : IEventHandler<OrderCreatedEvent>
{
    public async Task HandleAsync(OrderCreatedEvent @event)
    {
        // Verificar idempotencia
        if (await IsAlreadyProcessed(@event.Data.OrderId))
            return;

        // Procesar evento
        await ReserveInventory(@event.Data.Items);

        // Marcar como procesado
        await MarkAsProcessed(@event.Data.OrderId);
    }
}
```

## Versionado

### v1.0 (Actual)
- Versión inicial del evento
- Incluye todos los campos documentados arriba

### Cambios Planeados

No hay cambios planeados actualmente.

## Consideraciones

- **Tamaño**: Aproximadamente 2-5 KB por evento
- **Frecuencia**: Variable según tráfico de pedidos
- **Criticidad**: Alta - Es el trigger de todo el flujo de negocio
- **TTL**: Los eventos deben procesarse dentro de 5 minutos

## Troubleshooting

### Problema: Evento no es consumido
- Verificar que la cola existe
- Verificar permisos del consumidor
- Revisar logs del event bus

### Problema: Datos inconsistentes
- Validar schema antes de publicar
- Verificar que totalAmount = subtotal + tax + shipping - discount

## Referencias

- [Orders API Context](../../services/orders-api/.copilot-context.md)
- [Event Catalog](../README.md)
- [Saga Pattern](../../guides/saga-pattern.md)
