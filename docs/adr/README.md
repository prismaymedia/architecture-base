# Architecture Decision Records (ADRs)

Este directorio contiene todas las decisiones arquitectónicas importantes del proyecto Remote Spotify Player para aplicaciones DJ. Cada ADR documenta una decisión significativa, su contexto, alternativas consideradas y consecuencias.

## Formato de ADR

Cada ADR sigue la estructura:

- **Estado**: Propuesto / Aceptado / Rechazado / Deprecado / Superseded
- **Fecha**: Fecha de la decisión
- **Decisores**: Quién participó en la decisión
- **Contexto**: Situación que llevó a la decisión
- **Decisión**: Qué se decidió
- **Justificación**: Por qué se tomó esta decisión
- **Alternativas**: Qué otras opciones se consideraron
- **Consecuencias**: Impacto positivo y negativo
- **Referencias**: Links a documentos relacionados

## Lista de ADRs

| # | Título | Estado | Fecha |
|---|--------|--------|-------|
| [001](001-event-driven-architecture.md) | Event-Driven Architecture | Aceptado | 2025-11-14 |
| [002](002-database-per-service.md) | Database per Service Pattern | Aceptado | 2025-11-14 |
| [003](003-iis-web-server.md) | Uso de IIS como Servidor Web | Superseded | 2025-11-14 |
| [004](004-bit-components-platform.md) | BIT como Plataforma de Componentes | Superseded | 2025-11-14 |
| [005](005-react-vite-frontend.md) | React con Vite para el Frontend | Aceptado | 2025-11-14 |
| [006](006-python-backend.md) | Python para Backend de Microservicios | Aceptado | 2025-11-14 |
| [007](007-trunk-based-development.md) | Trunk-Based Development Strategy | Aceptado | 2025-11-14 |

## Decisiones Fundamentales

Las decisiones 001-002, 005-007 forman el núcleo de nuestra arquitectura:

### Core Architecture
1. **Event-Driven** (ADR-001): Comunicación asíncrona entre servicios
2. **Database per Service** (ADR-002): Independencia de datos por microservicio

### Technology Stack
3. **React + Vite Frontend** (ADR-005): Framework moderno para UI de control DJ
4. **Python Backend** (ADR-006): Microservicios con FastAPI
5. **Trunk-Based Development** (ADR-007): Estrategia de control de versiones y cambios

### Cloud & Integration (NEW)
5. **GCP as Cloud Platform** (ADR-007): Google Cloud Platform para infraestructura serverless
6. **Spotify Web API** (ADR-008): Integración oficial con Spotify para control de reproducción
7. **Cloud Firestore Real-time Sync** (ADR-009): Sincronización en tiempo real de estado de playback

### Decisiones Superseded

- **IIS Web Server** (ADR-003): Reemplazado por Cloud Run (GCP) + Uvicorn/Vite
- **BIT Components** (ADR-004): Reemplazado por npm packages (frontend) y Python packages (backend)

## Proceso de ADR

### Crear un Nuevo ADR

1. Copia la plantilla `adr-template.md`
2. Nombra el archivo: `XXX-descripcion-corta.md`
3. Completa todas las secciones
4. Solicita review del equipo de arquitectura
5. Actualiza este README con la nueva entrada

### Estados

- **Propuesto**: En discusión, no implementado
- **Aceptado**: Aprobado y en uso
- **Rechazado**: Evaluado pero no seleccionado
- **Deprecado**: Ya no se usa, pero fue válido
- **Superseded**: Reemplazado por otro ADR (incluir link)

### Modificar un ADR Existente

Los ADRs son inmutables una vez aceptados. Para cambiar una decisión:

1. Crear nuevo ADR que supersede el anterior
2. Marcar el ADR viejo como "Superseded by ADR-XXX"
3. Explicar en el nuevo ADR por qué se cambió

## ADRs Planificados

Próximas decisiones arquitectónicas a documentar:

### DJ & Spotify Specific
- [ ] MIDI Protocol Integration Strategy (controladores DJ)
- [ ] Audio Analysis and BPM Detection (fallback cuando Spotify no provee)
- [ ] Offline Mode and Caching Strategy
- [ ] Crossfade and Mixing Implementation
- [ ] Integration with DJ Software (Rekordbox, Serato)

### General Architecture
- [ ] Estrategia de API Versioning
- [ ] Autenticación y Autorización (OAuth 2.0 con Spotify + JWT)
- [ ] Estrategia de Testing (Unit, Integration, E2E)
- [ ] Observabilidad y Monitoring (Cloud Monitoring + Logging)
- [ ] CI/CD Pipeline Architecture (Cloud Build + Cloud Run)
- [ ] Disaster Recovery y Backup Strategy
- [ ] Performance Testing Strategy
- [ ] Rate Limiting and Throttling Strategy
- [ ] WebSocket vs Server-Sent Events for Real-time Commands

## Referencias

- [Architecture Overview](../architecture/README.md)
- [Guías de Desarrollo](../guides/README.md)
- [Catálogo de Eventos](../events/README.md)

## Recursos Externos

- [ADR GitHub Organization](https://adr.github.io/)
- [Documenting Architecture Decisions](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions)
- [ThoughtWorks ADR Tools](https://github.com/npryce/adr-tools)
- [Spotify Web API Documentation](https://developer.spotify.com/documentation/web-api)
- [GCP Architecture Center](https://cloud.google.com/architecture)
