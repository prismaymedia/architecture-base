# Sistema de Microservicios E-commerce

> **Arquitectura**: Event-Driven Microservices  
> **Frontend**: React 18+ con Vite  
> **Backend**: Python con FastAPI  
> **Metodología**: Kanban  
> **Estado**: Planeación y Diseño Arquitectónico

Sistema de e-commerce distribuido basado en microservicios con arquitectura orientada a eventos, construido con React para el frontend y Python para el backend.

## 🏗️ Arquitectura

Este proyecto implementa un sistema de microservicios desacoplados que se comunican mediante eventos asíncronos. Cada servicio tiene su propia base de datos y es independientemente desplegable.

### Microservicios

- **Orders API**: Gestión del ciclo de vida de pedidos
- **Inventory API**: Control de inventario y disponibilidad
- **Payments API**: Procesamiento de pagos y transacciones
- **Notifications API**: Envío de notificaciones multicanal

### Stack Tecnológico

#### Frontend
- **Framework**: React 18+ (latest)
- **Build Tool**: Vite 5+
- **Language**: TypeScript 5+
- **State Management**: React Query (TanStack Query) + Zustand
- **Routing**: React Router v6
- **UI Library**: shadcn/ui with Tailwind CSS
- **Testing**: Vitest + React Testing Library

#### Backend
- **Language**: Python 3.12+
- **Framework**: FastAPI
- **Server**: Uvicorn (ASGI)
- **ORM**: SQLAlchemy 2.0
- **Validation**: Pydantic v2

#### Infrastructure
- **Mensajería**: RabbitMQ (with aio-pika)
- **Base de Datos**: PostgreSQL (database per service)
- **Caché**: Redis
- **Logging**: structlog (Python), console (frontend)
- **Monitoring**: Prometheus + Grafana
- **Containerization**: Docker + Docker Compose

## 📁 Estructura del Proyecto

```
architecture-base/
├── .github/
│   └── copilot-instructions.md          # Instrucciones globales para GitHub Copilot
├── frontend/                             # Frontend React + Vite
│   ├── src/
│   │   ├── components/                   # React components
│   │   ├── pages/                        # Page components (routes)
│   │   ├── hooks/                        # Custom hooks
│   │   ├── services/                     # API clients
│   │   ├── stores/                       # State management
│   │   ├── types/                        # TypeScript types
│   │   └── App.tsx                       # Main app component
│   ├── package.json
│   ├── vite.config.ts
│   └── tsconfig.json
├── docs/
│   ├── architecture/                     # Documentación arquitectónica
│   │   └── README.md                     # Visión general de la arquitectura
│   ├── adr/                              # Architecture Decision Records
│   │   ├── README.md                     # Índice de ADRs
│   │   ├── 001-event-driven-architecture.md
│   │   ├── 002-database-per-service.md
│   │   ├── 003-iis-web-server.md         # Superseded
│   │   ├── 004-bit-components-platform.md # Superseded
│   │   ├── 005-react-vite-frontend.md    # ✨ NEW
│   │   └── 006-python-backend.md         # ✨ NEW
│   ├── events/                           # Catálogo de eventos
│   │   ├── README.md                     # Documentación de eventos
│   │   ├── orders/                       # Eventos de Orders API
│   │   ├── inventory/                    # Eventos de Inventory API
│   │   ├── payments/                     # Eventos de Payments API
│   │   └── notifications/                # Eventos de Notifications API
│   ├── guides/                           # Guías de desarrollo
│   │   ├── README.md                     # Índice de guías
│   │   ├── saga-pattern.md               # Guía del patrón Saga
│   │   ├── product-owner-guide.md        # Manual para Product Owner
│   │   ├── kanban-guide.md               # Guía de Kanban para el equipo
│   │   ├── idea-to-task-flow.md          # 🔄 Flujo de ideas a tareas
│   │   └── clickup-integration.md        # 🚀 Integración con ClickUp
│   ├── backlog-template.md               # Plantilla de historia de usuario
│   └── task-template.md                  # 📄 Plantilla de tarea técnica
├── services/                             # Backend microservices (Python)
│   ├── orders-api/
│   │   ├── app/
│   │   │   ├── api/                      # API endpoints
│   │   │   ├── core/                     # Config & settings
│   │   │   ├── domain/                   # Business logic
│   │   │   ├── application/              # Use cases
│   │   │   ├── infrastructure/           # DB, messaging, etc.
│   │   │   └── main.py                   # FastAPI app
│   │   ├── tests/
│   │   ├── pyproject.toml
│   │   └── .copilot-context.md          # Contexto específico del servicio
│   ├── inventory-api/
│   │   └── .copilot-context.md
│   ├── payments-api/
│   │   └── .copilot-context.md
│   └── notifications-api/
│       └── .copilot-context.md
├── shared/                               # Shared code
│   ├── frontend/                         # Shared React components/utils
│   └── backend/                          # Shared Python packages
├── IDEAS.md                              # 💡 Captura rápida de ideas
├── BACKLOG.md                            # 📋 Product backlog con historias de usuario
├── docker-compose.yml                    # Local development setup
└── README.md                             # Este archivo
```

## 📋 Gestión de Proyecto - Kanban

Este proyecto utiliza **metodología Kanban** para gestión continua del flujo de trabajo.

### Product Backlog

El [BACKLOG.md](BACKLOG.md) contiene todas las historias de usuario del proyecto:

- **🔴 Prioridad Alta**: US-001 (Creación de Pedido), US-002 (Procesamiento de Pagos), US-003 (Reserva de Inventario)
- **🟡 Prioridad Media**: US-004 (Notificaciones), US-005 (Historial), US-006 (Cancelación)
- **🟢 Prioridad Baja**: US-007 (Dashboard), US-008 (Métricas), US-009 (Tracking), US-010 (PayPal)

### Estados del Kanban

1. **To Do**: Historias refinadas, listas para trabajarse
2. **In Progress**: En desarrollo activo (WIP: máximo 5)
3. **In Review**: En code review o QA (WIP: máximo 3)
4. **Done**: Completadas y en producción

### Documentación de Gestión

- 📖 [Manual de Product Owner](docs/guides/product-owner-guide.md) - Gestión del backlog con Kanban
- 📖 [Guía de Kanban](docs/guides/kanban-guide.md) - Workflow para el equipo
- 📝 [Plantilla de Historia](docs/backlog-template.md) - Para agregar nuevas features

## 💡 Gestión de Ideas y Tareas

### Flujo Automatizado: Ideas → User Stories → Tasks → ClickUp

Este proyecto implementa un sistema automatizado para convertir ideas en tareas ejecutables:

```
IDEAS.md → BACKLOG.md → Technical Tasks → ClickUp
  💡         📋              ⚙️              ✅
```

### Archivos Clave

- 💡 [IDEAS.md](IDEAS.md) - Captura rápida de ideas
- 📋 [BACKLOG.md](BACKLOG.md) - User stories refinadas
- 📄 [task-template.md](docs/task-template.md) - Plantilla de tarea técnica
- 🔄 [idea-to-task-flow.md](docs/guides/idea-to-task-flow.md) - Flujo completo
- 🚀 [clickup-integration.md](docs/guides/clickup-integration.md) - Integración con ClickUp

### Proceso en 4 Pasos

1. **Captura de Ideas** (IDEAS.md):
   - Anota ideas rápidas con contexto, problema, valor
   - No requiere formato perfecto
   - Marca prioridad preliminar (🔴/🟡/🟢/💭)

2. **Refinamiento a User Stories** (BACKLOG.md):
   - Copilot convierte ideas en historias formales
   - Aplica framework RICE para priorización
   - Generas criterios de aceptación detallados

3. **Generación de Tareas Técnicas**:
   - Copilot descompone US en tareas (TASK-XXX)
   - Incluye: Description, Functional ACs, Technical ACs, Best Practices
   - Revisas una por una antes de aprobar

4. **Exportación a ClickUp**:
   - Manual (copy-paste), CSV, o API automática
   - Tareas listas para ejecución por el equipo
   - Mantiene trazabilidad completa

### Comandos para Copilot

```bash
# Refinamiento de ideas
"Copilot, convierte ID-XXX a user story formal"

# Generación de tareas
"Copilot, genera tareas para el próximo sprint basado en prioridades"
"Copilot, muéstrame TASK-XXX completa"

# Revisión iterativa
"Copilot, modifica TASK-XXX: agrega AC sobre logging de errores"
"Copilot, aprobada. Siguiente tarea."

# Exportación
"Copilot, exporta tareas aprobadas para ClickUp"
```

Ver [idea-to-task-flow.md](docs/guides/idea-to-task-flow.md) para detalles completos.

### 🤖 Automatización con Scripts

Además de usar Copilot interactivamente, puedes usar el **procesador automático de ideas**:

```bash
# Procesar ideas automáticamente
./process-ideas.sh

# O directamente con Python
python -m scripts.idea_processor.cli

# Modo preview (sin modificar archivos)
./process-ideas.sh --dry-run
```

**Qué hace el script:**
1. ✅ Lee todas las ideas de `IDEAS.md` con estado "💭 Por refinar"
2. ✅ Detecta duplicados usando IA (OpenAI o Google Gemini)
3. ✅ Marca ideas duplicadas con referencia a US similar
4. ✅ Genera historias de usuario automáticamente para ideas únicas
5. ✅ Agrega nuevas US a `BACKLOG.md` en la sección de prioridad correcta
6. ✅ Actualiza `IDEAS.md` marcando ideas como convertidas

### 🔄 GitHub Actions - Procesamiento Automático

**¡NUEVO!** El procesador se ejecuta automáticamente con cada push a `master`:

```bash
# 1. Agrega ideas a IDEAS.md
vim IDEAS.md  # Agrega idea con estado "💭 Por refinar"

# 2. Commit y push
git commit -am "feat: add new idea"
git push origin master

# 3. GitHub Actions procesa automáticamente
# - Usa Google Gemini AI
# - Detecta duplicados
# - Genera user stories
# - Commitea cambios automáticamente
```

**Setup**: Solo necesitas configurar el secret `GEMINI_API_KEY` en GitHub Settings.

Ver [docs/guides/github-actions-setup.md](docs/guides/github-actions-setup.md) para guía completa.

Ver [scripts/idea_processor/README.md](scripts/idea_processor/README.md) para documentación completa.

## 🎯 Fase Actual: Planeación

**Este proyecto está en fase de planeación arquitectónica**. No contiene código de implementación todavía.

### Archivos de Planeación Creados

✅ **Contexto de GitHub Copilot**:
- `.github/copilot-instructions.md`: Instrucciones globales para Copilot
- `.copilot-context.md` en cada servicio: Contexto específico por microservicio

✅ **Documentación Arquitectónica**:
- Visión general del sistema y patrones
- Diagramas de arquitectura
- Especificación de cada microservicio
- Tecnologías y stack

✅ **ADRs (Architecture Decision Records)**:
- ADR-001: Event-Driven Architecture
- ADR-002: Database per Service Pattern
- ADR-003: IIS como Servidor Web
- ADR-004: BIT como Plataforma de Componentes

✅ **Catálogo de Eventos**:
- Especificación completa de eventos
- Schemas JSON
- Productores y consumidores
- Convenciones y versionado

✅ **Guías de Desarrollo**:
- Patrones arquitectónicos (Saga, CQRS)
- Estándares de código
- Convenciones de desarrollo
- Mejores prácticas

✅ **Gestión de Proyecto**:
- BACKLOG.md con 10 historias de usuario iniciales
- Manual de Product Owner con metodología Kanban
- Guía de Kanban para el equipo
- Plantilla para agregar nuevas historias

✅ **Sistema de Ideas y Tareas**:
- IDEAS.md para captura rápida de ideas
- task-template.md con formato completo de tareas técnicas
- Flujo automatizado: Ideas → User Stories → Tasks → ClickUp
- Guía de integración con ClickUp (manual, CSV, API)
- **🤖 Procesador Automático de Ideas** (scripts/idea_processor/):
  - Detección automática de duplicados con IA
  - Generación de historias de usuario desde ideas
  - Actualización automática de IDEAS.md y BACKLOG.md

## 🚀 Próximos Pasos

### Fase 1: Infraestructura Base
- [ ] Configurar entorno de desarrollo
- [ ] Setup de IIS y Application Pools
- [ ] Configurar RabbitMQ / Azure Service Bus
- [ ] Setup de bases de datos SQL Server

### Fase 2: Componentes BIT
- [ ] Crear componentes de contratos (eventos, DTOs)
- [ ] Implementar event bus abstractions
- [ ] Crear shared infrastructure components

### Fase 3: Implementación de Servicios
- [ ] Orders API (implementación)
- [ ] Inventory API (implementación)
- [ ] Payments API (implementación)
- [ ] Notifications API (implementación)

### Fase 4: Testing e Integración
- [ ] Unit tests
- [ ] Integration tests
- [ ] Contract tests
- [ ] End-to-end tests

### Fase 5: CI/CD y Deployment
- [ ] Pipeline de CI/CD
- [ ] Deployment automation
- [ ] Monitoring y alertas

## 📚 Documentación

### Para Desarrolladores

- **[Instrucciones de Copilot](.github/copilot-instructions.md)**: Lee esto primero para entender cómo Copilot te ayudará
- **[Arquitectura](docs/architecture/README.md)**: Visión general del sistema
- **[Guías de Desarrollo](docs/guides/README.md)**: Patrones y mejores prácticas
- **[Catálogo de Eventos](docs/events/README.md)**: Todos los eventos del sistema

### Para Arquitectos

- **[ADRs](docs/adr/README.md)**: Decisiones arquitectónicas importantes
- **[Saga Pattern](docs/guides/saga-pattern.md)**: Implementación de transacciones distribuidas

### Por Servicio

Cada microservicio tiene su archivo `.copilot-context.md` con:
- Responsabilidades del servicio
- Eventos publicados y consumidos
- Reglas de negocio
- Estructura del proyecto
- Dependencias

## 🤝 Contribuir

Este proyecto está diseñado para ser construido con la asistencia de GitHub Copilot. Los archivos de contexto proporcionan toda la información necesaria para que Copilot genere código alineado con la arquitectura.

### Usando GitHub Copilot

1. **Lee el contexto**: Revisa `.github/copilot-instructions.md`
2. **Servicio específico**: Lee `.copilot-context.md` del servicio en el que trabajarás
3. **Consulta eventos**: Revisa `docs/events/` para eventos relacionados
4. **Pregunta a Copilot**: Copilot tiene contexto de toda la documentación

### Workflow

1. Crea un branch para tu feature
2. Consulta documentación relevante
3. Usa Copilot para generar código siguiendo los patrones
4. Escribe tests
5. Crea Pull Request

## 🔒 Principios de Diseño

### Microservicios
- ✅ Independencia y autonomía
- ✅ Database per service
- ✅ Comunicación por eventos
- ❌ Sin dependencias directas

### Event-Driven
- ✅ Desacoplamiento temporal
- ✅ Consistencia eventual
- ✅ Idempotencia obligatoria
- ✅ Saga pattern para transacciones

### Resiliencia
- ✅ Circuit breakers
- ✅ Retry policies
- ✅ Timeouts apropiados
- ✅ Health checks

## 📊 Flujo de Negocio Principal

### Creación de Orden (Happy Path)

```
1. Cliente crea orden → Orders API
   └─> Publica: OrderCreatedEvent

2. Inventory API reserva stock
   └─> Publica: InventoryReservedEvent

3. Payments API procesa pago
   └─> Publica: PaymentApprovedEvent

4. Orders API confirma orden
   └─> Publica: OrderConfirmedEvent

5. Notifications API envía confirmación
   └─> Email + Push notification
```

### Compensación (Pago Falla)

```
1-2. [Igual que arriba]

3. Payments API rechaza pago
   └─> Publica: PaymentRejectedEvent

4. Inventory API libera stock
   └─> Publica: InventoryReleasedEvent

5. Orders API cancela orden
   └─> Publica: OrderCancelledEvent

6. Notifications API notifica cancelación
```

## 🛠️ Tecnologías Clave

### Frontend
- **React**: UI library con component-based architecture
- **Vite**: Build tool ultra-rápido con HMR instantáneo
- **TypeScript**: Type safety para mejor DX
- **React Router**: Client-side routing
- **TanStack Query**: Server state management
- **Zustand**: Client state management
- **Tailwind CSS**: Utility-first CSS framework
- **Vitest**: Test runner

### Backend
- **FastAPI**: Framework web moderno con auto-documentación
- **Pydantic**: Validación de datos con type hints
- **SQLAlchemy**: ORM para PostgreSQL
- **Uvicorn**: ASGI server de alto rendimiento
- **aio-pika**: Cliente RabbitMQ asíncrono
- **pytest**: Testing framework
- **structlog**: Logging estructurado
- **Alembic**: Database migrations

## 📝 Licencia

[Definir licencia]

## 👥 Equipo

- **Architecture Team**: Responsable de decisiones arquitectónicas
- **Development Teams**: Un equipo por microservicio

## 📞 Contacto

- Slack: #architecture
- Email: architecture@company.com
- Wiki: [Link al wiki interno]

---

**Nota**: Este proyecto está en fase de planeación. La implementación seguirá las especificaciones documentadas en los archivos de contexto y guías.
