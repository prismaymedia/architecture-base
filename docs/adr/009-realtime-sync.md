# ADR-009: Sincronización en Tiempo Real con Cloud Firestore

## Estado
**Aceptado** - 2025-11-14

## Contexto

El sistema de Remote Spotify Player requiere sincronización de estado de playback en tiempo real entre múltiples dispositivos:

1. **Múltiples clientes**: DJ puede tener laptop, tablet, phone, consola MIDI conectados simultáneamente
2. **Baja latencia**: Cambios deben reflejarse en <100ms en todos los dispositivos
3. **Consistencia**: Todos los clientes deben ver el mismo estado (track, posición, volumen, etc.)
4. **Offline resilience**: El sistema debe funcionar con conexión intermitente
5. **Escalabilidad**: Soportar múltiples DJs con múltiples dispositivos cada uno
6. **Bidireccional**: Cualquier dispositivo puede enviar comandos y recibir updates

### Opciones Evaluadas

#### Opción 1: Cloud Firestore (Real-time Database)
**Pros:**
- Real-time listeners nativos (push notifications)
- Latencia ultra-baja (<50ms típicamente)
- Offline support built-in con sync automático al reconectar
- Escalabilidad horizontal automática
- SDKs para web, mobile, backend
- Queries eficientes con índices
- Security rules granulares
- Integración perfecta con GCP

**Contras:**
- Costo por read/write (pero bajo para este caso de uso)
- Menos flexible que base de datos relacional
- Lock-in a GCP

#### Opción 2: WebSockets + Redis Pub/Sub
**Pros:**
- Control total sobre protocol
- Latencia muy baja
- Redis es fast y battle-tested
- Cloud-agnostic

**Contras:**
- Requiere implementar WebSocket server (Cloud Run no es ideal para long-lived connections)
- Manejo manual de reconnections, offline, sync
- Más código para mantener
- Escalabilidad horizontal compleja (sticky sessions o shared state)
- No hay offline support automático

#### Opción 3: Cloud Pub/Sub + Polling
**Pros:**
- Integrado con nuestra arquitectura event-driven
- Escalabilidad garantizada
- Fácil de implementar

**Contras:**
- Polling introduce latencia (mínimo 500ms-1s)
- No cumple requisito de <100ms
- Mayor costo por polling frecuente
- No hay offline support

#### Opción 4: Server-Sent Events (SSE)
**Pros:**
- Más simple que WebSockets
- Unidireccional (servidor → cliente) suficiente para state sync
- HTTP-friendly

**Contras:**
- No bidireccional nativo (requiere requests separados para comandos)
- No hay offline support automático
- Escalabilidad requiere configuración custom

## Decisión

Utilizaremos **Cloud Firestore** como solución de sincronización en tiempo real del estado de playback.

### Arquitectura de Sincronización

```
┌─────────────┐         ┌──────────────────┐         ┌─────────────┐
│   Device A  │◄────────┤  Cloud Firestore │────────►│  Device B   │
│  (Laptop)   │ realtime│   /playback/     │ realtime│  (Tablet)   │
└─────────────┘ listener│    {userId}      │ listener└─────────────┘
                        └──────────────────┘
                               ▲      │
                               │      │ write
                          read │      ▼
                        ┌──────────────────┐
                        │ Playback Control │
                        │      API         │
                        │  (Cloud Run)     │
                        └──────────────────┘
                               ▲
                               │ commands
                        ┌──────────────────┐
                        │   Spotify API    │
                        └──────────────────┘
```

### Estructura de Datos en Firestore

```javascript
// Collection: playback
// Document ID: {userId}
{
  userId: "spotify:user:123",
  lastUpdated: Timestamp,
  playbackState: {
    isPlaying: boolean,
    track: {
      id: "spotify:track:abc",
      name: "Track Name",
      artist: "Artist Name",
      album: "Album Name",
      duration: 240000,  // ms
      uri: "spotify:track:abc",
      artworkUrl: "https://..."
    },
    position: 45000,  // ms
    volume: 75,       // 0-100
    device: {
      id: "device_id",
      name: "Living Room Speaker",
      type: "Speaker"
    },
    queue: [
      { trackId: "...", uri: "..." },
      // next tracks
    ],
    metadata: {
      bpm: 128,      // if available
      key: "Am",     // if available
      energy: 0.85   // 0-1
    }
  },
  connectedDevices: [
    {
      deviceId: "laptop_123",
      lastSeen: Timestamp,
      type: "web"
    },
    {
      deviceId: "tablet_456",
      lastSeen: Timestamp,
      type: "web"
    }
  ]
}
```

### Flujo de Actualización

1. **Usuario envía comando** (ej: play track):
   ```
   Device A → Playback Control API → Spotify API → Success
   ```

2. **API actualiza Firestore**:
   ```
   Playback Control API → Firestore.update(/playback/{userId})
   ```

3. **Firestore notifica a todos los listeners**:
   ```
   Firestore → Device A (realtime update)
            → Device B (realtime update)
            → Device C (realtime update)
   ```

4. **Devices actualizan UI**:
   ```
   Device A/B/C → Update UI with new state
   ```

**Latencia total**: 50-100ms (API call + Firestore write + push notification)

### Polling Complementario

Para asegurar sincronización con estado real de Spotify (edge cases):

```python
# Background job (Cloud Scheduler + Cloud Function)
# Ejecuta cada 5 segundos para usuarios activos

async def sync_spotify_state(user_id: str):
    # Get current state from Spotify API
    spotify_state = await spotify_api.get_playback_state(user_id)
    
    # Get cached state from Firestore
    firestore_state = await firestore.get(f'/playback/{user_id}')
    
    # If states diverge, update Firestore
    if not states_match(spotify_state, firestore_state):
        await firestore.update(f'/playback/{user_id}', spotify_state)
        # Firestore automatically notifies all listeners
```

### Offline Support

Cloud Firestore SDKs manejan offline automáticamente:

1. **Offline reads**: SDK sirve datos desde caché local
2. **Offline writes**: SDK guarda writes en queue local
3. **Reconnection**: SDK sincroniza automáticamente al reconectar
4. **Conflict resolution**: Last-write-wins (suficiente para nuestro caso)

### Security Rules

```javascript
// Firestore Security Rules
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    
    // Playback state: users can read/write their own data
    match /playback/{userId} {
      allow read: if request.auth.uid == userId;
      allow write: if request.auth.uid == userId;
    }
    
    // Connected devices: same as playback state
    match /playback/{userId}/devices/{deviceId} {
      allow read: if request.auth.uid == userId;
      allow write: if request.auth.uid == userId;
    }
  }
}
```

### Performance Optimization

1. **Índices**:
   - Index en `lastUpdated` para queries de usuarios activos
   - Index en `connectedDevices.lastSeen` para cleanup de devices obsoletos

2. **Caching**:
   - SDK caché local reduce reads
   - TTL de 1 segundo en caché (balance entre freshness y cost)

3. **Batching**:
   - Agrupar múltiples updates de metadata en un solo write
   - Throttling en cliente (max 10 updates/segundo)

## Consecuencias

### Positivas

✅ **Latencia ultra-baja**: <50ms push notifications a todos los dispositivos  
✅ **Offline support**: Funciona sin conexión, sync automático al reconectar  
✅ **Escalabilidad**: Soporta miles de usuarios concurrentes sin configuración  
✅ **Menos código**: No requiere implementar WebSocket server ni sync logic  
✅ **Real-time garantizado**: Push notifications, no polling  
✅ **Security**: Rules granulares por usuario  
✅ **Monitoring**: Integrado con Cloud Monitoring  

### Negativas

⚠️ **Costo por operación**: Cada read/write tiene costo (pero bajo: $0.06/100k reads)  
⚠️ **Lock-in a GCP**: Firestore es servicio propietario  
⚠️ **NoSQL limitations**: Queries complejas son limitadas  
⚠️ **Eventual consistency**: Aunque rápido, no es 100% consistent  

### Mitigaciones

- **Costo**: Monitoring de reads/writes, optimizar queries, usar caché
- **Lock-in**: Abstraer detrás de interfaz (facilita migración futura)
- **NoSQL**: Para queries complejas, usar Cloud SQL (datos transaccionales)
- **Consistency**: Para nuestro caso de uso (estado de playback), eventual consistency es suficiente

## Estimación de Costos

Para 1000 usuarios activos simultáneos:

- **Writes**: 10 updates/sec/user × 1000 users = 10,000 writes/sec
  - Daily: 864M writes/day × $0.18/million = **$155/day** = **$4,650/month**
  
- **Reads** (real-time listeners): ~2x writes = 20,000 reads/sec
  - Daily: 1,728M reads/day × $0.06/million = **$104/day** = **$3,120/month**

- **Storage**: 10KB/user × 1000 users = 10MB → **Negligible**

**Total estimado**: ~**$7,800/month** para 1000 usuarios activos

**Optimizaciones**:
- Throttling: Reducir updates a 1/sec → Cost reducido en 90%
- Caching: Reducir reads en 50% → Cost reducido en 50%
- **Costo optimizado**: ~**$800-1,200/month** para 1000 usuarios

## Alternativas Consideradas

### WebSockets + Redis
No seleccionado porque requiere implementación custom de offline support, reconnection logic, y escalabilidad horizontal.

### Polling con Cloud Pub/Sub
No seleccionado porque latencia de polling (>500ms) no cumple requisito de <100ms.

## Referencias

- [Cloud Firestore Documentation](https://cloud.google.com/firestore/docs)
- [Realtime Updates](https://firebase.google.com/docs/firestore/query-data/listen)
- [Offline Data](https://firebase.google.com/docs/firestore/manage-data/enable-offline)
- [Security Rules](https://firebase.google.com/docs/firestore/security/get-started)
- [Pricing](https://cloud.google.com/firestore/pricing)
- [Best Practices](https://cloud.google.com/firestore/docs/best-practices)

## Notas

- Evaluación realizada: 2025-11-14
- Revisión programada: Después de implementar US-003 (Sincronización en Tiempo Real)
- Dueño de decisión: Architecture Team + Backend Team
- Monitoring de costos: Alertas cuando reads/writes excedan budget mensual
