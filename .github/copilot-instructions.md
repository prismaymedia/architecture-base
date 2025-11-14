# Instrucciones Globales para GitHub Copilot

## Contexto del Proyecto

Este es un sistema de microservicios distribuidos construido con arquitectura orientada a eventos. El proyecto utiliza:

- **BIT**: Plataforma de componentes para desarrollo modular
- **IIS**: Internet Information Services como servidor web
- **Event-Driven Architecture**: Comunicación asíncrona entre servicios

## Arquitectura General

### Microservicios

1. **Orders API** - Gestión de pedidos
2. **Inventory API** - Control de inventario
3. **Payments API** - Procesamiento de pagos
4. **Notifications API** - Envío de notificaciones

### Patrones de Comunicación

- **Eventos Asíncronos**: Para comunicación entre servicios (RabbitMQ/Azure Service Bus)
- **REST APIs**: Para comunicación síncrona cuando sea necesario
- **Compensación**: Para mantener consistencia eventual

## Principios de Diseño

### 1. Arquitectura de Microservicios

- Cada servicio debe ser independiente y autónomo
- Base de datos por servicio (Database per Service pattern)
- Desacoplamiento mediante eventos
- Sin dependencias directas entre servicios

### 2. Event-Driven Patterns

- **Event Sourcing**: Considerar para servicios que requieren auditoría completa
- **CQRS**: Separación de comandos y consultas donde tenga sentido
- **Saga Pattern**: Para transacciones distribuidas
- **Event Notification**: Para notificar cambios de estado

### 3. Resiliencia

- Circuit Breaker para llamadas externas
- Retry policies con backoff exponencial
- Timeouts apropiados
- Health checks en todos los servicios

## Convenciones de Código

### Nombrado

- **Eventos**: PasadoTense + Sufijo "Event" (ej: `OrderCreatedEvent`)
- **Comandos**: Imperativo + Sufijo "Command" (ej: `CreateOrderCommand`)
- **Handlers**: Nombre del mensaje + "Handler" (ej: `OrderCreatedEventHandler`)
- **Servicios**: Sustantivo + "Service" (ej: `OrderService`)

### Estructura de Proyecto

```
services/
├── {service-name}/
│   ├── src/
│   │   ├── api/           # Controllers/Endpoints
│   │   ├── application/   # Application logic, handlers
│   │   ├── domain/        # Entidades, value objects
│   │   ├── infrastructure/ # Implementaciones técnicas
│   │   └── events/        # Definición de eventos
│   ├── tests/
│   └── .copilot-context.md
```

## Tecnologías y Stack

### Backend (.NET para IIS)

- ASP.NET Core Web API
- Entity Framework Core
- MassTransit / NServiceBus para mensajería
- Serilog para logging

### Infraestructura

- IIS como servidor web principal
- SQL Server / PostgreSQL para bases de datos
- RabbitMQ / Azure Service Bus para mensajería
- Redis para caché distribuido

### BIT Components

- Componentes reutilizables compartidos entre servicios
- Contracts (schemas de eventos y DTOs)
- Shared libraries (utilidades comunes)

## Reglas Importantes

### ❌ NO hacer

- NO crear dependencias directas entre microservicios
- NO compartir bases de datos entre servicios
- NO hacer llamadas síncronas si se puede usar eventos
- NO incluir lógica de negocio en controladores
- NO exponer entidades de dominio directamente

### ✅ SÍ hacer

- SÍ usar DTOs para todas las APIs
- SÍ validar eventos y comandos
- SÍ implementar idempotencia en handlers
- SÍ usar logging estructurado
- SÍ documentar todos los eventos publicados/consumidos

## Testing

- Unit tests para lógica de dominio
- Integration tests para event handlers
- Contract tests para eventos compartidos
- End-to-end tests para flujos críticos

## Documentación Requerida

Cuando trabajes en este proyecto, siempre considera:

1. **Documentar eventos**: Cada evento debe estar documentado en `docs/events/`
2. **Diagramas de flujo**: Para sagas y procesos complejos
3. **ADRs**: Para decisiones arquitectónicas importantes
4. **README**: Cada servicio debe tener su propio README

## Comandos Útiles

Referencia los scripts y comandos específicos en cada servicio's README.

## Gestión de Proyecto

Este proyecto utiliza **metodología Kanban** para gestión continua del flujo de trabajo.

### Product Backlog

- **BACKLOG.md**: Backlog principal con todas las historias de usuario
- Historias en formato: "Como... Quiero... Para..."
- Priorizadas por valor de negocio usando RICE framework
- Límites WIP: In Progress (5), In Review (3)

### Kanban Board States

1. **To Do**: Historias priorizadas y refinadas, listas para trabajarse
2. **In Progress**: En desarrollo activo (máximo 5 simultáneas)
3. **In Review**: En code review o QA (máximo 3 simultáneas)
4. **Done**: Completadas y en producción

### Agregar Nueva Feature

1. Usa plantilla en `docs/backlog-template.md`
2. Formato de historia de usuario con criterios de aceptación
3. Estima con Story Points (1, 2, 3, 5, 8, 13)
4. Asigna prioridad y Epic
5. Agrega a `BACKLOG.md` en sección correspondiente

### Documentación de Gestión

- Manual de Product Owner: `/docs/guides/product-owner-guide.md`
- Guía de Kanban: `/docs/guides/kanban-guide.md`
- Plantilla de historia: `/docs/backlog-template.md`

## Flujo de Ideas a Tareas (Automatizado)

Este proyecto implementa un sistema automatizado para convertir ideas en tareas ejecutables en ClickUp.

### 📝 Sistema de Captura de Ideas

- **IDEAS.md**: Archivo centralizado para capturar ideas rápidas
- Formato simple: Contexto, Problema, Valor, Prioridad (🔴/🟡/🟢/💭)
- No requiere formato perfecto - lo importante es capturar la esencia
- Las ideas se refinan periódicamente a historias de usuario formales

### 🔄 Proceso de Conversión

```
IDEAS.md → BACKLOG.md → Technical Tasks → ClickUp
  💡         📋              ⚙️              ✅
```

### 🤖 Generación Automatizada de Tareas

Cuando el Product Owner solicite crear tareas para un sprint, Copilot debe:

1. **Analizar prioridades** en `BACKLOG.md`:
   - Identificar user stories en "High Priority" con estado "To Do"
   - Considerar story points y dependencias
   - Sugerir cuáles incluir en el sprint basado en capacidad del equipo

2. **Descomponer US en tareas técnicas**:
   - Cada user story genera 2-5 tareas dependiendo de complejidad
   - Usar nomenclatura `TASK-XXX` (secuencial)
   - Tareas en **inglés** usando formato de `docs/task-template.md`

3. **Para cada tarea, generar**:
   - **Description**: Technical scope, archivos a modificar, dependencias
   - **Functional Acceptance Criteria**: 4-6 criterios orientados a negocio/usuario
   - **Technical Acceptance Criteria**: Code quality, performance, security, testing, observability
   - **Best Practices to Apply**: Checklist detallado de:
     - Architecture (Clean Architecture, CQRS, Repository pattern)
     - Code Quality (SOLID, meaningful names, small methods)
     - Event-Driven (idempotency, correlation IDs, outbox pattern, versioning)
     - Resilience (circuit breaker, retry policies, timeouts)
     - Security (input validation, parameterized queries, no sensitive data in logs)
     - Testing (TDD, unit tests, integration tests, contract tests)
     - Observability (structured logging, metrics, health checks, correlation IDs)
   - **Recommendations**: Before/During/After implementation tips
   - **Testing Strategy**: Unit, integration, manual testing checklist
   - **Related Resources**: Links a docs, ADRs, event specs, service context
   - **Definition of Done**: Checklist completo

4. **Presentar preliminar para revisión**:
   - Mostrar resumen de tareas generadas (sprint overview)
   - Permitir revisar cada tarea **una por una**
   - Aceptar modificaciones antes de aprobar
   - NO crear tareas en ClickUp sin aprobación explícita del PO

5. **Workflow de revisión iterativa**:
   ```
   PO: "Muéstrame TASK-001 completa"
   Copilot: [Despliega tarea completa con todos los detalles]
   
   PO: "Modifica TASK-001 - agrega AC sobre logging de errores"
   Copilot: [Actualiza TAC y muestra cambio]
   
   PO: "Aprobada. Siguiente tarea."
   Copilot: [Muestra TASK-002...]
   ```

6. **Después de aprobar todas**:
   - Generar archivo `sprint-X-tasks.md` con todas las tareas aprobadas
   - Proveer instrucciones para crear en ClickUp (manual o API)
   - Actualizar BACKLOG.md marcando US como "In Progress"

### 📋 Comandos para Generación de Tareas

Cuando el PO solicite:

- **"Genera tareas para el próximo sprint basado en prioridades"**
  → Analizar BACKLOG.md, identificar High Priority, descomponer en tareas técnicas

- **"Crea tareas preliminares para US-XXX"**
  → Generar 2-5 tareas técnicas para esa user story específica

- **"Muéstrame TASK-XXX completa"**
  → Desplegar tarea completa con todos los detalles del template

- **"Modifica TASK-XXX: [instrucción]"**
  → Actualizar tarea según instrucción y mostrar cambio

- **"Aprobada. Siguiente tarea."**
  → Marcar como aprobada y mostrar siguiente tarea del sprint

- **"Exporta tareas aprobadas para ClickUp"**
  → Generar archivo `sprint-X-tasks.md` con formato ClickUp-compatible

### ⚙️ Plantillas y Recursos

- **Plantilla de tarea**: `/docs/task-template.md`
- **Flujo completo**: `/docs/guides/idea-to-task-flow.md`
- **Captura de ideas**: `/IDEAS.md`

### 🎯 Principios Clave

1. **Tareas en inglés**: Para colaboración internacional
2. **Revisión una por una**: PO debe aprobar cada tarea individualmente
3. **Best practices incluidas**: Cada tarea tiene checklist de arquitectura, seguridad, testing
4. **Contexto completo**: Links a docs, eventos, ADRs relevantes
5. **Criterios claros**: Functional + Technical ACs bien definidos
6. **Recomendaciones prácticas**: Tips before/during/after implementation

## Recursos

- Documentación arquitectónica: `/docs/architecture/`
- Catálogo de eventos: `/docs/events/`
- Guías de desarrollo: `/docs/guides/`
- ADRs: `/docs/adr/`
- **Backlog del proyecto**: `/BACKLOG.md`
