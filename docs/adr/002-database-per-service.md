# Decisión Arquitectónica 002: Database per Service Pattern

**Estado**: Aceptado  
**Fecha**: 2025-11-14  
**Decisores**: Equipo de Arquitectura  

## Contexto

En una arquitectura de microservicios, debemos decidir cómo gestionar la persistencia de datos. La decisión afecta el acoplamiento entre servicios, la escalabilidad y la autonomía de cada equipo.

## Decisión

Cada microservicio tendrá su propia base de datos independiente. No se permitirá acceso directo a la base de datos de otro servicio.

## Justificación

### Ventajas

1. **Independencia**: Cada servicio puede elegir la tecnología de BD más apropiada
2. **Escalabilidad**: Cada base de datos puede escalar independientemente
3. **Despliegue Independiente**: No hay riesgo de bloqueos de esquema entre servicios
4. **Aislamiento de Fallos**: Problemas en una BD no afectan otros servicios
5. **Autonomía de Equipos**: Cada equipo gestiona su esquema sin coordinación

### Desventajas

1. **Joins Distribuidos**: No se pueden hacer JOINs entre servicios
2. **Transacciones Distribuidas**: Requiere implementar Saga pattern
3. **Consistencia Eventual**: No hay consistencia inmediata entre servicios
4. **Duplicación de Datos**: Puede haber duplicación necesaria
5. **Complejidad en Queries**: Queries que abarcan múltiples servicios son complejas

## Alternativas Consideradas

### 1. Base de Datos Compartida
- **Rechazado**: Alto acoplamiento
- Dificultad para escalar independientemente
- Riesgo de modificaciones que afecten múltiples servicios
- Cuellos de botella

### 2. Shared Schema por Servicio
- **Rechazado**: Acoplamiento a nivel de esquema
- Dificulta migraciones independientes

### 3. Database per Team (múltiples servicios por BD)
- **Rechazado**: No proporciona suficiente aislamiento
- Equipos diferentes compartiendo recursos

## Consecuencias

### Positivas
- Cada servicio es verdaderamente independiente
- Equipos pueden optimizar su almacenamiento según necesidades
- Migraciones de esquema sin coordinación entre equipos
- Posibilidad de usar diferentes tecnologías (SQL Server, PostgreSQL, MongoDB, etc.)

### Negativas
- Necesidad de implementar Saga pattern para transacciones distribuidas
- Reporting cross-service requiere soluciones específicas (CQRS, Data Warehouse)
- Mayor complejidad en operaciones
- Costos de infraestructura potencialmente más altos

## Implementación

### Por Servicio

**Orders API**:
- Database: `OrdersDB` (SQL Server)
- Tablas: Orders, OrderItems, OrderHistory
- No expone acceso directo a otros servicios

**Inventory API**:
- Database: `InventoryDB` (SQL Server)
- Tablas: Products, Stock, Reservations
- Gestiona su propio estado de inventario

**Payments API**:
- Database: `PaymentsDB` (SQL Server)
- Tablas: Transactions, PaymentMethods, Refunds
- Datos sensibles aislados

**Notifications API**:
- Database: `NotificationsDB` (SQL Server)
- Tablas: NotificationLog, Templates, Preferences
- Historia de notificaciones enviadas

### Estrategias para Queries Cross-Service

1. **API Composition**: Servicio compone respuesta llamando a múltiples APIs
2. **CQRS**: Read models específicos mantenidos mediante eventos
3. **Data Warehouse**: Para analytics y reporting
4. **BFF Pattern**: Backend for Frontend que agrega datos

### Transacciones Distribuidas

Usar Saga Pattern con compensación:
```
Orden de ejecución:
1. Orders: Crear orden
2. Inventory: Reservar stock (compensable)
3. Payments: Procesar pago (compensable)
4. Orders: Confirmar orden

En caso de fallo:
- Payments falla → Inventory libera → Orders cancela
```

## Migraciones

- Cada servicio gestiona sus propias migraciones
- Usar Entity Framework Migrations / Flyway
- Versionado de esquema independiente
- No se permite DDL cross-database

## Backup y Recuperación

- Estrategia de backup por base de datos
- RPO y RTO pueden variar por servicio según criticidad
- Testing de recuperación independiente

## Referencias

- [Architecture Overview](../architecture/README.md)
- [Saga Pattern Guide](../guides/saga-pattern.md)
- [CQRS Pattern Guide](../guides/cqrs-pattern.md)
