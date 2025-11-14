# 💡 Captura de Ideas

> **Propósito**: Archivo centralizado para capturar ideas rápidas antes de convertirlas en historias de usuario formales.

## 📝 Cómo Usar Este Archivo

1. **Anota ideas rápidamente** cuando surjan, sin preocuparte por el formato perfecto
2. **Agrega contexto mínimo** (qué problema resuelve, quién lo necesita)
3. **Marca prioridad preliminar** (🔴 Alta, 🟡 Media, 🟢 Baja, 💭 Por Definir)
4. **Periódicamente**: Copilot te ayudará a refinar estas ideas y convertirlas en historias de usuario para el BACKLOG.md

---

## 🔴 Ideas - Alta Prioridad

### [ID-001] Dashboard de Métricas en Tiempo Real

- **Contexto**: Los administradores necesitan ver el estado del sistema sin entrar a múltiples servicios
- **Problema**: Actualmente hay que revisar logs de cada microservicio individualmente
- **Valor**: Reducir tiempo de diagnóstico de incidentes de 30min a 2min
- **Fecha**: 2025-11-14
- **Estado**: 💭 Por refinar

### [ID-002] Sistema de Retry Inteligente para Eventos

- **Contexto**: Cuando un evento falla, se reintenta inmediatamente sin considerar la causa
- **Problema**: Fallos transitorios (ej: DB timeout) se manejan igual que errores permanentes
- **Valor**: Reducir falsos positivos en alertas y mejorar resiliencia
- **Fecha**: 2025-11-14
- **Estado**: 💭 Por refinar

---

## 🟡 Ideas - Media Prioridad

### [ID-003] Versionado Automático de Contratos de Eventos

- **Contexto**: Los equipos modifican eventos sin coordinación entre servicios
- **Problema**: Cambios breaking causan fallos en producción
- **Valor**: Evitar incidentes por incompatibilidad de contratos
- **Fecha**: 2025-11-14
- **Estado**: 💭 Por refinar

### [ID-004] Simulador de Carga para Testing

- **Contexto**: No sabemos cómo se comporta el sistema bajo carga real
- **Problema**: Incidentes en producción que no se detectan en QA
- **Valor**: Detectar cuellos de botella antes de producción
- **Fecha**: 2025-11-14
- **Estado**: 💭 Por refinar

---

## 🟢 Ideas - Baja Prioridad

### [ID-005] CLI para Operaciones Comunes

- **Contexto**: Operaciones repetitivas requieren múltiples comandos
- **Problema**: Curva de aprendizaje alta para nuevos desarrolladores
- **Valor**: Acelerar onboarding y reducir errores humanos
- **Fecha**: 2025-11-14
- **Estado**: 💭 Por refinar

---

## 💭 Ideas - Por Clasificar

### [ID-006] Integración con Herramienta de Monitoreo Externa

- **Contexto**: _Pendiente de definir_
- **Problema**: _Pendiente de definir_
- **Valor**: _Pendiente de definir_
- **Fecha**: 2025-11-14
- **Estado**: 💭 Por refinar

---

## 🗑️ Ideas Descartadas / Archivadas

_Ideas que se evaluaron y decidieron no continuar_

### [ID-XXX] Ejemplo de Idea Descartada

- **Razón**: Costo muy alto vs beneficio mínimo
- **Fecha Descartada**: YYYY-MM-DD

---

## 📋 Proceso de Refinamiento

Cuando tengas varias ideas acumuladas:

1. **Solicita refinamiento**: "Copilot, revisa IDEAS.md y conviértelas en historias de usuario"
2. **Copilot generará**: Historias formales con formato del `backlog-template.md`
3. **Revisas y apruebas**: Una por una antes de agregarlas al BACKLOG.md
4. **Mueves a Backlog**: Ideas aprobadas se convierten en US-XXX en BACKLOG.md
5. **Actualizas IDEAS.md**: Marca las ideas como "✅ Convertida a US-XXX"

---

## 📚 Ejemplo Completo de Conversión

### Antes del Procesamiento

```markdown
### [ID-007] Cache de Productos Más Vendidos

- **Contexto**: El endpoint /api/products/bestsellers se consulta 1000+ veces/min
- **Problema**: Cada request golpea la DB, causando latencia de 800ms
- **Valor**: Reducir latencia a <50ms y carga de DB en 90%
- **Fecha**: 2025-11-14
- **Estado**: 💭 Por refinar
```

### Después de Ejecutar `./process-ideas.sh`

**En IDEAS.md:**
```markdown
### [ID-007] Cache de Productos Más Vendidos

- **Contexto**: El endpoint /api/products/bestsellers se consulta 1000+ veces/min
- **Problema**: Cada request golpea la DB, causando latencia de 800ms
- **Valor**: Reducir latencia a <50ms y carga de DB en 90%
- **Fecha**: 2025-11-14
- **Estado**: ✅ Convertida a US-011
```

**En BACKLOG.md (agregado automáticamente):**
```markdown
#### US-011: Implementar Caché para Productos Más Vendidos
**Como** administrador del sistema
**Quiero** cachear la consulta de productos más vendidos
**Para** reducir la latencia del endpoint y la carga en la base de datos

**Criterios de Aceptación:**
- [ ] El endpoint /api/products/bestsellers responde en menos de 50ms
- [ ] La caché se actualiza automáticamente cada 5 minutos
- [ ] Se reduce la carga de la base de datos en al menos 90%
- [ ] La caché se invalida cuando se agrega o modifica un producto
- [ ] Se implementan métricas de cache hit/miss ratio
- [ ] El sistema funciona correctamente cuando la caché falla (fallback a DB)

**Estimación**: 5 Story Points
**Epic**: Performance Optimization
**Prioridad**: Alta 🔴
**Servicios Afectados**: Products API
**Dependencias**: Ninguna
**Estado**: To Do

**Notas Técnicas:**
- Implementar usando Redis como caché distribuido
- Configurar TTL de 5 minutos para la caché
- Publicar ProductCacheInvalidatedEvent cuando se modifiquen productos
- Implementar circuit breaker para fallo de Redis
```

### Resultado del Procesador Automático

```
🚀 Idea Processor Initialized

Step 1: Loading files...
✓ Found 7 ideas
✓ Found 10 existing user stories

Step 2: Parsing ideas and user stories...
📝 Ideas to process: 1

Step 3: Checking for duplicates...
Checking ID-007: Cache de Productos Más Vendidos
  ✓ Unique idea

Step 4: Generating user stories from 1 unique ideas...
Generating user story for ID-007...
  ✓ Generated US-011: Implementar Caché para Productos Más Vendidos

┌────────────────────────────────────────────────────────────────────┐
│                    ✨ Generated User Stories                       │
├────────┬──────────────────────────┬────────────┬──────┬────────────┤
│ US ID  │ Title                    │ Priority   │ SP   │ Epic       │
├────────┼──────────────────────────┼────────────┼──────┼────────────┤
│ US-011 │ Implementar Caché...     │ Alta 🔴    │ 5    │ Perf. Opt. │
└────────┴──────────────────────────┴────────────┴──────┴────────────┘

Step 5: Updating files...
✓ IDEAS.md updated
✓ BACKLOG.md updated

📊 Processing Complete!
Duplicate Ideas Found: 0
New User Stories Generated: 1
```

---

## 🎯 Tips para Capturar Buenas Ideas

- **Sé específico** sobre el problema, no solo la solución
- **Cuantifica el valor** cuando sea posible (tiempo ahorrado, errores evitados, etc.)
- **Identifica el usuario** afectado (developer, admin, end-user, etc.)
- **No te preocupes por el formato** - lo importante es capturar la esencia
- **Actualiza el estado** cuando la idea evolucione

---

## 📊 Estadísticas

- **Total Ideas Capturadas**: 6
- **Por Refinar**: 6
- **Convertidas a User Stories**: 0
- **Descartadas**: 0
- **Última Actualización**: 2025-11-14
