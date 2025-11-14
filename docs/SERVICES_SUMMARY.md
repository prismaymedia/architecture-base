# Resumen de Microservicios - Remote Spotify Player DJ

> **Última actualización**: 2025-11-14  
> **Proyecto**: Sistema de control remoto de Spotify para aplicaciones DJ  
> **Cloud Platform**: Google Cloud Platform (GCP)

---

## Visión General

El sistema se compone de 4 microservicios principales desplegados en **Cloud Run** (GCP), comunicándose mediante **Cloud Pub/Sub** con arquitectura event-driven.

```
┌──────────────────────┐
│  Frontend (React)    │
│  DJ Controller UI    │
└──────────┬───────────┘
           │ HTTPS/REST
           ▼
┌──────────────────────────────────────────────────────────┐
│              Cloud Endpoints / API Gateway               │
└───────┬─────────────┬──────────────┬────────────────────┘
        │             │              │
        ▼             ▼              ▼
┌──────────────┐ ┌──────────────┐ ┌────────────────────┐
│   Spotify    │ │  Playback    │ │ DJ Console Integ   │
│ Integration  │ │  Control     │ │ (MIDI/HID)         │
│     API      │ │     API      │ │       API          │
└──────┬───────┘ └──────┬───────┘ └────────┬───────────┘
       │                │                   │
       └────────┬───────┴───────┬───────────┘
                │               │
                ▼               ▼
         ┌─────────────────────────────┐
         │   Cloud Pub/Sub (Events)    │
         └─────────────┬───────────────┘
                       │
                       ▼
              ┌────────────────┐
              │  Sync Service  │
              └────────┬───────┘
                       │
                       ▼
              ┌────────────────┐
              │ Cloud Firestore│
              │ (Real-time DB) │
              └────────────────┘
```

---

## Microservicios

### 1. Spotify Integration API

**Responsabilidad**: Gateway entre el sistema y Spotify Web API

**Funciones Clave**:
- Autenticación OAuth 2.0 con Spotify
- Gestión de access/refresh tokens (almacenados en Secret Manager)
- Búsqueda de tracks, artistas, álbumes, playlists
- Obtención de metadata (BPM, key, audio features)
- Gestión de dispositivos Spotify disponibles

**Stack Tecnológico**:
- Python 3.12+ con FastAPI
- spotipy (biblioteca de Spotify Web API)
- google-cloud-secret-manager (gestión de credenciales)
- Cloud SQL PostgreSQL (tokens, usuarios, dispositivos)

**Eventos Publicados**:
- `UserAuthenticatedEvent`: Usuario autenticado con Spotify Premium
- `TokenRefreshedEvent`: Access token renovado
- `AuthenticationFailedEvent`: Error en autenticación
- `DevicesUpdatedEvent`: Lista de dispositivos actualizada

**Endpoints Principales**:
- `POST /api/auth/login`: Iniciar OAuth flow
- `GET /api/auth/callback`: Callback de OAuth
- `GET /api/devices`: Listar dispositivos Spotify
- `GET /api/search`: Buscar contenido en Spotify
- `GET /api/tracks/{id}/features`: Obtener audio features

**Referencias**:
- [ADR-008: Spotify API Integration](../adr/008-spotify-api-integration.md)
- [Context File](../../services/spotify-integration-api/.copilot-context.md)

---

### 2. Playback Control API

**Responsabilidad**: Controlar reproducción de Spotify

**Funciones Clave**:
- Ejecutar comandos de playback (play, pause, next, previous)
- Ajustar volumen (0-100%)
- Seek a posición específica en track
- Gestionar cola de reproducción (add, remove, reorder tracks)
- Obtener estado actual de playback desde Spotify

**Stack Tecnológico**:
- Python 3.12+ con FastAPI
- spotipy para comandos de playback
- Cloud Pub/Sub para eventos
- Cloud SQL PostgreSQL (historial de comandos, estado)

**Eventos Publicados**:
- `PlaybackCommandEvent`: Comando de playback ejecutado
- `PlaybackStateChangedEvent`: Estado de reproducción cambió
- `VolumeChangedEvent`: Volumen ajustado
- `TrackChangedEvent`: Track cambió (next/previous/select)
- `PlaybackErrorEvent`: Error al ejecutar comando

**Eventos Consumidos**:
- `UserAuthenticatedEvent`: Preparar control para usuario
- `MIDICommandEvent`: Comando desde controlador MIDI
- `SyncRefreshRequestedEvent`: Actualizar estado desde Spotify

**Endpoints Principales**:
- `POST /api/playback/play`: Iniciar reproducción
- `POST /api/playback/pause`: Pausar reproducción
- `POST /api/playback/next`: Siguiente track
- `POST /api/playback/previous`: Track anterior
- `PUT /api/playback/volume`: Ajustar volumen
- `PUT /api/playback/seek`: Seek a posición
- `GET /api/playback/state`: Estado actual de playback

**Reglas de Negocio**:
- Solo permitir comandos si usuario tiene sesión activa en Spotify
- Validar que dispositivo target existe y está disponible
- Reintentar comandos hasta 3 veces con backoff exponencial
- Rate limiting: Máximo 10 comandos/segundo por usuario

---

### 3. Sync Service

**Responsabilidad**: Sincronización en tiempo real del estado de playback

**Funciones Clave**:
- Mantener estado de playback en Cloud Firestore
- Distribuir updates a todos los dispositivos conectados (latencia <100ms)
- Polling periódico a Spotify API para asegurar sincronización (cada 5s)
- Gestionar offline support y conflict resolution
- Tracking de dispositivos conectados

**Stack Tecnológico**:
- Python 3.12+ con FastAPI
- google-cloud-firestore (real-time database)
- Cloud Pub/Sub para consumir eventos
- Cloud Scheduler para polling periódico

**Eventos Consumidos**:
- `PlaybackStateChangedEvent`: Actualizar Firestore
- `TrackChangedEvent`: Actualizar track actual
- `VolumeChangedEvent`: Actualizar volumen
- `UserAuthenticatedEvent`: Inicializar estado para usuario
- `DeviceConnectedEvent`: Registrar nuevo dispositivo

**Eventos Publicados**:
- `SyncStateUpdatedEvent`: Estado sincronizado actualizado
- `SyncConflictDetectedEvent`: Conflicto entre estado local y Spotify
- `DeviceDisconnectedEvent`: Dispositivo desconectado (timeout)

**Estructura de Datos en Firestore**:
```javascript
/playback/{userId}/
  - userId: string
  - lastUpdated: timestamp
  - playbackState:
      - isPlaying: boolean
      - track: { id, name, artist, album, duration, uri, artworkUrl }
      - position: number  // milliseconds
      - volume: number    // 0-100
      - device: { id, name, type }
      - queue: array
      - metadata: { bpm, key, energy }
  - connectedDevices: array
```

**Optimizaciones**:
- Throttling de updates (max 10/segundo)
- Caché local en SDK de Firestore (reduce reads)
- Batching de updates de metadata
- TTL de 1 segundo en caché

**Referencias**:
- [ADR-009: Real-time Sync with Cloud Firestore](../adr/009-realtime-sync.md)

---

### 4. DJ Console Integration API

**Responsabilidad**: Integración con hardware DJ (MIDI/HID)

**Funciones Clave**:
- Detectar controladores MIDI conectados (USB/Bluetooth)
- Mapear controles MIDI a comandos de playback
- Enviar feedback a controladores (LED, motorized faders)
- Soporte para protocolos: MIDI, HID, OSC
- Gestión de presets y configuraciones de mapeo

**Stack Tecnológico**:
- Python 3.12+ con FastAPI
- python-rtmidi (protocol MIDI)
- hidapi (protocol HID para controladores USB)
- Cloud SQL PostgreSQL (mappings, presets)

**Eventos Publicados**:
- `DeviceConnectedEvent`: Controlador MIDI detectado
- `DeviceDisconnectedEvent`: Controlador desconectado
- `MIDICommandEvent`: Comando MIDI recibido (ej: fader movido)
- `MappingUpdatedEvent`: Configuración de mapeo actualizada

**Eventos Consumidos**:
- `PlaybackStateChangedEvent`: Actualizar feedback en controlador (LEDs)
- `VolumeChangedEvent`: Actualizar posición de fader motorizado
- `TrackChangedEvent`: Actualizar display en controlador

**Mapeos Soportados**:
```python
# Ejemplo de mapeo MIDI
{
  "play_button": {"midi_channel": 1, "note": 0x10, "type": "note_on"},
  "pause_button": {"midi_channel": 1, "note": 0x11, "type": "note_on"},
  "volume_fader": {"midi_channel": 1, "cc": 0x07, "type": "control_change"},
  "crossfader": {"midi_channel": 1, "cc": 0x0F, "type": "control_change"},
  "cue_button": {"midi_channel": 1, "note": 0x20, "type": "note_on"}
}
```

**Controladores Soportados** (Planificados):
- Pioneer DDJ series
- Native Instruments Traktor Kontrol
- Novation Launchpad
- Akai APC series
- Genéricos: Cualquier MIDI controller con mapeo custom

**Endpoints Principales**:
- `GET /api/devices`: Listar controladores conectados
- `POST /api/mappings`: Crear configuración de mapeo
- `GET /api/mappings/{id}`: Obtener mapeo
- `PUT /api/mappings/{id}`: Actualizar mapeo
- `POST /api/mappings/{id}/test`: Probar mapeo

---

## Comunicación Entre Servicios

### Flujo: DJ Mueve Fader de Volumen

```
1. DJ mueve fader físico
   ↓
2. DJ Console Integration API detecta MIDI CC
   └→ Publica: MIDICommandEvent { type: "volume", value: 75 }
   
3. Playback Control API consume evento
   └→ Ejecuta: spotify.set_volume(75)
   └→ Publica: VolumeChangedEvent { volume: 75 }
   
4. Sync Service consume evento
   └→ Actualiza: Firestore /playback/{userId}/playbackState/volume = 75
   
5. Firestore notifica real-time a todos los listeners
   └→ Frontend UI actualiza slider de volumen
   └→ Otro controlador MIDI actualiza su fader (si es motorizado)
   └→ Mobile app actualiza volumen
```

### Flujo: DJ Presiona Play en Frontend

```
1. Frontend envía: POST /api/playback/play
   ↓
2. Playback Control API
   └→ Ejecuta: spotify.start_playback()
   └→ Publica: PlaybackStateChangedEvent { isPlaying: true, ... }
   
3. Sync Service consume evento
   └→ Actualiza: Firestore /playback/{userId}/playbackState/isPlaying = true
   
4. Firestore notifica real-time a listeners
   └→ Frontend muestra botón "Pause"
   └→ Controlador MIDI enciende LED de "Play"
   └→ Tablet actualiza UI
```

---

## Bases de Datos

### Cloud SQL PostgreSQL (Relacional)

Cada servicio tiene su propia instancia/base de datos:

1. **spotify_integration_db**:
   - Tables: `spotify_users`, `spotify_tokens`, `spotify_devices`
   - Purpose: Datos transaccionales de autenticación

2. **playback_control_db**:
   - Tables: `playback_commands`, `command_history`, `playback_errors`
   - Purpose: Log de comandos ejecutados

3. **dj_console_integration_db**:
   - Tables: `midi_devices`, `midi_mappings`, `mapping_presets`
   - Purpose: Configuraciones de hardware

4. **sync_service_db** (Opcional):
   - Tables: `sync_log`, `conflict_resolution_log`
   - Purpose: Auditoría de sincronización

### Cloud Firestore (NoSQL Real-time)

Compartido entre servicios (read-only para la mayoría):

- Collection: `/playback/{userId}`
- Purpose: Estado de playback en tiempo real
- Access: 
  - **Write**: Solo Sync Service
  - **Read**: Todos los servicios + Frontend

---

## Gestión de Eventos

### Cloud Pub/Sub Topics

```
spotify-dj-remote.user.authenticated
spotify-dj-remote.user.token-refreshed
spotify-dj-remote.user.authentication-failed

spotify-dj-remote.playback.command
spotify-dj-remote.playback.state-changed
spotify-dj-remote.playback.track-changed
spotify-dj-remote.playback.volume-changed
spotify-dj-remote.playback.error

spotify-dj-remote.sync.state-updated
spotify-dj-remote.sync.conflict-detected

spotify-dj-remote.device.connected
spotify-dj-remote.device.disconnected
spotify-dj-remote.device.midi-command
```

### Event Schema Versioning

Todos los eventos incluyen:
```json
{
  "eventId": "uuid",
  "eventType": "string",
  "version": "1.0",
  "timestamp": "ISO8601",
  "correlationId": "uuid",
  "userId": "string",
  "payload": { /* event-specific data */ }
}
```

---

## Observabilidad

### Cloud Monitoring (Métricas)

Por servicio:
- Request latency (p50, p95, p99)
- Error rate
- Request count
- Active connections
- Database connection pool usage

Domain-specific:
- **Spotify Integration API**: Spotify API call latency, token refresh rate
- **Playback Control API**: Playback command success rate
- **Sync Service**: Firestore write latency, sync conflict rate
- **DJ Console Integration API**: MIDI message rate, device connection count

### Cloud Logging (Logs)

Structured logging con:
- `correlationId`: Trazar request across services
- `userId`: Filtrar por usuario
- `serviceName`: Identificar servicio origen
- `logLevel`: DEBUG, INFO, WARN, ERROR
- `message`: Descripción human-readable

**Nunca** loggear:
- Access tokens o refresh tokens
- Spotify user credentials
- Sensitive user data

### Cloud Trace (Distributed Tracing)

Trace requests desde frontend hasta Spotify API:
```
Frontend → API Gateway → Playback Control API → Spotify Integration API → Spotify API
    |                                    ↓
    |                          Pub/Sub Publish
    |                                    ↓
    └──────────────────> Sync Service → Firestore
```

---

## Deployment

### Cloud Run

Cada servicio se despliega como container serverless:

```yaml
# Ejemplo: playback-control-api
service: playback-control-api
region: us-central1
platform: managed
min-instances: 0
max-instances: 100
memory: 512Mi
cpu: 1
timeout: 60s
concurrency: 80
```

### CI/CD (Cloud Build)

```
git push → Cloud Build → Build Container → Push to GCR → Deploy to Cloud Run
```

### Environment Variables

Gestionadas vía **Secret Manager**:
- `SPOTIFY_CLIENT_ID`
- `SPOTIFY_CLIENT_SECRET`
- `DATABASE_URL`
- `PUBSUB_PROJECT_ID`
- `FIRESTORE_PROJECT_ID`

---

## Referencias

- [README Principal](../README.md)
- [Architecture Overview](./architecture/README.md)
- [ADR-007: GCP Platform](./adr/007-gcp-cloud-platform.md)
- [ADR-008: Spotify API Integration](./adr/008-spotify-api-integration.md)
- [ADR-009: Real-time Sync](./adr/009-realtime-sync.md)
- [Event Catalog](./events/README.md)
