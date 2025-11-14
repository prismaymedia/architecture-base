# Product Backlog

> **Última actualización**: 2025-11-14
> 
> **Metodología**: Kanban
> 
> **Estado del Backlog**: En construcción inicial

---

## Instrucciones de Uso

Este backlog contiene todas las historias de usuario pendientes, en progreso y completadas del proyecto. Utilizamos metodología Kanban para gestión continua del flujo de trabajo.

### Para agregar una nueva historia:
1. Usa la plantilla en `docs/backlog-template.md`
2. Asigna prioridad según valor de negocio
3. Coloca en la sección "To Do"
4. Actualiza la fecha de última modificación

### Para mover historias:
- Mueve entre secciones según el estado real
- Actualiza fecha cuando cambies de estado
- Mantén límites WIP (Work In Progress)

### Límites WIP (Work In Progress):
- **In Progress**: Máximo 5 historias simultáneas
- **In Review**: Máximo 3 historias simultáneas

---

## Backlog por Prioridad

### 🔴 Prioridad Alta - Crítico

#### US-001: Creación de Pedido Básico
**Como** cliente del e-commerce  
**Quiero** poder crear un pedido con productos seleccionados  
**Para** completar mi compra

**Criterios de Aceptación:**
- [ ] Puedo agregar productos al carrito
- [ ] Puedo ver el resumen de mi pedido antes de confirmar
- [ ] El sistema valida disponibilidad de stock
- [ ] Se genera un número de orden único
- [ ] Recibo confirmación por email

**Estimación**: 8 Story Points  
**Epic**: Gestión de Pedidos  
**Servicios Afectados**: Orders API, Inventory API, Notifications API  
**Estado**: To Do  
**Notas Técnicas**: Implementar OrderCreatedEvent y flujo básico de Saga

---

#### US-002: Procesamiento de Pagos
**Como** cliente  
**Quiero** pagar mi pedido con tarjeta de crédito  
**Para** completar la transacción

**Criterios de Aceptación:**
- [ ] Puedo ingresar datos de tarjeta de forma segura
- [ ] El sistema tokeniza la información de pago
- [ ] Recibo confirmación de pago aprobado o rechazado
- [ ] Si el pago es rechazado, el pedido se cancela automáticamente
- [ ] Los datos de pago están encriptados

**Estimación**: 13 Story Points  
**Epic**: Procesamiento de Pagos  
**Servicios Afectados**: Payments API, Orders API  
**Dependencias**: US-001  
**Estado**: To Do  
**Notas Técnicas**: Integración con Stripe, implementar PaymentApprovedEvent

---

#### US-003: Reserva de Inventario
**Como** sistema  
**Quiero** reservar automáticamente el inventario cuando se crea un pedido  
**Para** garantizar disponibilidad de productos

**Criterios de Aceptación:**
- [ ] Al crear pedido, el stock se reserva temporalmente
- [ ] La reserva expira después de 15 minutos si no se confirma pago
- [ ] Si no hay stock, el pedido se cancela inmediatamente
- [ ] El stock liberado vuelve a estar disponible
- [ ] Se registra historial de movimientos de inventario

**Estimación**: 8 Story Points  
**Epic**: Gestión de Inventario  
**Servicios Afectados**: Inventory API  
**Dependencias**: US-001  
**Estado**: To Do  
**Notas Técnicas**: Implementar InventoryReservedEvent, job para liberar reservas expiradas

---

#### 📚 EJEMPLO: US-011: Implementar Caché para Productos Más Vendidos
> **Nota**: Esta historia fue generada automáticamente desde ID-007 usando `./process-ideas.sh`

**Como** administrador del sistema  
**Quiero** cachear la consulta de productos más vendidos  
**Para** reducir la latencia del endpoint y la carga en la base de datos

**Criterios de Aceptación:**
- [ ] El endpoint /api/products/bestsellers responde en menos de 50ms
- [ ] La caché se actualiza automáticamente cada 5 minutos
- [ ] Se reduce la carga de la base de datos en al menos 90%
- [ ] La caché se invalida cuando se agrega o modifica un producto
- [ ] Se implementan métricas de cache hit/miss ratio
- [ ] El sistema funciona correctamente cuando la caché falla (fallback a DB)

**Estimación**: 5 Story Points  
**Epic**: Performance Optimization  
**Prioridad**: Alta 🔴  
**Servicios Afectados**: Products API  
**Dependencias**: Ninguna  
**Estado**: To Do

**Notas Técnicas:**
- Implementar usando Redis como caché distribuido
- Configurar TTL de 5 minutos para la caché
- Publicar ProductCacheInvalidatedEvent cuando se modifiquen productos
- Implementar circuit breaker para fallo de Redis

---

### 🟡 Prioridad Media - Importante

#### US-004: Notificaciones de Estado de Pedido
**Como** cliente  
**Quiero** recibir notificaciones sobre el estado de mi pedido  
**Para** estar informado del progreso

**Criterios de Aceptación:**
- [ ] Recibo email cuando se crea el pedido
- [ ] Recibo email cuando se confirma el pago
- [ ] Recibo email cuando el pedido se envía (con tracking)
- [ ] Recibo email si el pedido se cancela
- [ ] Puedo configurar mis preferencias de notificación

**Estimación**: 5 Story Points  
**Epic**: Comunicación con Cliente  
**Servicios Afectados**: Notifications API  
**Dependencias**: US-001, US-002  
**Estado**: To Do

---

#### US-005: Historial de Pedidos
**Como** cliente  
**Quiero** ver el historial de todos mis pedidos  
**Para** hacer seguimiento de mis compras

**Criterios de Aceptación:**
- [ ] Puedo ver lista de todos mis pedidos
- [ ] Puedo filtrar por estado (pendiente, completado, cancelado)
- [ ] Puedo ver detalles de cada pedido
- [ ] Puedo ver historial de cambios de estado
- [ ] La lista está paginada

**Estimación**: 5 Story Points  
**Epic**: Gestión de Pedidos  
**Servicios Afectados**: Orders API  
**Dependencias**: US-001  
**Estado**: To Do

---

#### US-006: Cancelación de Pedido
**Como** cliente  
**Quiero** poder cancelar mi pedido antes de que se envíe  
**Para** no recibir productos que ya no necesito

**Criterios de Aceptación:**
- [ ] Puedo cancelar pedidos en estado "Pendiente" o "Confirmado"
- [ ] No puedo cancelar pedidos ya enviados
- [ ] Si ya se procesó el pago, se genera reembolso automático
- [ ] El inventario reservado se libera
- [ ] Recibo confirmación de cancelación

**Estimación**: 8 Story Points  
**Epic**: Gestión de Pedidos  
**Servicios Afectados**: Orders API, Payments API, Inventory API  
**Dependencias**: US-001, US-002  
**Estado**: To Do  
**Notas Técnicas**: Implementar compensación en Saga

---

### 🟢 Prioridad Baja - Mejoras

#### US-007: Dashboard de Inventario
**Como** administrador de inventario  
**Quiero** ver un dashboard con el estado actual del inventario  
**Para** gestionar el stock de manera eficiente

**Criterios de Aceptación:**
- [ ] Veo productos con stock bajo
- [ ] Veo productos sin stock
- [ ] Veo historial de movimientos de inventario
- [ ] Puedo ajustar manualmente el inventario
- [ ] Los ajustes se auditan

**Estimación**: 8 Story Points  
**Epic**: Herramientas de Administración  
**Servicios Afectados**: Inventory API  
**Estado**: To Do

---

#### US-008: Métricas de Negocio
**Como** gerente de operaciones  
**Quiero** ver métricas clave del negocio  
**Para** tomar decisiones basadas en datos

**Criterios de Aceptación:**
- [ ] Veo total de ventas del día/mes
- [ ] Veo tasa de conversión de pedidos
- [ ] Veo productos más vendidos
- [ ] Veo tasa de cancelaciones
- [ ] Veo tiempo promedio de procesamiento

**Estimación**: 13 Story Points  
**Epic**: Analytics  
**Servicios Afectados**: Nuevo servicio (Analytics API)  
**Estado**: To Do

---

#### US-009: Tracking de Envío
**Como** cliente  
**Quiero** hacer seguimiento de mi envío en tiempo real  
**Para** saber cuándo llegará mi pedido

**Criterios de Aceptación:**
- [ ] Recibo número de tracking cuando se envía el pedido
- [ ] Puedo ver estado actual del envío
- [ ] Veo estimación de entrega
- [ ] Recibo notificación cuando se entrega
- [ ] Integración con API de transportista

**Estimación**: 8 Story Points  
**Epic**: Logística  
**Servicios Afectados**: Orders API, Notifications API  
**Dependencias**: US-001  
**Estado**: To Do

---

#### US-010: Métodos de Pago Adicionales
**Como** cliente  
**Quiero** poder pagar con PayPal además de tarjeta  
**Para** usar mi método de pago preferido

**Criterios de Aceptación:**
- [ ] Puedo seleccionar PayPal como método de pago
- [ ] El flujo de pago con PayPal funciona correctamente
- [ ] Recibo confirmación del pago
- [ ] Los reembolsos funcionan para PayPal
- [ ] Los datos se almacenan de forma segura

**Estimación**: 8 Story Points  
**Epic**: Procesamiento de Pagos  
**Servicios Afectados**: Payments API  
**Dependencias**: US-002  
**Estado**: To Do

---

## Estado del Kanban Board

### 📋 To Do (Backlog)
- US-001: Creación de Pedido Básico
- US-002: Procesamiento de Pagos
- US-003: Reserva de Inventario
- US-004: Notificaciones de Estado de Pedido
- US-005: Historial de Pedidos
- US-006: Cancelación de Pedido
- US-007: Dashboard de Inventario
- US-008: Métricas de Negocio
- US-009: Tracking de Envío
- US-010: Métodos de Pago Adicionales
- US-011: Implementar Caché para Productos Más Vendidos (📚 Ejemplo auto-generado)

**Total**: 11 historias (10 + 1 ejemplo)

---

### 🏗️ In Progress (WIP: 0/5)

_Ninguna historia en progreso actualmente_

---

### 👀 In Review (WIP: 0/3)

_Ninguna historia en revisión actualmente_

---

### ✅ Done

_Ninguna historia completada aún_

---

## Épics

### Epic: Gestión de Pedidos
**Objetivo**: Permitir a los clientes crear, ver y gestionar sus pedidos  
**Historias**: US-001, US-005, US-006  
**Progreso**: 0/3 (0%)

### Epic: Procesamiento de Pagos
**Objetivo**: Procesar pagos de manera segura y eficiente  
**Historias**: US-002, US-010  
**Progreso**: 0/2 (0%)

### Epic: Gestión de Inventario
**Objetivo**: Mantener control preciso del inventario  
**Historias**: US-003, US-007  
**Progreso**: 0/2 (0%)

### Epic: Comunicación con Cliente
**Objetivo**: Mantener al cliente informado  
**Historias**: US-004, US-009  
**Progreso**: 0/2 (0%)

### Epic: Herramientas de Administración
**Objetivo**: Proveer herramientas para administradores  
**Historias**: US-007, US-008  
**Progreso**: 0/2 (0%)

---

## Métricas del Backlog

- **Total de Historias**: 10
- **Story Points Totales**: 82
- **Historias Completadas**: 0
- **Velocity Promedio**: TBD (se calculará después de primeros sprints)
- **Tiempo Estimado de Completación**: TBD

---

## Definición de "Done"

Una historia se considera "Done" cuando:

1. ✅ Código implementado y committeado
2. ✅ Tests escritos y pasando (>80% coverage)
3. ✅ Code review aprobado por al menos 2 personas
4. ✅ Documentación actualizada
5. ✅ Eventos documentados en catálogo (si aplica)
6. ✅ Desplegado en ambiente de staging
7. ✅ Probado por QA
8. ✅ Aceptado por Product Owner
9. ✅ Desplegado en producción
10. ✅ Monitoreado por 24 horas sin incidentes

---

## Notas

### Próximas Sesiones de Refinamiento
- **Fecha**: Por definir
- **Objetivo**: Refinar historias US-001 a US-003

### Bloqueadores Actuales
_Ninguno_

### Deuda Técnica Conocida
_Por documentar a medida que surja_

---

## Historial de Cambios

| Fecha | Cambio | Autor |
|-------|--------|-------|
| 2025-11-14 | Creación inicial del backlog | Product Owner |

---

## Referencias

- [Manual de Product Owner](docs/guides/product-owner-guide.md)
- [Guía de Kanban](docs/guides/kanban-guide.md)
- [Plantilla de Historia de Usuario](docs/backlog-template.md)
- [Architecture Overview](docs/architecture/README.md)
