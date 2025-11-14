# Saga Pattern - Guía de Implementación

## ¿Qué es el Saga Pattern?

El Saga Pattern es un patrón de diseño para gestionar transacciones distribuidas en arquitecturas de microservicios. En lugar de usar transacciones ACID tradicionales (que no funcionan bien entre servicios), una Saga coordina una serie de transacciones locales mediante eventos.

## Problema que Resuelve

En microservicios con bases de datos independientes:
- ❌ No puedes usar transacciones distribuidas (2PC)
- ❌ No puedes hacer rollback automático entre servicios
- ❌ Necesitas mantener consistencia eventual

**Solución**: Una secuencia de transacciones locales donde cada paso:
1. Completa su transacción local
2. Publica un evento
3. Trigger del siguiente paso

Si algo falla, ejecutar **transacciones compensatorias** para deshacer cambios.

## Tipos de Saga

### 1. Choreography (Coreografía)

Cada servicio escucha eventos y decide qué hacer. **No hay coordinador central**.

**Ventajas:**
- Simple para flujos cortos
- Bajo acoplamiento
- Sin single point of failure

**Desventajas:**
- Difícil de entender el flujo completo
- Complejidad crece con más pasos
- Difícil de debuggear

**Cuándo usar:**
- Flujos simples (2-3 pasos)
- Alta autonomía de servicios
- Baja interdependencia

### 2. Orchestration (Orquestación)

Un **coordinador central** (Saga Orchestrator) controla el flujo.

**Ventajas:**
- Flujo explícito y fácil de entender
- Fácil de debuggear
- Control centralizado de compensación

**Desventajas:**
- Potencial single point of failure
- Más acoplamiento al orquestador

**Cuándo usar:**
- Flujos complejos (4+ pasos)
- Necesitas visibilidad del estado
- Lógica de compensación compleja

## Nuestro Caso: Order Creation Saga

Usamos **Choreography** para la creación de órdenes porque es un flujo relativamente simple y queremos mantener servicios desacoplados.

### Flujo Happy Path

```
1. Cliente → POST /api/orders
   └─> Orders API crea orden
       └─> Publica: OrderCreatedEvent

2. Inventory API escucha OrderCreatedEvent
   └─> Reserva stock
       └─> Publica: InventoryReservedEvent

3. Payments API escucha OrderCreatedEvent
   └─> Espera InventoryReservedEvent
       └─> Procesa pago
           └─> Publica: PaymentApprovedEvent

4. Orders API escucha PaymentApprovedEvent
   └─> Confirma orden
       └─> Publica: OrderConfirmedEvent

5. Notifications API escucha OrderConfirmedEvent
   └─> Envía confirmación al cliente
```

### Flujo con Fallo (Compensación)

**Escenario: Payment Falla**

```
1-2. [Igual que happy path]

3. Payments API procesa pago
   └─> Payment Gateway rechaza
       └─> Publica: PaymentRejectedEvent

4. Inventory API escucha PaymentRejectedEvent
   └─> Libera reserva (COMPENSACIÓN)
       └─> Publica: InventoryReleasedEvent

5. Orders API escucha PaymentRejectedEvent
   └─> Cancela orden (COMPENSACIÓN)
       └─> Publica: OrderCancelledEvent

6. Notifications API escucha OrderCancelledEvent
   └─> Notifica al cliente
```

**Escenario: No Hay Stock**

```
1. Cliente → POST /api/orders
   └─> Orders API crea orden
       └─> Publica: OrderCreatedEvent

2. Inventory API escucha OrderCreatedEvent
   └─> Verifica stock → NO HAY SUFICIENTE
       └─> Publica: InventoryReservationFailedEvent

3. Payments API escucha InventoryReservationFailedEvent
   └─> NO procesa pago (compensación preventiva)

4. Orders API escucha InventoryReservationFailedEvent
   └─> Cancela orden (COMPENSACIÓN)
       └─> Publica: OrderCancelledEvent

5. Notifications API escucha OrderCancelledEvent
   └─> Notifica al cliente (sin stock)
```

## Implementación

### Estructura de una Saga

**NO CÓDIGO REAL - Solo concepto:**

```csharp
// State Machine para tracking
public enum OrderSagaState
{
    Started,
    InventoryReserved,
    PaymentProcessed,
    OrderConfirmed,
    Completed,
    Failed,
    Compensating,
    Compensated
}

// Saga State Storage
public class OrderSagaState
{
    public Guid OrderId { get; set; }
    public OrderSagaState State { get; set; }
    public DateTime StartedAt { get; set; }
    public DateTime? CompletedAt { get; set; }
    public List<SagaStep> CompletedSteps { get; set; }
    public string FailureReason { get; set; }
}

// Cada paso de la saga
public class SagaStep
{
    public string Name { get; set; }
    public DateTime ExecutedAt { get; set; }
    public string EventId { get; set; }
    public bool IsCompensated { get; set; }
}
```

### Event Handlers

**NO CÓDIGO REAL - Solo concepto:**

```csharp
// En Orders API
public class PaymentApprovedEventHandler : IEventHandler<PaymentApprovedEvent>
{
    public async Task HandleAsync(PaymentApprovedEvent @event)
    {
        // 1. Idempotencia
        if (await IsAlreadyProcessed(@event.EventId))
            return;

        // 2. Obtener orden
        var order = await _orderRepository.GetByIdAsync(@event.OrderId);
        
        // 3. Validar estado (puede estar cancelada por timeout)
        if (order.Status == OrderStatus.Cancelled)
        {
            _logger.Warning("Order already cancelled, ignoring payment approval");
            return;
        }

        // 4. Cambiar estado
        order.Confirm();
        await _orderRepository.UpdateAsync(order);

        // 5. Publicar evento
        await _eventBus.PublishAsync(new OrderConfirmedEvent
        {
            OrderId = order.Id,
            ConfirmedAt = DateTime.UtcNow
        });

        // 6. Marcar como procesado
        await MarkAsProcessed(@event.EventId);
    }
}

// Compensación en Inventory API
public class PaymentRejectedEventHandler : IEventHandler<PaymentRejectedEvent>
{
    public async Task HandleAsync(PaymentRejectedEvent @event)
    {
        // 1. Idempotencia
        if (await IsAlreadyProcessed(@event.EventId))
            return;

        // 2. Buscar reserva
        var reservation = await _reservationRepository
            .GetByOrderIdAsync(@event.OrderId);

        if (reservation == null)
        {
            _logger.Warning("No reservation found for order {OrderId}", @event.OrderId);
            return;
        }

        // 3. Liberar stock (COMPENSACIÓN)
        await _stockService.ReleaseReservationAsync(reservation.Id);

        // 4. Publicar evento
        await _eventBus.PublishAsync(new InventoryReleasedEvent
        {
            OrderId = @event.OrderId,
            ReservationId = reservation.Id,
            Reason = "Payment rejected"
        });

        // 5. Marcar como procesado
        await MarkAsProcessed(@event.EventId);
    }
}
```

## Mejores Prácticas

### 1. Idempotencia

**CRÍTICO**: Todos los handlers deben ser idempotentes.

```csharp
// NO CÓDIGO REAL
// Usar tabla de eventos procesados
public async Task<bool> IsAlreadyProcessed(string eventId)
{
    return await _db.ProcessedEvents
        .AnyAsync(e => e.EventId == eventId);
}

public async Task MarkAsProcessed(string eventId)
{
    await _db.ProcessedEvents.AddAsync(new ProcessedEvent
    {
        EventId = eventId,
        ProcessedAt = DateTime.UtcNow
    });
    await _db.SaveChangesAsync();
}
```

### 2. Timeouts

Configurar timeouts para cada paso:

```
- Inventory Reservation: 5 minutos
- Payment Processing: 2 minutos
- Overall Saga: 10 minutos
```

Si expira, ejecutar compensación automática.

### 3. Estado de Saga

Almacenar estado de la saga para:
- Monitoring
- Debugging
- Recovery
- Reanudar sagas interrumpidas

```
OrderSagaState table:
- OrderId
- CurrentState
- StartedAt
- LastUpdatedAt
- CompletedSteps (JSON)
- FailureReason
```

### 4. Compensación Completa

Cada acción debe tener su compensación:

| Acción | Compensación |
|--------|-------------|
| Create Order | Cancel Order |
| Reserve Inventory | Release Reservation |
| Process Payment | Refund Payment |
| Send Notification | Send Cancellation Notice |

### 5. Orden de Compensación

Compensar en **orden inverso** a la ejecución:

```
Ejecución:
1. Create Order
2. Reserve Inventory
3. Process Payment

Compensación:
3. Refund Payment
2. Release Inventory
1. Cancel Order
```

### 6. Semantic Lock

Usar locks semánticos en lugar de locks de base de datos:

```csharp
// NO CÓDIGO REAL
public class Order
{
    public OrderStatus Status { get; private set; }
    
    // Semantic lock via estado
    public bool CanBeModified()
    {
        return Status == OrderStatus.Pending || 
               Status == OrderStatus.Created;
    }
    
    public void Confirm()
    {
        if (!CanBeModified())
            throw new InvalidOperationException("Cannot confirm order in current state");
            
        Status = OrderStatus.Confirmed;
    }
}
```

## Monitoreo y Observabilidad

### Correlation ID

Propagar Correlation ID en todos los eventos:

```
Event 1: OrderCreatedEvent
  └─> CorrelationId: abc-123

Event 2: InventoryReservedEvent
  └─> CorrelationId: abc-123
  └─> CausationId: [EventId de OrderCreatedEvent]

Event 3: PaymentApprovedEvent
  └─> CorrelationId: abc-123
  └─> CausationId: [EventId de InventoryReservedEvent]
```

### Dashboard de Sagas

Monitorear:
- Sagas en progreso
- Sagas completadas (tasa de éxito)
- Sagas fallidas
- Tiempo promedio de completación
- Paso donde más fallan

### Alertas

Configurar alertas para:
- Saga excede timeout
- Tasa de fallos > 5%
- Compensaciones frecuentes
- Eventos duplicados

## Testing

### Unit Tests

Testear cada handler individualmente:

```csharp
// NO CÓDIGO REAL
[Fact]
public async Task PaymentApprovedEventHandler_Should_ConfirmOrder()
{
    // Arrange
    var handler = new PaymentApprovedEventHandler(...);
    var @event = new PaymentApprovedEvent { OrderId = orderId };

    // Act
    await handler.HandleAsync(@event);

    // Assert
    var order = await _repository.GetByIdAsync(orderId);
    Assert.Equal(OrderStatus.Confirmed, order.Status);
}
```

### Integration Tests

Testear flujo completo de saga:

```csharp
// NO CÓDIGO REAL
[Fact]
public async Task OrderCreationSaga_HappyPath_Should_CompleteSuccessfully()
{
    // Arrange
    var orderRequest = CreateOrderRequest();

    // Act
    var orderId = await CreateOrder(orderRequest);

    // Assert - Verificar cada paso
    await WaitFor(() => InventoryIsReserved(orderId));
    await WaitFor(() => PaymentIsProcessed(orderId));
    await WaitFor(() => OrderIsConfirmed(orderId));
    await WaitFor(() => NotificationIsSent(orderId));
}

[Fact]
public async Task OrderCreationSaga_PaymentFails_Should_Compensate()
{
    // Arrange - Configurar payment gateway para fallar
    ConfigurePaymentToFail();

    // Act
    var orderId = await CreateOrder(orderRequest);

    // Assert - Verificar compensación
    await WaitFor(() => InventoryIsReleased(orderId));
    await WaitFor(() => OrderIsCancelled(orderId));
}
```

## Troubleshooting

### Problema: Saga Stuck (Atascada)

**Síntoma**: Saga no progresa

**Diagnóstico**:
1. Verificar logs del último paso completado
2. Revisar dead letter queue
3. Verificar que todos los servicios estén up

**Solución**:
1. Re-publicar evento manualmente si se perdió
2. Ejecutar compensación manual si es necesario
3. Implementar timeout automation

### Problema: Compensación Parcial

**Síntoma**: Algunos pasos compensados, otros no

**Diagnóstico**:
1. Revisar estado de saga
2. Ver qué servicios fallaron en compensación

**Solución**:
1. Manual intervention para completar compensación
2. Implementar retry automático para compensaciones

## Referencias

- [Event Catalog](../events/README.md)
- [Architecture Overview](../architecture/README.md)
- [Idempotency Guide](idempotency.md)
- [Event-Driven Patterns](event-driven-patterns.md)

## Recursos Externos

- [Saga Pattern - Chris Richardson](https://microservices.io/patterns/data/saga.html)
- [Distributed Sagas - Caitie McCaffrey](https://www.youtube.com/watch?v=0UTOLRTwOX0)
