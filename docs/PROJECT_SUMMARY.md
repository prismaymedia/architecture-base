# 🎵 Remote Spotify Player para DJ - Resumen del Proyecto

> **Fecha**: 2025-11-14  
> **Estado**: Planeación Arquitectónica Completa  
> **Cloud Platform**: Google Cloud Platform (GCP)  
> **Dominio**: Música DJ / Control Remoto de Spotify

---

## 🎯 Visión del Proyecto

Sistema de control remoto de Spotify diseñado específicamente para DJs profesionales, permitiendo controlar la reproducción desde consolas DJ (controladores MIDI/HID) y aplicaciones DJ como Rekordbox, Serato o Traktor. El sistema sincroniza el estado de playback en tiempo real (<100ms) entre múltiples dispositivos.

### Casos de Uso Principales

1. **DJ en Venue**: Controlar Spotify desde controlador MIDI (Pioneer DDJ, Traktor Kontrol) con feedback táctil y visual
2. **Home DJ Setup**: Sincronizar playback entre laptop (Rekordbox) y tablet (control visual)
3. **Mobile DJ**: Controlar música desde phone mientras se proyecta en screen/speakers
4. **Collaborative Sets**: Múltiples DJs controlando el mismo playback (B2B sets)

---

## 🏗️ Arquitectura del Sistema

### Stack Tecnológico

#### Frontend
- **Framework**: React 18+ con TypeScript
- **Build Tool**: Vite 5+
- **State Management**: 
  - TanStack Query (server state)
  - Zustand (client state - playback controls)
- **Real-time**: Firestore SDK con real-time listeners
- **Hardware**: Web MIDI API para controladores MIDI en browser
- **Styling**: Tailwind CSS + shadcn/ui

#### Backend
- **Language**: Python 3.12+
- **Framework**: FastAPI (async)
- **ORM**: SQLAlchemy 2.0 (async)
- **Spotify SDK**: spotipy (con customizaciones)
- **MIDI**: python-rtmidi
- **Validation**: Pydantic v2

#### GCP Services
- **Compute**: Cloud Run (serverless containers, auto-scaling)
- **Messaging**: Cloud Pub/Sub (event-driven architecture)
- **Database**: 
  - Cloud SQL for PostgreSQL (transaccional data)
  - Cloud Firestore (real-time sync del estado de playback)
- **Cache**: Cloud Memorystore for Redis
- **Security**: Secret Manager (Spotify credentials, tokens)
- **Observability**: Cloud Logging + Monitoring + Trace
- **Storage**: Cloud Storage (assets, metadata, backups)

### Microservicios (4 servicios)

```
┌─────────────────────────────────────────────────────────────┐
│                    Frontend (React + Vite)                  │
│        DJ Controller UI + Waveform Visualizations           │
└────────────────────────┬────────────────────────────────────┘
                         │ HTTPS/REST
                         ▼
┌─────────────────────────────────────────────────────────────┐
│           Cloud Endpoints / API Gateway (GCP)                │
└───┬─────────────┬──────────────┬─────────────────────┬──────┘
    │             │              │                     │
    ▼             ▼              ▼                     ▼
┌──────────┐ ┌──────────┐ ┌─────────────┐ ┌──────────────────┐
│ Spotify  │ │ Playback │ │ DJ Console  │ │   Sync Service   │
│Integration│ │ Control  │ │ Integration │ │  (Real-time)     │
│   API    │ │   API    │ │    API      │ │                  │
│          │ │          │ │  (MIDI/HID) │ │                  │
└────┬─────┘ └────┬─────┘ └──────┬──────┘ └────────┬─────────┘
     │            │              │                  │
     └────────────┴──────────────┴──────────────────┘
                         │
                         ▼
              ┌──────────────────────┐
              │  Cloud Pub/Sub       │
              │  (Event Bus)         │
              └──────────┬───────────┘
                         │
         ┌───────────────┴────────────────┐
         │                                │
         ▼                                ▼
┌──────────────────┐           ┌──────────────────┐
│  Cloud Firestore │           │    Cloud SQL     │
│  (Real-time DB)  │           │   (PostgreSQL)   │
│                  │           │   per service    │
│ Playback State   │           │                  │
└──────────────────┘           └──────────────────┘
         │
         │ Real-time listeners
         ▼
┌─────────────────────────────────────────┐
│  Clients (Laptop, Tablet, Phone,        │
│  MIDI Controllers) - <100ms sync        │
└─────────────────────────────────────────┘
```

#### 1. Spotify Integration API
- **Responsabilidad**: Gateway a Spotify Web API
- **Funciones**: OAuth 2.0, gestión de tokens, búsqueda, metadata (BPM/key)
- **Tecnología**: FastAPI + spotipy + Secret Manager
- **Eventos**: `UserAuthenticatedEvent`, `TokenRefreshedEvent`, `DevicesUpdatedEvent`

#### 2. Playback Control API
- **Responsabilidad**: Control de reproducción de Spotify
- **Funciones**: Play/pause/skip, volumen, seek, gestión de cola
- **Tecnología**: FastAPI + spotipy
- **Eventos**: `PlaybackCommandEvent`, `PlaybackStateChangedEvent`, `VolumeChangedEvent`

#### 3. Sync Service
- **Responsabilidad**: Sincronización en tiempo real
- **Funciones**: Actualizar estado en Firestore, distribuir a dispositivos, polling a Spotify
- **Tecnología**: FastAPI + Firestore SDK + Cloud Scheduler
- **Latencia**: <100ms para updates entre dispositivos

#### 4. DJ Console Integration API
- **Responsabilidad**: Integración con hardware MIDI/HID
- **Funciones**: Detección de controladores, mapeo MIDI, feedback a LEDs/faders
- **Tecnología**: FastAPI + python-rtmidi + hidapi
- **Eventos**: `DeviceConnectedEvent`, `MIDICommandEvent`

---

## 📋 Product Backlog (10 User Stories)

### 🔴 Alta Prioridad (Core Features)

1. **US-001: Autenticación con Spotify** (8 pts)
   - OAuth 2.0 flow con Spotify Premium
   - Gestión automática de tokens
   
2. **US-002: Control Básico de Reproducción** (13 pts)
   - Play, pause, skip, volume, seek
   - Latencia <200ms
   
3. **US-003: Sincronización en Tiempo Real** (8 pts)
   - Estado de playback sincronizado en todos los dispositivos
   - Latencia <100ms usando Firestore

### 🟡 Prioridad Media

4. **US-004: Integración con Controlador MIDI** (13 pts)
   - Mapeo de faders/knobs/botones a comandos Spotify
   
5. **US-005: Gestión de Playlists y Colas** (8 pts)
   - Buscar tracks, gestionar colas, ver playlists
   
6. **US-006: Dashboard de Estado de Playback** (8 pts)
   - Waveform visualization, BPM, key, VU meter

### 🟢 Prioridad Baja

7. **US-007: Analytics de Uso y Sesiones** (8 pts)
8. **US-008: Soporte Multi-dispositivo** (5 pts)
9. **US-009: Presets y Configuraciones DJ** (5 pts)
10. **US-010: Integración con Rekordbox/Serato** (13 pts)

**Total**: 81 Story Points

---

## 🎨 Ideas para Futuras Features

1. **Crossfade Automático entre Tracks** - Transiciones suaves sin cortes
2. **Detección Automática de BPM y Key** - Para mezclas armónicas
3. **Sistema de Cue Points y Loops** - Marcar momentos clave en tracks
4. **Offline Mode con Cache** - Para venues con internet inestable
5. **Smart Playlist Recommendations** - AI-powered sugerencias contextuales
6. **Grabación de Sesiones DJ** - Con respeto a ToS de Spotify
7. **Visualizador de Espectro en Tiempo Real** - Feedback visual profesional
8. **Integración con Luces y Visuales** - DMX/Art-Net para shows
9. **Collaborative Playlists en Tiempo Real** - B2B DJ sets

---

## 🔧 Decisiones Arquitectónicas (ADRs)

### Decisiones Fundamentales

- **ADR-001**: Event-Driven Architecture ✅
- **ADR-002**: Database per Service Pattern ✅
- **ADR-005**: React + Vite Frontend ✅
- **ADR-006**: Python + FastAPI Backend ✅

### Decisiones Específicas del Proyecto (NEW)

- **ADR-007**: **GCP as Cloud Platform** ✅
  - Cloud Run para serverless compute
  - Cloud Pub/Sub para messaging
  - Cloud Firestore para real-time sync
  - Secret Manager para credenciales Spotify
  
- **ADR-008**: **Spotify Web API Integration** ✅
  - OAuth 2.0 PKCE flow
  - spotipy library como wrapper
  - Rate limiting: 180 req/min/user
  - Token auto-refresh 5 min antes de expiración
  
- **ADR-009**: **Real-time Sync with Cloud Firestore** ✅
  - Push notifications <50ms latency
  - Offline support automático
  - Last-write-wins conflict resolution
  - Costo optimizado: ~$800-1,200/mes para 1000 usuarios activos

---

## 📊 Flujos de Negocio Clave

### Flujo 1: DJ Mueve Fader de Volumen

```
1. DJ mueve fader físico en controlador MIDI
   ↓
2. DJ Console Integration API detecta MIDI CC message
   └→ Publica: MIDICommandEvent { type: "volume", value: 75 }
   
3. Playback Control API consume evento
   └→ Ejecuta: spotify.set_volume(75)
   └→ Publica: VolumeChangedEvent { volume: 75 }
   
4. Sync Service consume evento
   └→ Actualiza: Firestore /playback/{userId}/volume = 75
   
5. Firestore notifica en tiempo real (<50ms)
   └→ Frontend UI: Slider actualizado
   └→ Tablet: Volumen actualizado
   └→ Otro controlador MIDI: Fader movido (si es motorizado)

Latencia total: ~100-150ms
```

### Flujo 2: DJ Presiona Play en Frontend

```
1. Frontend: POST /api/playback/play
   ↓
2. Playback Control API:
   └→ spotify.start_playback()
   └→ Publica: PlaybackStateChangedEvent { isPlaying: true }
   
3. Sync Service:
   └→ Firestore.update({ isPlaying: true })
   
4. Real-time sync a todos los dispositivos:
   └→ Frontend: Botón cambia a "Pause"
   └→ MIDI Controller: LED "Play" enciende
   └→ Mobile app: UI actualizada

Latencia total: ~50-100ms
```

---

## 🔒 Consideraciones de Seguridad

1. **Nunca loggear** access tokens, refresh tokens o credenciales
2. **Encriptar tokens** antes de almacenar en DB
3. **HTTPS obligatorio** para todos los endpoints
4. **PKCE (Proof Key for Code Exchange)** en OAuth flow
5. **Validar redirect URI** en OAuth para prevenir CSRF
6. **Secret Manager** para todas las credenciales (no env vars)
7. **IAM granular** por servicio en GCP
8. **Rate limiting** para prevenir abuse
9. **Input validation** con Pydantic en todos los endpoints
10. **Secrets rotation** automática cada 90 días

---

## 📈 Observabilidad y Monitoring

### Métricas Clave (Cloud Monitoring)

**Por Servicio**:
- Request latency (p50, p95, p99)
- Error rate (4xx, 5xx)
- Request count
- Active connections

**Domain-Specific**:
- **Spotify Integration**: Spotify API latency, token refresh rate
- **Playback Control**: Command success rate, Spotify API errors
- **Sync Service**: Firestore write latency, sync conflict rate
- **DJ Console Integration**: MIDI message rate, device connection count

### Logging (Cloud Logging)

Structured logging con:
- `correlationId`: Trazar request across services
- `userId`: Filtrar por usuario
- `serviceName`: Identificar origen
- `logLevel`: DEBUG, INFO, WARN, ERROR

### Tracing (Cloud Trace)

Distributed tracing de end-to-end:
```
Frontend → API Gateway → Playback Control → Spotify Integration → Spotify API
                               ↓
                        Pub/Sub Publish
                               ↓
                         Sync Service → Firestore → All Clients
```

---

## 🚀 Deployment

### Cloud Run (Serverless Containers)

Cada servicio:
- **Min instances**: 0 (cost optimization)
- **Max instances**: 100 (auto-scale)
- **Memory**: 512Mi - 1Gi
- **CPU**: 1 vCPU
- **Timeout**: 60s
- **Concurrency**: 80 requests/container

### CI/CD (Cloud Build)

```
git push → Cloud Build → Build Docker Image → Push to GCR → Deploy to Cloud Run → Health Check
```

### Environments

- **Development**: `dev` namespace, separate GCP project
- **Staging**: `staging` namespace, pre-production testing
- **Production**: `prod` namespace, múltiples regiones (us-central1, europe-west1)

---

## 💰 Estimación de Costos (1000 usuarios activos)

### Cloud Run
- **Spotify Integration API**: ~$100/mes
- **Playback Control API**: ~$150/mes
- **Sync Service**: ~$80/mes
- **DJ Console Integration API**: ~$50/mes
**Subtotal**: $380/mes

### Cloud Firestore (optimizado con throttling)
- **Reads**: ~$3,000/mes → **$1,000/mes** (con caché 50%)
- **Writes**: ~$4,500/mes → **$500/mes** (con throttling 1/sec)
**Subtotal**: $1,500/mes

### Cloud SQL (4 instancias pequeñas)
- **PostgreSQL**: ~$300/mes

### Cloud Pub/Sub
- **Messages**: ~$50/mes

### Otros (Storage, Secret Manager, Logging)
- ~$100/mes

### **Total Estimado**: ~$2,330/mes para 1000 usuarios activos
**Por usuario**: ~$2.33/mes

---

## 📚 Documentación Disponible

### Core Documentation
- ✅ `README.md` - Visión general del proyecto
- ✅ `BACKLOG.md` - Product backlog con 10 user stories
- ✅ `IDEAS.md` - 9 ideas para futuras features
- ✅ `docs/SERVICES_SUMMARY.md` - Resumen detallado de microservicios

### Architecture Decision Records
- ✅ `docs/adr/007-gcp-cloud-platform.md`
- ✅ `docs/adr/008-spotify-api-integration.md`
- ✅ `docs/adr/009-realtime-sync.md`
- ✅ `docs/adr/README.md` - Índice de ADRs

### Service Context
- ✅ `services/spotify-integration-api/.copilot-context.md`
- ✅ Otros servicios documentados en `SERVICES_SUMMARY.md`

### Guides (To be created)
- [ ] `docs/guides/spotify-integration.md` - Guía de integración con Spotify
- [ ] `docs/guides/midi-protocol.md` - Protocolo MIDI/HID
- [ ] Event catalog para nuevos eventos

### Copilot Configuration
- ✅ `.github/copilot-instructions.md` - Instrucciones globales actualizadas

---

## ✅ Estado del Proyecto

### Completado ✅

- [x] Visión y arquitectura del sistema
- [x] Definición de 4 microservicios con responsabilidades claras
- [x] 10 user stories priorizadas en backlog
- [x] 9 ideas para futuras features
- [x] 3 ADRs fundamentales (GCP, Spotify API, Real-time Sync)
- [x] Documentación de servicios
- [x] Configuración de GitHub Copilot
- [x] Estimación de costos de GCP
- [x] Estrategia de deployment y CI/CD
- [x] Consideraciones de seguridad y observabilidad

### Próximos Pasos 🔜

- [ ] Crear event catalog detallado (schemas JSON de eventos)
- [ ] Actualizar `docs/architecture/README.md` con diagramas
- [ ] Crear guías de integración (Spotify, MIDI)
- [ ] Definir contract tests entre servicios
- [ ] Crear mock de Spotify API para desarrollo local
- [ ] Setup de proyecto GCP y credenciales
- [ ] Registrar aplicación en Spotify Developer Dashboard
- [ ] Implementar Sprint 1: US-001, US-002, US-003

---

## 🎯 Valor del Proyecto

### Para DJs
- ✅ Control profesional de Spotify desde equipo DJ habitual
- ✅ Sincronización perfecta entre dispositivos (<100ms)
- ✅ Integración con software DJ (Rekordbox, Serato - future)
- ✅ Workflow similar a CDJs profesionales

### Para el Negocio
- ✅ Plataforma escalable en GCP con costos predecibles
- ✅ Arquitectura event-driven permite agregar features fácilmente
- ✅ Real-time sync sin servidor custom (Firestore out-of-the-box)
- ✅ Monitoring y observabilidad completa (GCP native)

### Diferenciadores
- ✅ Única solución que integra Spotify + hardware DJ + real-time sync
- ✅ Latencia ultra-baja (<100ms) vs competencia (>500ms)
- ✅ Soporte MIDI nativo (vs solo apps móviles)
- ✅ Multi-dispositivo real-time (vs single device)

---

## 📞 Contacto y Recursos

- **Equipo de Arquitectura**: architecture-team@company.com
- **Slack**: #spotify-dj-remote
- **Documentación**: `/docs`
- **ADRs**: `/docs/adr`
- **Backlog**: `BACKLOG.md`
- **Ideas**: `IDEAS.md`

---

**Fecha de Creación**: 2025-11-14  
**Última Actualización**: 2025-11-14  
**Versión**: 1.0.0 (Planning Phase)
