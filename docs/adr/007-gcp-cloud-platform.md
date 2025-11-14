# ADR-007: Google Cloud Platform (GCP) como Plataforma Cloud

## Estado
**Aceptado** - 2025-11-14

## Contexto

El sistema de Remote Spotify Player para aplicaciones DJ requiere una plataforma cloud robusta, escalable y con servicios managed que permitan:

1. **Despliegue serverless** de microservicios containerizados
2. **Mensajería asíncrona** para arquitectura event-driven
3. **Base de datos managed** con alta disponibilidad
4. **Sincronización en tiempo real** para múltiples dispositivos DJ
5. **Almacenamiento seguro** de credenciales y secrets (Spotify API keys)
6. **Observabilidad completa** (logging, monitoring, tracing)
7. **Baja latencia** para control de reproducción en tiempo real
8. **Integración nativa** con servicios de Google (potencial Firebase para mobile apps)

### Opciones Evaluadas

#### Opción 1: Google Cloud Platform (GCP)
**Pros:**
- Cloud Run: Despliegue serverless de containers con auto-scaling
- Cloud Pub/Sub: Mensajería asíncrona con exactamente-una-vez delivery
- Cloud Firestore: Base de datos NoSQL con real-time sync out-of-the-box
- Cloud SQL: PostgreSQL managed con replicación automática
- Secret Manager: Gestión segura de API keys y credentials
- Excelente integración con Firebase (mobile, real-time, auth)
- Cloud Logging/Monitoring/Trace: Observabilidad nativa
- Precios competitivos con free tier generoso
- Latencias bajas en regiones globales

**Contras:**
- Menor market share que AWS (menos documentación community-driven)
- Algunos servicios más nuevos que AWS equivalentes

#### Opción 2: AWS
**Pros:**
- Mayor market share y comunidad
- Amplia documentación y casos de uso
- ECS/Fargate para containers, Lambda para serverless
- SQS/SNS para mensajería

**Contras:**
- No tiene equivalente directo a Cloud Firestore para real-time sync
- Configuración más compleja para real-time features
- Secret Manager más costoso
- Menos integración nativa para real-time use cases

#### Opción 3: Azure
**Pros:**
- Azure Functions, Container Instances
- Service Bus para mensajería
- Cosmos DB con change feed

**Contras:**
- Real-time sync no tan robusto como Firestore
- Costos más elevados en varios servicios
- Menor momentum en comunidad para este tipo de aplicaciones

## Decisión

Utilizaremos **Google Cloud Platform (GCP)** como plataforma cloud principal para el proyecto.

### Servicios GCP Específicos

1. **Compute:**
   - Cloud Run: Microservices containerizados serverless
   - Cloud Functions: Para event handlers simples (opcional)

2. **Messaging:**
   - Cloud Pub/Sub: Event bus para arquitectura event-driven

3. **Databases:**
   - Cloud SQL for PostgreSQL: Database per service (transaccional)
   - Cloud Firestore: Estado de playback en tiempo real
   - Cloud Memorystore for Redis: Caché distribuido

4. **Storage:**
   - Cloud Storage: Assets, metadata, backups

5. **Security:**
   - Secret Manager: Spotify API credentials, tokens
   - Identity Platform: Autenticación de usuarios (OAuth con Spotify)

6. **Observability:**
   - Cloud Logging: Logs centralizados
   - Cloud Monitoring: Métricas y dashboards
   - Cloud Trace: Distributed tracing
   - Cloud Profiler: Performance profiling (opcional)

7. **Networking:**
   - Cloud Load Balancing: Distribución de tráfico
   - Cloud CDN: Para assets estáticos (opcional)
   - Cloud Endpoints / API Gateway: API management

8. **Real-time:**
   - Cloud Firestore: Sincronización en tiempo real del estado de playback

## Consecuencias

### Positivas

✅ **Serverless y auto-scaling**: Cloud Run escala automáticamente según demanda, cero infra management  
✅ **Real-time nativo**: Firestore provee sincronización en tiempo real sin implementación custom  
✅ **Pub/Sub robusto**: Garantías de entrega exactly-once, retry automático, dead-letter queues  
✅ **Seguridad integrada**: Secret Manager para credentials, IAM granular por servicio  
✅ **Observabilidad completa**: Logging/Monitoring/Trace sin configuración adicional  
✅ **Integración Firebase**: Potencial para mobile apps DJ con Firebase Auth, FCM, etc.  
✅ **Costos predecibles**: Pay-per-use, free tier generoso para desarrollo  
✅ **Latencia baja**: Control de playback responde en <200ms con Cloud Run + Firestore  

### Negativas

⚠️ **Vendor lock-in**: Mayor acoplamiento a GCP que soluciones cloud-agnostic  
⚠️ **Curva de aprendizaje**: Equipo debe familiarizarse con servicios GCP específicos  
⚠️ **Menor comunidad**: Menos recursos y ejemplos que AWS en Stack Overflow  
⚠️ **Dependencia de Firestore**: Real-time sync depende de servicio propietario de Google  

### Mitigaciones

- **Abstracción de servicios**: Crear interfaces para Pub/Sub, Storage, etc. (facilita migración futura)
- **Documentación interna**: Crear guías y best practices específicas para GCP
- **Multi-region**: Desplegar en múltiples regiones para alta disponibilidad
- **Monitoring**: Alertas proactivas para cuotas y límites de GCP

## Alternativas Consideradas

### Solución Multi-cloud
No seleccionada porque aumenta complejidad operacional y no aporta valor significativo para el MVP.

### Solución On-premise
No seleccionada porque requiere inversión en infraestructura, mantenimiento y no escala dinámicamente.

## Referencias

- [Cloud Run Documentation](https://cloud.google.com/run/docs)
- [Cloud Pub/Sub Best Practices](https://cloud.google.com/pubsub/docs/best-practices)
- [Cloud Firestore Real-time Updates](https://cloud.google.com/firestore/docs/query-data/listen)
- [GCP Architecture Center](https://cloud.google.com/architecture)
- [Event-driven Architecture on GCP](https://cloud.google.com/architecture/event-driven-architectures)

## Notas

- Evaluación realizada: 2025-11-14
- Revisión programada: Después de 6 meses de operación en producción
- Dueño de decisión: Architecture Team
