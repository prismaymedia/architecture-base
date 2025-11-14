# Remote Spotify Player para Aplicaciones DJ

> **Arquitectura**: Event-Driven Microservices  
> **Frontend**: React 18+ con Vite  
> **Backend**: Python con FastAPI  
> **Cloud Platform**: Google Cloud Platform (GCP)  
> **Metodología**: Kanban  
> **Estado**: Planeación y Diseño Arquitectónico

Sistema de reproducción remota de Spotify distribuido basado en microservicios con arquitectura orientada a eventos, diseñado para integrarse con aplicaciones DJ profesionales como Rekordbox, Serato, Traktor y consolas DJ. Construido con React para el frontend y Python para el backend, desplegado completamente en GCP.

## 🏗️ Arquitectura

Este proyecto implementa un sistema de microservicios desacoplados que se comunican mediante eventos asíncronos para permitir el control remoto de reproducción de Spotify desde aplicaciones DJ. Cada servicio tiene su propia base de datos y es independientemente desplegable en GCP.

### Microservicios

- **Spotify Integration API**: Gestión de autenticación, conexión y comunicación con Spotify Web API
- **Playback Control API**: Control de reproducción (play, pause, skip, volume, seek)
- **Sync Service**: Sincronización en tiempo real del estado de reproducción entre dispositivos
- **DJ Console Integration API**: Integración con protocolos MIDI/HID de consolas DJ y software DJ

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

#### Infrastructure (GCP)
- **Mensajería**: Google Cloud Pub/Sub (event-driven communication)
- **Base de Datos**: Cloud SQL for PostgreSQL (database per service)
- **Caché**: Cloud Memorystore for Redis
- **Logging**: Google Cloud Logging (structured logging)
- **Monitoring**: Google Cloud Monitoring + Cloud Trace
- **API Gateway**: Cloud Endpoints / API Gateway
- **Containerization**: Cloud Run (serverless containers)
- **Real-time**: Cloud Firestore for real-time sync
- **Storage**: Cloud Storage (for assets, playlists, metadata)

## 📁 Estructura del Proyecto

```
architecture-base/
├── .github/
│   └── copilot-instructions.md          # Instrucciones globales para GitHub Copilot
├── frontend/                             # Frontend React + Vite (DJ Controller UI)
│   ├── src/
│   │   ├── components/                   # React components (player controls, playlists)
│   │   ├── pages/                        # Page components (routes)
│   │   ├── hooks/                        # Custom hooks (useSpotifyPlayer, useSync)
│   │   ├── services/                     # API clients
│   │   ├── stores/                       # State management (playback state)
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
│   │   ├── 005-react-vite-frontend.md
│   │   ├── 006-python-backend.md
│   │   ├── 007-gcp-cloud-platform.md     # ✨ NEW - GCP as cloud provider
│   │   ├── 008-spotify-api-integration.md # ✨ NEW - Spotify Web API
│   │   └── 009-realtime-sync.md          # ✨ NEW - Real-time state sync
│   ├── events/                           # Catálogo de eventos
│   │   ├── README.md                     # Documentación de eventos
│   │   ├── spotify/                      # Eventos de Spotify Integration API
│   │   ├── playback/                     # Eventos de Playback Control API
│   │   ├── sync/                         # Eventos de Sync Service
│   │   └── dj-console/                   # Eventos de DJ Console Integration API
│   ├── guides/                           # Guías de desarrollo
│   │   ├── README.md                     # Índice de guías
│   │   ├── saga-pattern.md               # Guía del patrón Saga
│   │   ├── spotify-integration.md        # ✨ NEW - Guía de integración con Spotify
│   │   ├── midi-protocol.md              # ✨ NEW - Protocolo MIDI/HID
│   │   ├── product-owner-guide.md        # Manual para Product Owner
│   │   ├── kanban-guide.md               # Guía de Kanban para el equipo
│   │   ├── idea-to-task-flow.md          # 🔄 Flujo de ideas a tareas
│   │   └── clickup-integration.md        # 🚀 Integración con ClickUp
│   ├── backlog-template.md               # Plantilla de historia de usuario
│   └── task-template.md                  # 📄 Plantilla de tarea técnica
├── services/                             # Backend microservices (Python on GCP Cloud Run)
│   ├── spotify-integration-api/
│   │   ├── app/
│   │   │   ├── api/                      # API endpoints (OAuth, token management)
│   │   │   ├── core/                     # Config & settings
│   │   │   ├── domain/                   # Business logic (Spotify SDK wrapper)
│   │   │   ├── application/              # Use cases
│   │   │   ├── infrastructure/           # GCP services, Pub/Sub, Cloud SQL
│   │   │   └── main.py                   # FastAPI app
│   │   ├── tests/
│   │   ├── pyproject.toml
│   │   └── .copilot-context.md          # Contexto específico del servicio
│   ├── playback-control-api/
│   │   └── .copilot-context.md
│   ├── sync-service/
│   │   └── .copilot-context.md
│   └── dj-console-integration-api/
│       └── .copilot-context.md
├── shared/                               # Shared code
│   ├── frontend/                         # Shared React components/utils
│   └── backend/                          # Shared Python packages (GCP clients, event schemas)
├── IDEAS.md                              # 💡 Captura rápida de ideas
├── BACKLOG.md                            # 📋 Product backlog con historias de usuario
├── docker-compose.yml                    # Local development setup
└── README.md                             # Este archivo
```

## 📋 Gestión de Proyecto - Kanban

Este proyecto utiliza **metodología Kanban** para gestión continua del flujo de trabajo.

### Product Backlog

El [BACKLOG.md](BACKLOG.md) contiene todas las historias de usuario del proyecto:

- **🔴 Prioridad Alta**: US-001 (Autenticación Spotify), US-002 (Control de Reproducción), US-003 (Sincronización en Tiempo Real)
- **🟡 Prioridad Media**: US-004 (Integración MIDI), US-005 (Gestión de Playlists), US-006 (Estado de Playback)
- **🟢 Prioridad Baja**: US-007 (Analytics de Uso), US-008 (Soporte Multi-dispositivo), US-009 (Presets DJ), US-010 (Integración Rekordbox)

### Estados del Kanban

1. **To Do**: Historias refinadas, listas para trabajarse
2. **In Progress**: En desarrollo activo (WIP: máximo 5)
3. **In Review**: En code review o QA (WIP: máximo 3)
4. **Done**: Completadas y en producción

### Métricas del Proyecto

El archivo [`project_config.yaml`](project_config.yaml) centraliza las métricas de tareas:

```yaml
project_metrics:
  backlog_tasks_count: 0          # Tareas en backlog
  qa_tasks_pending_count: 0       # Tareas pendientes en QA
  qa_tasks_in_progress_count: 0   # Tareas en curso en QA
```

**Actualización manual**: Los valores deben actualizarse manualmente según el estado real de las tareas.

**Uso programático**: Scripts Python, herramientas CI/CD y documentación pueden leer estos valores:

```python
import yaml
with open('project_config.yaml') as f:
    config = yaml.safe_load(f)
    backlog_count = config['project_metrics']['backlog_tasks_count']
```

Ver [Guía de Uso de project_config.yaml](docs/guides/project-config-usage.md) para más detalles.

### Documentación de Gestión

- 📖 [Manual de Product Owner](docs/guides/product-owner-guide.md) - Gestión del backlog con Kanban
- 📖 [Guía de Kanban](docs/guides/kanban-guide.md) - Workflow para el equipo
- 📝 [Plantilla de Historia](docs/backlog-template.md) - Para agregar nuevas features
- 📊 [Uso de project_config.yaml](docs/guides/project-config-usage.md) - Métricas centralizadas

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
- ADR-005: React + Vite Frontend
- ADR-006: Python + FastAPI Backend
- ADR-007: GCP as Cloud Platform (NEW)
- ADR-008: Spotify API Integration Strategy (NEW)
- ADR-009: Real-time Sync with Cloud Firestore (NEW)

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
- BACKLOG.md con 10 historias de usuario iniciales para sistema DJ remoto
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

### Fase 1: Infraestructura Base en GCP
- [ ] Configurar proyecto GCP y habilitar APIs necesarias
- [ ] Setup de Cloud Pub/Sub para mensajería entre servicios
- [ ] Configurar Cloud SQL for PostgreSQL (instancias por servicio)
- [ ] Setup de Cloud Memorystore for Redis (caché)
- [ ] Configurar Cloud Run para servicios containerizados
- [ ] Setup de Cloud Firestore para sincronización en tiempo real

### Fase 2: Integración con Spotify
- [ ] Registrar aplicación en Spotify Developer Dashboard
- [ ] Implementar flujo OAuth 2.0 para autenticación
- [ ] Crear wrapper para Spotify Web API
- [ ] Implementar manejo de tokens y refresh
- [ ] Crear componentes compartidos para SDK de Spotify

### Fase 3: Implementación de Servicios
- [ ] Spotify Integration API (autenticación, conexión)
- [ ] Playback Control API (play, pause, skip, volume)
- [ ] Sync Service (estado en tiempo real)
- [ ] DJ Console Integration API (MIDI/HID protocols)

### Fase 4: Testing e Integración
- [ ] Unit tests
- [ ] Integration tests con Spotify API (mocks)
- [ ] Contract tests para eventos
- [ ] End-to-end tests de flujos DJ
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
- **[ADR-007: Trunk-Based Development](docs/adr/007-trunk-based-development.md)**: Estrategia de control de versiones
- **[Saga Pattern](docs/guides/saga-pattern.md)**: Implementación de transacciones distribuidas
- **[Version Control Workflow](docs/guides/version-control-workflow.md)**: Flujo de trabajo con Git

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

1. Crea un branch siguiendo [Version Control Workflow](docs/guides/version-control-workflow.md)
2. Consulta documentación relevante
3. Usa Copilot para generar código siguiendo los patrones
4. Usa [Feature Flags](docs/guides/feature-flags.md) para trabajo incompleto
5. Escribe tests
6. Sigue [Code Review Guidelines](docs/guides/code-review.md)
7. Crea Pull Request

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

### Control de Versiones
- ✅ Trunk-Based Development
- ✅ Feature flags para trabajo incompleto
- ✅ Integración frecuente (diaria)
- ✅ Main branch siempre desplegable
- 📚 Ver [Version Control Workflow](docs/guides/version-control-workflow.md)

## 📊 Flujo de Negocio Principal

### Control Remoto de Reproducción (Happy Path)

```
1. DJ autentica con Spotify → Spotify Integration API
   └─> Publica: UserAuthenticatedEvent
   └─> Obtiene tokens OAuth y dispositivos disponibles

2. DJ inicia reproducción desde app → Playback Control API
   └─> Publica: PlaybackCommandEvent (play, track_uri, device_id)

3. Playback Control API envía comando a Spotify Web API
   └─> Publica: PlaybackStateChangedEvent (playing, track_info, position)

4. Sync Service distribuye estado a dispositivos conectados
   └─> Actualiza Cloud Firestore con estado actual
   └─> Publica: SyncStateUpdatedEvent

5. Frontend/DJ Console recibe actualización en tiempo real
   └─> UI se actualiza con estado de reproducción
   └─> Controles MIDI reflejan estado actual
```

### Integración con Consola DJ (MIDI/HID)

```
1. DJ conecta consola física → DJ Console Integration API
   └─> Detecta dispositivo MIDI/HID
   └─> Publica: DeviceConnectedEvent

2. DJ mueve fader de volumen en consola → MIDI message
   └─> DJ Console Integration API captura evento
   └─> Publica: VolumeChangeCommandEvent

3. Playback Control API procesa comando
   └─> Ajusta volumen en Spotify
   └─> Publica: VolumeChangedEvent

4. Sync Service sincroniza estado
   └─> Actualiza todos los dispositivos conectados
```

### Compensación (Error de Spotify API)

```
1-2. [Igual que arriba]

3. Spotify API retorna error (rate limit, token expirado, etc.)
   └─> Publica: PlaybackCommandFailedEvent

4. Playback Control API implementa retry con backoff
   └─> Intenta renovar token si es necesario
   └─> Reintenta comando hasta 3 veces

5. Si falla permanentemente:
   └─> Publica: PlaybackErrorEvent
   └─> Sync Service notifica a dispositivos
   └─> Frontend muestra error al DJ

6. DJ recibe feedback visual/MIDI
   └─> Indicador LED en consola (rojo = error)
   └─> Mensaje en pantalla con detalles del error
```

## 🛠️ Tecnologías Clave

### Frontend (DJ Controller UI)
- **React**: UI library con component-based architecture
- **Vite**: Build tool ultra-rápido con HMR instantáneo
- **TypeScript**: Type safety para mejor DX
- **React Router**: Client-side routing
- **TanStack Query**: Server state management para API calls
- **Zustand**: Client state management para estado de playback
- **Tailwind CSS**: Utility-first CSS framework
- **Web MIDI API**: Para integración directa con controladores MIDI
- **Web Audio API**: Para visualizaciones y análisis de audio
- **Vitest**: Test runner

### Backend (Microservices on GCP)
- **FastAPI**: Framework web moderno con auto-documentación y async support
- **Pydantic**: Validación de datos con type hints
- **SQLAlchemy**: ORM asíncrono para Cloud SQL PostgreSQL
- **Uvicorn**: ASGI server de alto rendimiento
- **google-cloud-pubsub**: Cliente Python para Cloud Pub/Sub
- **google-cloud-firestore**: Cliente para Firestore (real-time sync)
- **spotipy**: Biblioteca Python para Spotify Web API
- **python-rtmidi**: Para integración MIDI en backend
- **pytest**: Testing framework
- **structlog**: Logging estructurado integrado con Cloud Logging
- **Alembic**: Database migrations para Cloud SQL

### GCP Services
- **Cloud Run**: Serverless containers para microservices
- **Cloud Pub/Sub**: Event-driven messaging entre servicios
- **Cloud SQL**: PostgreSQL managed (database per service)
- **Cloud Firestore**: NoSQL real-time database para estado de playback
- **Cloud Memorystore**: Redis managed para caché
- **Cloud Storage**: Almacenamiento de assets (artwork, metadata)
- **Cloud Logging**: Logging centralizado y estructurado
- **Cloud Monitoring**: Métricas y alertas
- **Cloud Trace**: Distributed tracing
- **Secret Manager**: Gestión segura de API keys (Spotify credentials)
- **Cloud Endpoints / API Gateway**: API management y rate limiting

## 📝 Licencia

[Definir licencia]

## 👥 Equipo

- **Architecture Team**: Responsable de decisiones arquitectónicas y patrones
- **Backend Team**: Implementación de microservices en Python/GCP
- **Frontend Team**: Desarrollo de UI de control DJ
- **Integration Team**: Integración con Spotify API y protocolos MIDI
- **DevOps Team**: Infraestructura GCP y CI/CD

## 📞 Contacto

- Slack: #spotify-dj-remote
- Email: dj-platform@company.com
- Wiki: [Link al wiki interno]

---

**Nota**: Este proyecto está en fase de planeación. La implementación seguirá las especificaciones documentadas en los archivos de contexto y guías. El objetivo es crear un sistema robusto y escalable para control remoto de Spotify desde aplicaciones DJ profesionales, desplegado completamente en Google Cloud Platform.
