# ADR-008: Integración con Spotify Web API

## Estado
**Aceptado** - 2025-11-14

## Contexto

El sistema de Remote Spotify Player requiere integración profunda con Spotify para:

1. **Autenticación**: Usuarios deben autorizar acceso a su cuenta Spotify Premium
2. **Control de reproducción**: Play, pause, skip, volume, seek en dispositivos Spotify
3. **Obtención de contenido**: Buscar tracks, álbumes, artistas, playlists
4. **Estado de playback**: Obtener track actual, posición, dispositivos disponibles
5. **Gestión de colas**: Agregar/remover tracks de la cola de reproducción
6. **Metadata**: BPM, key, energy level (cuando disponible)

### Opciones Evaluadas

#### Opción 1: Spotify Web API (REST + OAuth 2.0)
**Pros:**
- API oficial y soportada por Spotify
- OAuth 2.0 PKCE flow para autenticación segura
- Scopes granulares para permisos específicos
- Web Playback SDK para playback en browser (alternativa)
- Endpoints robustos para control de reproducción
- Rate limits claros (180 requests/min por usuario)
- Documentación completa y actualizada

**Contras:**
- Requiere Spotify Premium para control de playback
- No soporta acceso directo al audio stream (DRM)
- Algunas limitaciones en metadata (BPM/key no siempre disponibles)
- Polling requerido para estado de playback (no push notifications nativas)
- Rate limits pueden ser restrictivos para high-frequency polling

#### Opción 2: Spotify Web Playback SDK (Browser-based)
**Pros:**
- Reproduce Spotify directamente en el browser
- No requiere dispositivo externo
- Mayor control sobre playback (access to audio context)

**Contras:**
- Solo funciona en browser (no en backend)
- No apto para integración con hardware DJ
- Limitado para control remoto multi-dispositivo
- DRM restrictions para análisis de audio

#### Opción 3: Third-party Spotify Libraries (spotipy, spotify-web-api-node)
**Pros:**
- Wrappers que simplifican uso de Spotify Web API
- Battle-tested en proyectos open source
- Manejo automático de rate limiting y retries

**Contras:**
- Dependen de mantenimiento de third-parties
- Mismas limitaciones que Spotify Web API subyacente

## Decisión

Utilizaremos **Spotify Web API (REST)** con **OAuth 2.0 Authorization Code Flow with PKCE** para integración, complementado con la biblioteca **spotipy** (Python) para simplificar implementación.

### Estrategia de Integración

1. **Autenticación:**
   - OAuth 2.0 Authorization Code Flow with PKCE
   - Scopes requeridos:
     - `user-read-playback-state`: Leer estado de reproducción
     - `user-modify-playback-state`: Controlar reproducción
     - `user-read-currently-playing`: Track actual
     - `user-read-recently-played`: Historial
     - `playlist-read-private`: Leer playlists privadas
     - `playlist-modify-public`: Modificar playlists públicas (opcional)
   
2. **Token Management:**
   - Almacenar tokens en GCP Secret Manager
   - Refresh token automático antes de expiración (1 hora)
   - Reintentos automáticos con backoff exponencial si refresh falla

3. **Control de Playback:**
   - Endpoints primarios:
     - `PUT /v1/me/player/play`: Iniciar reproducción
     - `PUT /v1/me/player/pause`: Pausar
     - `POST /v1/me/player/next`: Siguiente track
     - `POST /v1/me/player/previous`: Anterior track
     - `PUT /v1/me/player/volume`: Ajustar volumen
     - `PUT /v1/me/player/seek`: Seek a posición
   - Timeout: 5 segundos por request
   - Retry: Hasta 3 intentos con backoff exponencial (1s, 2s, 4s)

4. **Estado de Playback:**
   - Polling cada 1 segundo cuando hay usuario activo
   - Websocket fallback usando Cloud Firestore real-time listeners
   - Endpoint: `GET /v1/me/player`
   - Caching de estado en Cloud Firestore para distribución a múltiples clientes

5. **Rate Limiting:**
   - Implementar rate limiter local (Redis) para respetar 180 req/min/user
   - Batching de requests cuando sea posible
   - Priority queue para comandos críticos (playback control > metadata fetch)

6. **Error Handling:**
   - 401 Unauthorized → Renovar token automáticamente
   - 403 Forbidden → Usuario no tiene Premium, notificar
   - 429 Too Many Requests → Backoff exponencial, up to 60 segundos
   - 502/503 → Spotify API down, mostrar mensaje al usuario
   - Network timeout → Reintentar hasta 3 veces

### Biblioteca Spotipy

Usaremos [spotipy](https://github.com/spotipy-dev/spotipy) como wrapper:

```python
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Configuration
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope=SCOPES
))

# Example: Start playback
sp.start_playback(device_id=device_id, uris=[track_uri])
```

**Ventajas de spotipy:**
- Manejo automático de rate limiting
- Refresh token automático
- Retry logic built-in
- Typed responses (con type hints)
- Mantenida activamente (>14k stars en GitHub)

## Consecuencias

### Positivas

✅ **API oficial**: Soporte y estabilidad de Spotify  
✅ **OAuth seguro**: PKCE evita ataques de intercepción  
✅ **Scopes granulares**: Permisos mínimos necesarios  
✅ **spotipy simplifica**: Menos código boilerplate, retry logic incluido  
✅ **Escalable**: Rate limiting y caching permiten múltiples usuarios  
✅ **Documentación**: API bien documentada con ejemplos  

### Negativas

⚠️ **Premium requerido**: Solo usuarios Premium pueden usar playback control  
⚠️ **No audio stream access**: No podemos analizar audio directamente (waveform, BPM detection)  
⚠️ **Rate limits**: 180 req/min puede ser restrictivo con muchos usuarios  
⚠️ **Polling overhead**: No hay webhooks nativos para estado de playback  
⚠️ **Metadata limitada**: BPM/key no siempre disponibles  
⚠️ **Dependencia externa**: Si Spotify API cae, el sistema no funciona  

### Mitigaciones

- **Premium check**: Validar cuenta Premium en autenticación, mostrar upgrade message si no
- **Audio analysis alternativa**: Usar Spotify Audio Analysis API (`/v1/audio-analysis/{id}`) para waveform data
- **Rate limiting**: Implementar priority queue y caching agresivo
- **Efficient polling**: Websockets + Firestore para reducir polling directo a Spotify
- **Metadata enrichment**: Integrar con APIs third-party (MusicBrainz, AcousticBrainz) para BPM/key
- **Circuit breaker**: Detectar cuando Spotify API está down, mostrar status page

## Alternativas Consideradas

### Web Playback SDK
No seleccionado porque no permite control remoto multi-dispositivo ni integración con hardware DJ.

### Reverse engineering de Spotify Desktop
No seleccionado por violación de ToS de Spotify y riesgo legal.

### Integración con SoundCloud/Apple Music
Considerado como segunda fase, pero Spotify tiene mejor API y market share en DJ scene.

## Limitaciones Conocidas

1. **No offline playback**: Spotify API requiere conexión a internet
2. **No audio processing**: No podemos aplicar EQ, effects, pitch shifting
3. **No recording**: ToS de Spotify prohíbe grabar output
4. **No mixing**: No podemos hacer crossfade custom o beatmatching automático
5. **Device control**: Solo podemos controlar dispositivos donde usuario tenga sesión activa

## Referencias

- [Spotify Web API Documentation](https://developer.spotify.com/documentation/web-api)
- [Spotify OAuth 2.0 Guide](https://developer.spotify.com/documentation/general/guides/authorization/)
- [spotipy Library](https://spotipy.readthedocs.io/)
- [Spotify Rate Limits](https://developer.spotify.com/documentation/web-api/concepts/rate-limits)
- [Spotify Audio Analysis](https://developer.spotify.com/documentation/web-api/reference/get-audio-analysis)

## Roadmap Futuro

- **Phase 2**: Integrar Spotify Audio Analysis API para waveforms
- **Phase 3**: Explorar integración con SoundCloud/Apple Music como alternativas
- **Phase 4**: Investigar Spotify Partner API para features avanzadas (si calificamos)

## Notas

- Evaluación realizada: 2025-11-14
- Revisión programada: Después de implementar US-001 y US-002
- Dueño de decisión: Architecture Team + Backend Team
- Spotify Developer App registrada: [Pendiente]
