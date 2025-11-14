# Plantilla de Historia de Usuario

> Usa esta plantilla para agregar nuevas historias al backlog

---

## US-XXX: [Título de la Historia]

**Como** [tipo de usuario]  
**Quiero** [objetivo/acción]  
**Para** [beneficio/razón]

### Criterios de Aceptación

- [ ] [Criterio 1 - Específico y medible]
- [ ] [Criterio 2 - Específico y medible]
- [ ] [Criterio 3 - Específico y medible]
- [ ] [Criterio 4 - Específico y medible]
- [ ] [Criterio 5 - Específico y medible]

### Información Técnica

**Estimación**: [Story Points - 1, 2, 3, 5, 8, 13, 21]  
**Epic**: [Nombre del Epic]  
**Prioridad**: [Alta 🔴 / Media 🟡 / Baja 🟢]  
**Servicios Afectados**: [Lista de microservicios]  
**Dependencias**: [US-XXX, US-YYY] o Ninguna  
**Estado**: [To Do / In Progress / In Review / Done]

### Notas Técnicas

- [Detalles de implementación]
- [Eventos a publicar/consumir]
- [Patrones arquitectónicos a usar]
- [Integraciones externas]

### Tareas de Desarrollo (Opcional)

- [ ] Diseño de API endpoints
- [ ] Implementación de dominio
- [ ] Implementación de handlers de eventos
- [ ] Tests unitarios
- [ ] Tests de integración
- [ ] Documentación de API
- [ ] Actualizar catálogo de eventos

### Notas Adicionales

[Cualquier información adicional relevante]

---

## Ejemplo de Uso

## US-015: Reembolso Manual

**Como** administrador de operaciones  
**Quiero** poder procesar reembolsos manuales  
**Para** resolver casos especiales de servicio al cliente

### Criterios de Aceptación

- [ ] Puedo buscar un pedido por número de orden
- [ ] Puedo ver el historial de pagos del pedido
- [ ] Puedo iniciar un reembolso parcial o total
- [ ] El sistema valida que el monto no exceda el pago original
- [ ] El cliente recibe notificación del reembolso
- [ ] La acción queda auditada con usuario y timestamp

### Información Técnica

**Estimación**: 5 Story Points  
**Epic**: Procesamiento de Pagos  
**Prioridad**: Media 🟡  
**Servicios Afectados**: Payments API, Orders API, Notifications API  
**Dependencias**: US-002  
**Estado**: To Do

### Notas Técnicas

- Implementar `ManualRefundCommand`
- Publicar `RefundProcessedEvent`
- Agregar endpoint `POST /api/payments/{id}/refund/manual`
- Requiere autenticación con rol `Admin` o `Operations`
- Integración con pasarela de pago para procesar reembolso real

### Tareas de Desarrollo

- [ ] Diseño de API endpoint POST /api/payments/{id}/refund/manual
- [ ] Implementación de ManualRefundCommand y handler
- [ ] Validación de permisos (RBAC)
- [ ] Integración con payment gateway
- [ ] Publicar RefundProcessedEvent
- [ ] Tests unitarios de comando y validaciones
- [ ] Tests de integración del flujo completo
- [ ] Documentación en Swagger
- [ ] Actualizar catálogo de eventos

### Notas Adicionales

Esta funcionalidad es crítica para servicio al cliente. Considerar implementar:
- Límites de monto por usuario (ej: máximo $1000 por día)
- Approval workflow para montos mayores
- Dashboard para ver reembolsos procesados

---

## Guía de Story Points

Use la siguiente guía para estimar historias:

| Story Points | Complejidad | Tiempo Estimado | Ejemplo |
|--------------|-------------|-----------------|---------|
| 1 | Trivial | < 2 horas | Cambio de texto, ajuste de configuración |
| 2 | Muy Simple | 2-4 horas | CRUD simple, endpoint básico |
| 3 | Simple | 4-8 horas | Feature pequeña con validaciones |
| 5 | Moderada | 1-2 días | Feature completa con tests |
| 8 | Compleja | 2-3 días | Feature con múltiples servicios |
| 13 | Muy Compleja | 3-5 días | Feature con integraciones externas |
| 21 | Extremadamente Compleja | 1+ semana | Debe dividirse en historias más pequeñas |

**Nota**: Si una historia es 21 puntos o más, considérala un Epic y divídela en historias más pequeñas.

---

## Checklist antes de Agregar al Backlog

Antes de agregar una historia al backlog, verifica:

- [ ] La historia sigue el formato "Como... Quiero... Para..."
- [ ] Los criterios de aceptación son específicos y medibles
- [ ] La estimación está presente
- [ ] Se identificaron dependencias
- [ ] Se especificaron los servicios afectados
- [ ] La prioridad está clara
- [ ] Se agregó al Epic correspondiente
- [ ] El ID de la historia es único (US-XXX)

---

## Tips para Escribir Buenas Historias

### ✅ Hacer

- Escribir desde la perspectiva del usuario
- Ser específico en criterios de aceptación
- Incluir valor de negocio claro
- Mantener historias pequeñas (< 13 puntos)
- Incluir condiciones de edge cases

### ❌ No Hacer

- Escribir tareas técnicas como historias de usuario
- Usar jerga técnica en la descripción de usuario
- Hacer historias demasiado grandes
- Omitir criterios de aceptación
- Olvidar el "Para qué" (beneficio)

---

## Proceso de Creación de Historia

1. **Identificar Necesidad**: Reunión con stakeholders, feedback de usuarios
2. **Escribir Historia**: Usar esta plantilla
3. **Refinamiento**: Revisar con equipo técnico
4. **Estimación**: Planning poker o estimación por equipo
5. **Priorización**: Decidir con Product Owner
6. **Agregar a Backlog**: Actualizar `BACKLOG.md`
7. **Mover a Kanban**: Cuando esté lista para trabajarse

---

## Referencias

- [BACKLOG.md](../BACKLOG.md)
- [Product Owner Guide](guides/product-owner-guide.md)
- [Kanban Guide](guides/kanban-guide.md)
