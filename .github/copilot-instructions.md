# Instrucciones Globales para GitHub Copilot

## Contexto del Proyecto

Este es un **sistema de Remote Spotify Player para aplicaciones DJ** construido con arquitectura orientada a eventos. El proyecto permite controlar Spotify remotamente desde consolas DJ y aplicaciones como Rekordbox, con sincronización en tiempo real entre múltiples dispositivos. El proyecto utiliza:

- **Frontend**: React 18+ con Vite como build tool y TypeScript para UI de control DJ
- **Backend**: Python 3.12+ con FastAPI para microservicios
- **Cloud Platform**: Google Cloud Platform (GCP) con servicios serverless
- **Event-Driven Architecture**: Comunicación asíncrona entre servicios con Cloud Pub/Sub
- **Real-time Sync**: Cloud Firestore para sincronización de estado de playback (<100ms latency)

## Arquitectura General

### Microservicios

1. **Spotify Integration API** - Autenticación OAuth y comunicación con Spotify Web API
2. **Playback Control API** - Control de reproducción (play, pause, volume, seek)
3. **Sync Service** - Sincronización en tiempo real del estado de playback vía Firestore
4. **DJ Console Integration API** - Integración con controladores MIDI/HID y hardware DJ

### Patrones de Comunicación

- **Eventos Asíncronos**: Para comunicación entre servicios (Cloud Pub/Sub)
- **REST APIs**: Para comunicación síncrona (FastAPI endpoints)
- **Real-time Sync**: Cloud Firestore para estado de playback en tiempo real
- **OAuth 2.0**: Para autenticación con Spotify

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

#### Backend (Python)
- **Eventos**: PasadoTense + Sufijo "Event" (ej: `UserAuthenticatedEvent`, `PlaybackStateChangedEvent`)
- **Comandos**: Imperativo + Sufijo "Command" (ej: `StartPlaybackCommand`, `RefreshTokenCommand`)
- **Handlers**: Nombre del mensaje + "Handler" (ej: `UserAuthenticatedEventHandler`, `MIDICommandHandler`)
- **Servicios**: Sustantivo + "Service" (ej: `SpotifyService`, `PlaybackService`, `SyncService`)
- **Variables/Funciones**: snake_case (ej: `get_playback_state`, `refresh_spotify_token`)
- **Clases**: PascalCase (ej: `SpotifyUser`, `PlaybackRepository`, `MIDIDevice`)
- **Constantes**: UPPER_SNAKE_CASE (ej: `MAX_RETRY_ATTEMPTS`, `SPOTIFY_API_TIMEOUT`)

#### Frontend (React/TypeScript)
- **Componentes**: PascalCase (ej: `PlaybackControls`, `TrackDisplay`, `VolumeSlider`)
- **Hooks**: camelCase con prefijo "use" (ej: `useSpotifyPlayer`, `usePlaybackState`, `useMIDIDevice`)
- **Funciones**: camelCase (ej: `startPlayback`, `handleVolumeChange`, `syncPlaybackState`)
- **Interfaces/Types**: PascalCase con prefijo "I" o sufijo "Props" (ej: `ITrack`, `PlaybackControlsProps`)
- **Constantes**: UPPER_SNAKE_CASE (ej: `SPOTIFY_API_BASE_URL`, `MAX_VOLUME`)

### Estructura de Proyecto

#### Backend (Python/FastAPI)
```
services/
├── {service-name}/
│   ├── app/
│   │   ├── api/           # FastAPI endpoints (routers)
│   │   ├── core/          # Configuration, settings
│   │   ├── application/   # Use cases, command/query handlers
│   │   ├── domain/        # Domain models, business logic
│   │   ├── infrastructure/ # DB, messaging, external services
│   │   ├── events/        # Event schemas and handlers
│   │   ├── schemas/       # Pydantic request/response models
│   │   └── main.py        # FastAPI application entry point
│   ├── tests/
│   │   ├── unit/
│   │   ├── integration/
│   │   └── conftest.py
│   ├── pyproject.toml     # Python dependencies (Poetry)
│   └── .copilot-context.md
```

#### Frontend (React/Vite)
```
frontend/
├── src/
│   ├── components/        # Reusable React components
│   │   ├── common/        # Shared components
│   │   └── features/      # Feature-specific components
│   ├── pages/             # Page components (routes)
│   ├── hooks/             # Custom React hooks
│   ├── services/          # API clients
│   ├── stores/            # State management (Zustand)
│   ├── types/             # TypeScript types
│   ├── utils/             # Utility functions
│   └── App.tsx
├── tests/
└── vite.config.ts
```

## Tecnologías y Stack

### Frontend (React + Vite)

- **React 18+**: UI library con hooks y concurrent features
- **Vite 5+**: Build tool con HMR ultra-rápido
- **TypeScript 5+**: Type safety
- **React Router v6**: Client-side routing
- **TanStack Query**: Server state management
- **Zustand**: Client state management
- **Tailwind CSS**: Utility-first styling
- **shadcn/ui**: Component library
- **Vitest**: Testing framework
- **React Testing Library**: Component testing

### Backend (Python + FastAPI)

- **Python 3.12+**: Latest stable version
- **FastAPI**: Modern async web framework
- **Uvicorn**: ASGI server
- **Pydantic v2**: Data validation with type hints
- **SQLAlchemy 2.0**: ORM asíncrono
- **Alembic**: Database migrations
- **aio-pika**: RabbitMQ async client
- **pytest**: Testing framework
- **structlog**: Structured logging
- **black**: Code formatting
- **ruff**: Fast linting
- **mypy**: Static type checking

### Infraestructura

- **PostgreSQL**: Base de datos principal (database per service)
- **RabbitMQ**: Message broker para eventos
- **Redis**: Caché distribuido
- **Docker**: Containerization
- **Docker Compose**: Local development orchestration

### Shared Code

#### Frontend
- npm packages para componentes React compartidos
- Shared utilities y types
- Common API client configurations

#### Backend
- Python packages (pip/poetry) para código compartido
- Event contracts y schemas compartidos
- Common middleware y utilities

## Reglas Importantes

### ❌ NO hacer

- NO crear dependencias directas entre microservicios
- NO compartir bases de datos entre servicios
- NO hacer llamadas síncronas si se puede usar eventos
- NO incluir lógica de negocio en controladores
- NO exponer entidades de dominio directamente

### ✅ SÍ hacer

#### General
- SÍ usar DTOs/Schemas para todas las APIs
- SÍ validar eventos y comandos
- SÍ implementar idempotencia en handlers
- SÍ usar logging estructurado
- SÍ documentar todos los eventos publicados/consumidos

#### Backend (Python)
- SÍ usar type hints en todas las funciones
- SÍ usar async/await para operaciones I/O
- SÍ usar Pydantic para validación de datos
- SÍ implementar health checks en todos los servicios
- SÍ seguir Clean Architecture (domain, application, infrastructure)
- SÍ usar black + ruff para formateo consistente
- SÍ usar pytest con fixtures para testing

#### Frontend (React)
- SÍ usar TypeScript strict mode
- SÍ usar React hooks (useState, useEffect, useCallback, etc.)
- SÍ implementar error boundaries
- SÍ usar React Query para server state
- SÍ implementar code splitting con React.lazy
- SÍ usar Tailwind para estilos
- SÍ seguir principios de composición sobre herencia

## Testing

### Backend (Python)
- **Unit tests**: Para lógica de dominio (pytest)
- **Integration tests**: Para event handlers y database
- **Contract tests**: Para eventos compartidos
- **API tests**: Para endpoints FastAPI (httpx + TestClient)
- **Coverage**: Mínimo 80% de cobertura

### Frontend (React)
- **Unit tests**: Para hooks y utilities (Vitest)
- **Component tests**: Para componentes React (Testing Library)
- **Integration tests**: Para flujos completos
- **E2E tests**: Para user journeys críticos (Playwright - opcional)
- **Coverage**: Mínimo 70% de cobertura

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
