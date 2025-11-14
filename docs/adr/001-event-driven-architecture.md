# Decisión Arquitectónica 001: Uso de Event-Driven Architecture

**Estado**: Aceptado  
**Fecha**: 2025-11-14  
**Decisores**: Equipo de Arquitectura  

## Contexto

Necesitamos diseñar un sistema de e-commerce distribuido que soporte múltiples microservicios. Los servicios deben comunicarse entre sí de manera eficiente, manteniendo bajo acoplamiento y alta cohesión.

## Decisión

Implementaremos una arquitectura orientada a eventos (Event-Driven Architecture) utilizando un message broker centralizado (RabbitMQ o Azure Service Bus) para la comunicación entre microservicios.

## Justificación

### Ventajas

1. **Desacoplamiento**: Los servicios no necesitan conocerse entre sí directamente
2. **Escalabilidad**: Cada servicio puede escalar independientemente
3. **Resiliencia**: Si un servicio está caído, los eventos se encolan y procesan cuando se recupera
4. **Auditoría**: Todos los eventos pueden ser almacenados para auditoría
5. **Evolución**: Nuevos servicios pueden suscribirse a eventos existentes sin modificar productores
6. **Consistencia Eventual**: Aceptable para nuestro dominio de negocio

### Desventajas

1. **Complejidad**: Mayor complejidad en debugging y testing
2. **Consistencia**: No hay transacciones ACID entre servicios
3. **Latencia**: Mayor latencia que llamadas síncronas
4. **Duplicación**: Posibilidad de procesamiento duplicado (requiere idempotencia)
5. **Ordenamiento**: No se garantiza orden global de eventos

## Alternativas Consideradas

### 1. REST APIs síncronas
- **Rechazado**: Alto acoplamiento entre servicios
- Cascada de fallos
- Difícil escalabilidad

### 2. gRPC
- **Rechazado**: Aunque más eficiente que REST, mantiene acoplamiento directo
- No resuelve problemas de resiliencia

### 3. GraphQL Federation
- **Rechazado**: Complejidad adicional
- No elimina acoplamiento temporal

## Consecuencias

### Positivas
- Los servicios pueden desarrollarse y desplegarse independientemente
- Fácil agregar nuevos consumidores de eventos
- Mejor resiliencia del sistema completo
- Facilita implementación de patterns como CQRS y Event Sourcing

### Negativas
- Requiere infraestructura adicional (message broker)
- Necesidad de implementar idempotencia en todos los handlers
- Debugging más complejo (requiere distributed tracing)
- Equipo debe aprender nuevos patrones (Saga, compensación, etc.)

## Implementación

1. Seleccionar y configurar message broker (RabbitMQ/Azure Service Bus)
2. Implementar abstracciones comunes en BIT components
3. Establecer convenciones de nombrado para eventos
4. Implementar infraestructura de logging y tracing
5. Crear tests de integración para flujos de eventos
6. Documentar todos los eventos en catálogo central

## Notas

- Cada evento debe ser inmutable
- Los eventos deben contener toda la información necesaria (no lazy loading)
- Implementar versionado de eventos desde el inicio
- Considerar Event Sourcing para servicios que requieren auditoría completa

## Referencias

- [Architecture Overview](../architecture/README.md)
- [Event Catalog](../events/README.md)
- [Saga Pattern Guide](../guides/saga-pattern.md)
