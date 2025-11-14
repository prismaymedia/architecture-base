# 🔄 Flujo: Ideas → User Stories → Tasks → ClickUp

> **Propósito**: Documentar el proceso automatizado para convertir ideas en tareas ejecutables en ClickUp.

---

## 📊 Visión General del Flujo

```
┌─────────────┐      ┌──────────────┐      ┌─────────────┐      ┌──────────────┐
│  IDEAS.md   │─────▶│  BACKLOG.md  │─────▶│   TASKS     │─────▶│   ClickUp    │
│  (Captura)  │      │ (User Stories)│      │(Preliminar) │      │  (Ejecución) │
└─────────────┘      └──────────────┘      └─────────────┘      └──────────────┘
     💡                    📋                     ⚙️                    ✅
  Raw Ideas          Refined Stories      Technical Tasks        Team Execution
```

---

## 🎯 Fase 1: Captura de Ideas

### Cuándo Usar

- Cuando tengas una idea rápida (reunión, brainstorming, feedback de usuario)
- Cuando identifiques un problema o mejora
- Cuando no tengas tiempo para formalizar completamente

### Proceso

1. **Abre `IDEAS.md`**
2. **Agrega nueva entrada** en la sección de prioridad apropiada:
   ```markdown
   ### [ID-XXX] Título Descriptivo de la Idea
   
   - **Contexto**: ¿Quién necesita esto y por qué?
   - **Problema**: ¿Qué problema específico resuelve?
   - **Valor**: ¿Qué impacto tendrá? (cuantifica si es posible)
   - **Fecha**: 2025-11-14
   - **Estado**: 💭 Por refinar
   ```

3. **No te preocupes por**:
   - Formato perfecto
   - Criterios de aceptación detallados
   - Estimaciones precisas
   - Lo importante es **capturar la esencia**

### Ejemplo Real

```markdown
### [ID-007] Cache de Productos Más Vendidos

- **Contexto**: El endpoint /api/products/bestsellers se consulta 1000+ veces/min
- **Problema**: Cada request golpea la DB, causando latencia de 800ms
- **Valor**: Reducir latencia a <50ms y carga de DB en 90%
- **Fecha**: 2025-11-14
- **Estado**: 💭 Por refinar
```

---

## 🔄 Fase 2: Refinamiento a User Stories

### Cuándo Ejecutar

- **Semanalmente**: Al final de cada semana, revisa ideas acumuladas
- **Antes de Sprint Planning**: Para preparar backlog
- **Cuando tengas 5+ ideas** en estado "Por refinar"

### Comando para Copilot

```
Copilot, revisa IDEAS.md y convierte las ideas [ID-001, ID-002, ID-003] 
en historias de usuario formales usando el formato de backlog-template.md.
Priorízalas usando RICE framework.
```

### Qué Hace Copilot

1. **Analiza cada idea** y su contexto
2. **Genera historia de usuario** con formato:
   - Título: Como [rol], quiero [acción], para [beneficio]
   - Descripción detallada
   - Criterios de aceptación (4-6 criterios)
   - Story points (usando Fibonacci: 1, 2, 3, 5, 8, 13)
   - Prioridad RICE calculada

3. **Presenta preliminar** para tu revisión:
   ```markdown
   ## Historia Generada: US-011
   
   **Título**: Como administrador del sistema, quiero visualizar métricas 
   de rendimiento en tiempo real, para detectar problemas antes de que 
   afecten a usuarios
   
   **Story Points**: 8
   **Prioridad RICE**: 85 (Alta)
   - Reach: 10 (todos los admins)
   - Impact: 3 (alto impacto en operaciones)
   - Confidence: 80%
   - Effort: 3 semanas
   
   **Criterios de Aceptación**:
   - [ ] AC1: Dashboard muestra CPU, memoria, requests/sec de cada servicio
   - [ ] AC2: Métricas se actualizan cada 5 segundos sin refresh manual
   - [ ] AC3: Alertas visuales cuando métrica excede umbral (rojo >80%, amarillo >60%)
   - [ ] AC4: Histórico de últimas 24 horas con gráficos
   - [ ] AC5: Filtros por servicio y rango de tiempo
   
   ¿Aprobar para agregar a BACKLOG.md? (sí/no/modificar)
   ```

4. **Tú revisas y decides**:
   - ✅ **Aprobar**: Se agrega a `BACKLOG.md` con ID US-XXX
   - ❌ **Rechazar**: Se marca en `IDEAS.md` como descartada
   - ✏️ **Modificar**: Ajustas criterios y vuelves a revisar

5. **Actualiza IDEAS.md**:
   ```markdown
   ### [ID-007] Cache de Productos Más Vendidos
   
   - **Estado**: ✅ Convertida a US-011
   - **Fecha Conversión**: 2025-11-14
   ```

---

## ⚙️ Fase 3: Generación de Tareas Técnicas

### Cuándo Ejecutar

- **Durante Sprint Planning**: Antes de iniciar sprint
- **Bajo demanda**: Cuando una US esté lista para desarrollo

### Comando para Copilot

```
Copilot, genera tareas técnicas preliminares para el próximo sprint.
Usa las user stories con mayor prioridad de BACKLOG.md (sección High Priority).
Genera las tareas en inglés siguiendo task-template.md.
```

### Qué Hace Copilot

1. **Analiza prioridades** en `BACKLOG.md`:
   - Identifica las US en "High Priority" que están "To Do"
   - Considera story points y dependencias
   - Sugiere cuáles incluir en el sprint

2. **Descompone cada US en tareas técnicas**:
   - Una US puede generar 2-5 tareas dependiendo de complejidad
   - Ejemplo: US-001 (Creación de Pedido) → 4 tareas:
     - TASK-001: Implement Create Order API Endpoint
     - TASK-002: Implement Order Domain Model and Validation
     - TASK-003: Implement Order Repository and Database Schema
     - TASK-004: Publish OrderCreatedEvent to Message Broker

3. **Para cada tarea, genera** (usando `task-template.md`):
   - **Description**: Technical scope y contexto
   - **Functional AC**: Criterios orientados a usuario/negocio
   - **Technical AC**: Code quality, performance, security, testing
   - **Best Practices**: Checklist de arquitectura, SOLID, event-driven, resilience
   - **Recommendations**: Before/During/After implementation tips
   - **Testing Strategy**: Unit, integration, manual tests
   - **Related Resources**: Links a docs, ADRs, event specs

4. **Presenta preliminar** con resumen:
   ```markdown
   ## 📋 Tareas Preliminares - Sprint 1
   
   **User Stories Incluidas**: US-001, US-002, US-003
   **Total Story Points**: 26 puntos
   **Total Tareas Generadas**: 11 tareas
   
   ---
   
   ### US-001: Creación de Pedido Básico (13 pts) → 4 tareas
   
   #### TASK-001: Implement Create Order API Endpoint
   - **Priority**: 🔴 High
   - **Story Points**: 5
   - **Functional AC**: 6 criteria
   - **Technical AC**: 8 criteria
   - **Best Practices**: 25+ checklist items
   
   [Ver detalle completo de TASK-001]
   
   #### TASK-002: Implement Order Domain Model and Validation
   - **Priority**: 🔴 High
   - **Story Points**: 3
   ...
   
   ---
   
   ¿Quieres revisar las tareas una por una antes de exportar a ClickUp?
   ```

### Revisión Detallada

5. **Revisas cada tarea individualmente**:
   ```
   Usuario: Muéstrame TASK-001 completa
   
   Copilot: [Despliega tarea completa con todos los detalles]
   
   Usuario: Modifica TASK-001 - agrega AC para logging de errores
   
   Copilot: [Actualiza la tarea con nuevo criterio]
   
   Usuario: Aprobada. Siguiente tarea.
   ```

6. **Proceso iterativo**:
   - **Ver**: Una tarea a la vez
   - **Modificar**: Ajustar ACs, best practices, estimates
   - **Aprobar/Rechazar**: Decidir si va al sprint
   - **Siguiente**: Continuar hasta revisar todas

---

## 🚀 Fase 4: Exportación a ClickUp

### Preparación

Una vez aprobadas todas las tareas preliminares, Copilot genera:

1. **Archivo de exportación** (`sprint-X-tasks.md`):
   ```markdown
   # Sprint 1 - Tasks Export
   
   Generated: 2025-11-14
   Total Tasks: 11
   Total Story Points: 26
   
   ## TASK-001
   [Full task content in ClickUp-compatible format]
   
   ## TASK-002
   [Full task content...]
   ```

2. **Resumen para ClickUp**:
   - Lista de tareas con prioridades
   - Story points por tarea
   - Dependencies identificadas
   - Tags sugeridos (epic, service, priority)

### Opciones de Creación en ClickUp

#### Opción A: Manual (Copy-Paste)

1. Abre ClickUp y tu espacio/proyecto
2. Crea nueva tarea
3. Copia contenido de cada tarea del archivo generado
4. Pega en descripción de ClickUp
5. Configura: Priority, Story Points, Tags, Assignee
6. Repite para cada tarea

**Pros**: Control total, formato exacto  
**Contras**: Manual, lento para muchas tareas

#### Opción B: ClickUp API (Automatizado)

```bash
# Script de ejemplo (requiere API key de ClickUp)
python scripts/export-to-clickup.py --sprint 1 --file sprint-1-tasks.md
```

Copilot puede generar el script de integración si lo necesitas.

**Pros**: Rápido, automático  
**Contras**: Requiere configuración inicial de API

#### Opción C: CSV Import

1. Copilot genera CSV con columnas ClickUp
2. Importas vía ClickUp → Settings → Import/Export
3. Mapeas columnas (Title, Description, Priority, etc.)

**Pros**: Relativamente rápido  
**Contras**: Formato limitado, puede perder detalles

### Post-Creación

- **Actualiza BACKLOG.md**: Marca US como "In Progress"
- **Documenta en Sprint**: Crea entry en `docs/sprints/sprint-X.md`
- **Team Sync**: Comparte tareas en standup

---

## 🔁 Proceso Completo - Ejemplo Real

### Semana 1: Captura de Ideas

```markdown
# IDEAS.md

### [ID-008] API Rate Limiting
- **Contexto**: Sin rate limiting, un cliente malicioso puede saturar el sistema
- **Problema**: Incidentes de abuse, costos de infra elevados
- **Valor**: Proteger sistema y reducir costos en $500/mes
- **Fecha**: 2025-11-14
- **Estado**: 💭 Por refinar
```

### Semana 2: Refinamiento

```
Usuario: Copilot, refina ID-008 a user story

Copilot: [Genera US-012 con 5 ACs, 5 story points, prioridad Alta]

Usuario: Aprobada

Copilot: ✅ Agregada a BACKLOG.md como US-012
```

### Semana 3: Sprint Planning

```
Usuario: Copilot, genera tareas para sprint 2 basado en prioridades

Copilot: 
- US-012 (Rate Limiting) está en High Priority
- Generando 3 tareas técnicas:
  - TASK-012: Implement Rate Limiting Middleware
  - TASK-013: Configure Rate Limit Rules per API Key
  - TASK-014: Add Rate Limit Monitoring and Alerts

¿Revisar tareas ahora?

Usuario: Sí, muéstrame TASK-012

Copilot: [Despliega tarea completa con description, ACs, best practices]

Usuario: Agrega AC técnico sobre Redis para almacenar contadores

Copilot: ✅ Actualizado TAC5: "Use Redis for distributed rate limit counters"

Usuario: Aprobada. Siguiente.

Copilot: [Muestra TASK-013...]

Usuario: Todas aprobadas. Exporta a archivo.

Copilot: ✅ Generado sprint-2-tasks.md con 3 tareas
```

### Semana 4: Ejecución

- Equipo crea tareas en ClickUp usando `sprint-2-tasks.md`
- Desarrolladores trabajan con contexto completo
- Durante daily: Actualizan estado en ClickUp
- Al finalizar: Marcan como Done

---

## 🎯 Ventajas de Este Flujo

### Para Ti (Product Owner)

✅ **Captura rápida** - No pierdes ideas valiosas  
✅ **Refinamiento asistido** - Copilot ayuda a estructurar historias  
✅ **Revisión controlada** - Apruebas cada elemento antes de crear  
✅ **Trazabilidad** - De idea original hasta tarea en ClickUp  

### Para el Equipo

✅ **Contexto completo** - Tareas con descripción, ACs, best practices  
✅ **Consistencia** - Todas las tareas siguen mismo formato  
✅ **Guía técnica** - Recommendations y testing strategy incluidas  
✅ **Claridad** - Saben exactamente qué implementar y cómo  

### Para el Proyecto

✅ **Calidad** - Best practices y technical ACs aseguran estándares  
✅ **Velocidad** - Menos back-and-forth para clarificaciones  
✅ **Documentación** - Historial de decisiones en IDEAS.md y BACKLOG.md  
✅ **Priorización** - RICE framework para decisiones objetivas  

---

## 📝 Tips y Mejores Prácticas

### Captura de Ideas

- ✅ **Captura inmediatamente** - No confíes en la memoria
- ✅ **Sé específico** sobre el problema, no solo la solución
- ✅ **Cuantifica el valor** cuando sea posible
- ❌ **No te preocupes** por formato perfecto en esta fase

### Refinamiento

- ✅ **Revisa en batch** (5-10 ideas a la vez)
- ✅ **Prioriza con datos** (usa RICE framework)
- ✅ **Clarifica ambigüedades** antes de aprobar
- ❌ **No agregues** historias sin valor claro

### Generación de Tareas

- ✅ **Revisa una por una** - No apruebes en batch sin leer
- ✅ **Ajusta story points** si Copilot estima mal
- ✅ **Agrega contexto técnico** específico de tu sistema
- ❌ **No modifiques** best practices (son estándares del proyecto)

### ClickUp

- ✅ **Mantén sincronizado** - Si cambias en ClickUp, actualiza docs
- ✅ **Usa custom fields** para story points, epic, priority
- ✅ **Configura automation** para mover entre estados
- ❌ **No pierdas** la descripción detallada al crear tareas

---

## 🔧 Comandos Útiles para Copilot

```bash
# Refinamiento de ideas
"Copilot, convierte ID-XXX a user story formal"
"Copilot, refina todas las ideas de alta prioridad en IDEAS.md"
"Copilot, calcula RICE score para ID-008"

# Generación de tareas
"Copilot, genera tareas para US-XXX siguiendo task-template.md"
"Copilot, crea tareas para próximo sprint basado en prioridades"
"Copilot, descompone US-012 en tareas técnicas"

# Revisión iterativa
"Copilot, muéstrame TASK-XXX completa"
"Copilot, modifica TASK-015: agrega AC sobre performance"
"Copilot, estima story points para TASK-020"

# Exportación
"Copilot, genera archivo de exportación para sprint 3"
"Copilot, crea CSV para importar tareas a ClickUp"
"Copilot, resume tareas aprobadas para este sprint"
```

---

## 📊 Métricas de Éxito

Mide la efectividad del flujo:

- **Lead Time**: Tiempo de idea capturada → tarea en ClickUp
- **Conversion Rate**: % de ideas que se convierten en US
- **Task Clarity**: Preguntas/clarificaciones durante implementación (objetivo: <2 por tarea)
- **Estimation Accuracy**: Story points estimados vs reales (objetivo: ±20%)
- **Team Velocity**: Story points completados por sprint

---

## 🚦 Estados y Transiciones

```
IDEAS.md:
💭 Por Refinar → ✅ Convertida a US-XXX → 🗑️ Descartada

BACKLOG.md (User Stories):
📋 To Do → 🚧 In Progress → 👀 In Review → ✅ Done

ClickUp (Tasks):
📝 To Do → 🔨 In Progress → 🧪 In Testing → 👀 In Review → ✅ Done
```

---

## 📞 Soporte

Si tienes problemas con el flujo:

1. **Revisa este documento** - Cubre casos comunes
2. **Pregunta a Copilot** - "Copilot, ¿cómo convierto idea a user story?"
3. **Consulta templates** - `backlog-template.md`, `task-template.md`
4. **Revisa ejemplos** - `IDEAS.md`, `BACKLOG.md` tienen ejemplos reales

---

## 🔄 Flujo de Actualización

Este documento evoluciona con el proyecto. Si identificas mejoras:

1. Anota en `IDEAS.md` como mejora al proceso
2. Discute con el equipo en retrospectiva
3. Actualiza este documento
4. Comunica cambios al equipo
