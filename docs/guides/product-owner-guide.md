# Manual del Product Owner - Metodología Kanban

> **Rol**: Product Owner  
> **Metodología**: Kanban  
> **Proyecto**: Sistema de Microservicios E-commerce

---

## Tabla de Contenido

1. [Introducción](#introducción)
2. [Rol del Product Owner](#rol-del-product-owner)
3. [Kanban vs Scrum](#kanban-vs-scrum)
4. [Gestión del Backlog](#gestión-del-backlog)
5. [Priorización](#priorización)
6. [Métricas y KPIs](#métricas-y-kpis)
7. [Ceremonias](#ceremonias)
8. [Workflow Diario](#workflow-diario)
9. [Herramientas](#herramientas)
10. [Mejores Prácticas](#mejores-prácticas)

---

## Introducción

Como Product Owner en un proyecto Kanban, tu rol es maximizar el valor del producto gestionando y priorizando el backlog de manera continua. A diferencia de Scrum, Kanban no trabaja en sprints fijos, sino en un flujo continuo de trabajo.

### Principios Core de Kanban

1. **Visualizar el trabajo**: Todo el trabajo es visible en el tablero
2. **Limitar el WIP** (Work In Progress): No más de X elementos en progreso
3. **Gestionar el flujo**: Optimizar el throughput
4. **Hacer políticas explícitas**: Reglas claras para todos
5. **Implementar feedback loops**: Revisiones y retrospectivas regulares
6. **Mejorar colaborativamente**: Evolución continua del proceso

---

## Rol del Product Owner

### Responsabilidades Principales

#### 1. Gestión del Backlog
- Mantener el backlog actualizado y priorizado
- Agregar nuevas historias de usuario
- Refinar y detallar historias
- Eliminar historias obsoletas
- Dividir historias grandes en más pequeñas

#### 2. Definición de Valor
- Establecer qué tiene más valor para el negocio
- Comunicar el "por qué" detrás de cada historia
- Alinear el trabajo con objetivos estratégicos
- Medir el impacto de las features

#### 3. Stakeholder Management
- Recopilar feedback de usuarios y stakeholders
- Comunicar progreso y roadmap
- Gestionar expectativas
- Resolver conflictos de prioridades

#### 4. Aceptación de Trabajo
- Validar que el trabajo cumple criterios de aceptación
- Aprobar o rechazar historias completadas
- Proporcionar feedback al equipo

#### 5. Decisiones de Producto
- Decidir qué se construye y cuándo
- Hacer trade-offs entre features
- Determinar MVP (Minimum Viable Product)

### Lo que NO es tu Responsabilidad

- ❌ Microgestionar al equipo de desarrollo
- ❌ Decidir cómo se implementa técnicamente
- ❌ Asignar tareas a desarrolladores específicos
- ❌ Cambiar prioridades constantemente sin razón

---

## Kanban vs Scrum

### Diferencias Clave

| Aspecto | Scrum | Kanban |
|---------|-------|--------|
| **Iteraciones** | Sprints fijos (2-4 semanas) | Flujo continuo |
| **Compromisos** | Sprint commitment | Ninguno (flujo) |
| **Cambios** | No durante sprint | Cualquier momento |
| **Estimación** | Obligatoria | Opcional |
| **Roles** | PO, SM, Dev Team | Flexible |
| **Métricas** | Velocity | Lead Time, Cycle Time |
| **WIP Limits** | Sprint backlog | Explícito por columna |

### Por qué Kanban para este Proyecto

✅ **Ventajas para Microservicios**:
- Diferentes servicios pueden tener diferentes tiempos de desarrollo
- Prioridades pueden cambiar basado en incidentes o necesidades del negocio
- Equipos pueden trabajar a su propio ritmo
- Deploy continuo sin esperar fin de sprint
- Mejor para soporte y mantenimiento continuo

---

## Gestión del Backlog

### Estructura del Backlog

Nuestro backlog está en: `BACKLOG.md`

#### Secciones del Backlog

1. **To Do**: Historias listas para trabajarse
2. **In Progress**: Historias en desarrollo activo
3. **In Review**: Historias en code review o QA
4. **Done**: Historias completadas y en producción

### Agregar Nueva Historia

**Paso 1**: Usa la plantilla
```bash
# Abre la plantilla
docs/backlog-template.md
```

**Paso 2**: Completa todos los campos
- Título claro y descriptivo
- Descripción en formato "Como... Quiero... Para..."
- Criterios de aceptación específicos
- Estimación (si el equipo lo requiere)
- Prioridad
- Epic al que pertenece

**Paso 3**: Asigna ID único
```
US-XXX donde XXX es el siguiente número disponible
```

**Paso 4**: Agrega al backlog
```markdown
# Copia la historia completa al BACKLOG.md
# Coloca en la sección de prioridad correcta
# Actualiza las métricas al final del documento
```

**Paso 5**: Comunica al equipo
- Slack/Teams: Nueva historia agregada
- Menciona si es urgente o puede esperar

### Refinar Historia Existente

1. Abre `BACKLOG.md`
2. Localiza la historia (US-XXX)
3. Actualiza según necesites:
   - Criterios de aceptación más claros
   - Notas técnicas adicionales
   - Cambio de prioridad
4. Actualiza fecha en "Historial de Cambios"
5. Notifica al equipo si el cambio es significativo

### Eliminar Historia

**Cuándo eliminar**:
- Feature ya no es necesaria
- Duplicada con otra historia
- Objetivos del negocio cambiaron

**Cómo eliminar**:
1. Mueve a sección "Historias Archivadas" (al final del documento)
2. Agrega razón de archivado
3. Actualiza métricas
4. Comunica al equipo

```markdown
## Historias Archivadas

### US-XXX: [Título]
**Fecha de Archivado**: 2025-11-15  
**Razón**: Ya no es prioritario para el negocio  
[Historia completa...]
```

---

## Priorización

### Framework de Priorización: RICE

Usa el método RICE para priorizar objetivamente:

**R** = Reach (Alcance): ¿Cuántos usuarios afecta?  
**I** = Impact (Impacto): ¿Cuánto valor genera?  
**C** = Confidence (Confianza): ¿Qué tan seguro estás?  
**E** = Effort (Esfuerzo): ¿Cuánto cuesta desarrollar?  

**Fórmula**: `(R × I × C) / E`

#### Ejemplo

**US-001: Creación de Pedido Básico**
- Reach: 1000 usuarios/mes = 1000
- Impact: Alta (core feature) = 3
- Confidence: 100% = 1.0
- Effort: 8 story points = 8

**Score RICE**: (1000 × 3 × 1.0) / 8 = **375**

**US-007: Dashboard de Inventario**
- Reach: 5 administradores = 5
- Impact: Media = 2
- Confidence: 80% = 0.8
- Effort: 8 story points = 8

**Score RICE**: (5 × 2 × 0.8) / 8 = **1**

➡️ US-001 tiene prioridad mucho mayor

### Niveles de Prioridad

#### 🔴 Prioridad Alta - Crítico
- **Criterio**: Blockers, core features, bugs críticos
- **Tiempo**: Trabajar inmediatamente
- **Ejemplos**: 
  - Sistema caído
  - Feature sin la cual el producto no funciona
  - Vulnerabilidad de seguridad

#### 🟡 Prioridad Media - Importante
- **Criterio**: Features importantes pero no urgentes
- **Tiempo**: Próximas 2-4 semanas
- **Ejemplos**:
  - Mejoras de UX
  - Features que agregan valor pero no son core
  - Optimizaciones

#### 🟢 Prioridad Baja - Mejoras
- **Criterio**: Nice to have, mejoras menores
- **Tiempo**: Cuando haya tiempo
- **Ejemplos**:
  - Refactorizaciones
  - Features secundarias
  - Mejoras cosméticas

### Re-priorización

**Cuándo re-priorizar**:
- Cambios en estrategia de negocio
- Feedback de usuarios
- Incidentes o bugs urgentes
- Nuevas oportunidades de mercado
- Dependencias técnicas descubiertas

**Cómo re-priorizar**:
1. Evalúa con RICE nuevamente
2. Consulta con stakeholders clave
3. Actualiza `BACKLOG.md`
4. Comunica cambios al equipo con razón

---

## Métricas y KPIs

### Métricas de Kanban

#### 1. Lead Time
**Definición**: Tiempo desde que una historia entra al backlog hasta que está en producción

**Cómo medir**:
```
Lead Time = Fecha Done - Fecha Creación
```

**Meta**: < 10 días para historias de 5 puntos

#### 2. Cycle Time
**Definición**: Tiempo desde que el equipo empieza a trabajar hasta que está done

**Cómo medir**:
```
Cycle Time = Fecha Done - Fecha "In Progress"
```

**Meta**: < 5 días para historias de 5 puntos

#### 3. Throughput
**Definición**: Número de historias completadas por semana

**Cómo medir**:
```
Throughput = Historias completadas / Semana
```

**Meta**: 3-5 historias por semana

#### 4. WIP (Work In Progress)
**Definición**: Número de historias en progreso simultáneamente

**Límites actuales**:
- In Progress: Máximo 5
- In Review: Máximo 3

**Por qué limitar**: Previene context switching y asegura que el trabajo fluya

### Dashboard de Métricas

Crea un dashboard (Excel, Notion, Jira) con:

| Semana | Throughput | Lead Time Avg | Cycle Time Avg | Bloqueadores |
|--------|-----------|---------------|----------------|--------------|
| W45    | 3         | 8 días        | 4 días         | 0            |
| W46    | 4         | 9 días        | 5 días         | 1            |
| W47    | 2         | 12 días       | 6 días         | 2            |

**Análisis**: Si lead time aumenta, investigar bloqueadores.

### Cumulative Flow Diagram (CFD)

Graficar historias por estado a lo largo del tiempo:

```
   ┃
 15┃          ████████  Done
   ┃      ████████████  
 10┃    ████████████▒▒  In Review
   ┃  ████████████▒▒▒▒
  5┃████████████▒▒░░░░  In Progress
   ┃████████░░░░░░░░░░  To Do
  0┃─────────────────
    W1  W2  W3  W4  W5
```

**Señales de problemas**:
- Crecimiento de "In Progress" → Demasiado WIP
- Estancamiento → Bloqueadores
- Espacio entre líneas crece → Cuellos de botella

---

## Ceremonias

### 1. Backlog Refinement (Semanal)

**Cuándo**: Lunes 10:00 AM  
**Duración**: 1 hora  
**Participantes**: PO, Tech Lead, 1-2 desarrolladores

**Agenda**:
1. Revisar top 10 historias del backlog
2. Aclarar criterios de aceptación
3. Identificar dependencias técnicas
4. Estimar historias (si es necesario)
5. Dividir historias grandes

**Output**: Historias refinadas y listas para desarrollo

### 2. Kanban Standup (Diario)

**Cuándo**: Todos los días 9:30 AM  
**Duración**: 15 minutos  
**Participantes**: Todo el equipo

**Formato** (enfocado en el tablero, no en personas):
1. Revisar columna "In Review" de derecha a izquierda
2. Identificar bloqueadores
3. Verificar WIP limits
4. Siguiente historia a tomar

**NO es para**:
- Reportes individuales detallados
- Solucionar problemas técnicos (hacerlo después)

### 3. Replenishment Meeting (Bi-semanal)

**Cuándo**: Cada 2 semanas  
**Duración**: 30 minutos  
**Participantes**: PO, Tech Lead

**Agenda**:
1. Revisar throughput reciente
2. Determinar cuántas historias mover a "To Do"
3. Validar prioridades
4. Ajustar WIP limits si es necesario

**Output**: Backlog "To Do" poblado para próximas 2 semanas

### 4. Delivery Review (Semanal)

**Cuándo**: Viernes 3:00 PM  
**Duración**: 1 hora  
**Participantes**: Equipo completo + stakeholders opcionales

**Agenda**:
1. Demo de historias completadas esta semana
2. Validar que cumplen criterios de aceptación
3. Feedback de stakeholders
4. Decidir deploy a producción

**Output**: Historias aprobadas para deploy

### 5. Retrospectiva (Mensual)

**Cuándo**: Último viernes del mes  
**Duración**: 1.5 horas  
**Participantes**: Equipo completo

**Formato**:
1. ¿Qué fue bien?
2. ¿Qué puede mejorar?
3. Acciones específicas para siguiente mes

**Output**: Lista de mejoras a implementar

---

## Workflow Diario

### Tu Día Como Product Owner

#### Mañana (9:00 - 12:00)

**9:00 - 9:15**: Revisar emails y mensajes
- Feedback de usuarios
- Requests de stakeholders
- Reportes de bugs

**9:30 - 9:45**: Daily Standup
- Participar en standup
- Tomar nota de bloqueadores
- Identificar si necesitas aclarar algo

**10:00 - 11:00**: Gestión de Backlog
- Revisar nuevas solicitudes
- Actualizar prioridades
- Refinar historias para próxima semana

**11:00 - 12:00**: Aceptación de Trabajo
- Revisar historias en "In Review"
- Validar que cumplen criterios
- Aprobar o pedir cambios
- Mover a "Done" si está listo

#### Tarde (14:00 - 18:00)

**14:00 - 15:00**: Stakeholder Communication
- Meetings con stakeholders
- Actualizar roadmap
- Comunicar progreso

**15:00 - 16:00**: Refinamiento
- Trabajar en detalles de próximas historias
- Buscar feedback de usuarios
- Investigar competencia

**16:00 - 17:00**: Planning & Strategy
- Revisar métricas
- Ajustar roadmap
- Preparar próximas ceremonias

**17:00 - 18:00**: Support & Ad-hoc
- Responder preguntas del equipo
- Resolver bloqueadores
- Aclarar dudas sobre historias

---

## Herramientas

### Herramientas Recomendadas

#### 1. Gestión de Backlog
- **Actual**: `BACKLOG.md` (Markdown en Git)
- **Alternativas**: Jira, Trello, Azure DevOps, Linear

**Ventajas de Markdown**:
- ✅ Versionado con Git
- ✅ Code review de cambios
- ✅ No requiere herramienta externa
- ✅ Fácil de hacer backup

**Desventajas**:
- ❌ Sin drag-and-drop visual
- ❌ Sin reporting automático
- ❌ Requiere edición manual

#### 2. Visualización de Kanban Board

Opciones para visualizar el backlog:

**GitHub Projects** (Recomendado si usas GitHub):
```
1. Crear nuevo Project en GitHub
2. Agregar columnas: To Do, In Progress, In Review, Done
3. Configurar automation (mover automático en PR)
4. Linkear issues a historias en BACKLOG.md
```

**Trello** (Simple y visual):
```
1. Crear board "Product Backlog"
2. Crear listas por prioridad y estado
3. Crear cards por historia
4. Agregar labels, due dates
```

**Jira** (Enterprise):
```
1. Crear proyecto Kanban
2. Configurar workflow
3. Importar historias
4. Configurar automation rules
```

#### 3. Métricas y Analytics

- **Excel/Google Sheets**: Para tracking manual de métricas
- **Jira/Azure DevOps**: Reportes automáticos si usas estas herramientas
- **Custom Dashboard**: Considera construir dashboard con Power BI o Grafana

---

## Mejores Prácticas

### Do's ✅

1. **Mantén el backlog limpio**
   - Máximo 20-30 historias en "To Do"
   - Archiva historias obsoletas
   - Revisa semanalmente

2. **Comunica el "Por qué"**
   - No solo "qué" construir, sino "por qué"
   - Ayuda al equipo a entender el valor
   - Permite mejores decisiones técnicas

3. **Haz las historias pequeñas**
   - Idealmente < 5 story points
   - Facilita estimación
   - Reduce risk
   - Feedback más rápido

4. **Respeta los WIP limits**
   - Si se alcanza el límite, ayuda a desbloquear
   - No agregues más trabajo
   - Enfoca en terminar lo iniciado

5. **Acepta trabajo rápidamente**
   - Revisa historias en "In Review" daily
   - No dejes al equipo esperando
   - Da feedback específico

6. **Mide y optimiza**
   - Revisa métricas semanalmente
   - Identifica tendencias
   - Experimenta con mejoras

### Don'ts ❌

1. **No cambies prioridades constantemente**
   - Desestabiliza al equipo
   - Reduce productividad
   - Solo cambia con buena razón

2. **No microgestiones**
   - Confía en el equipo
   - No decidas "cómo" implementar
   - Enfócate en "qué" y "por qué"

3. **No agregues historias sin refinar**
   - Debe estar clara antes de entrar a backlog
   - Con criterios de aceptación definidos
   - Con dependencias identificadas

4. **No ignores la deuda técnica**
   - Balancea features con mejoras técnicas
   - Escucha al equipo sobre refactorings
   - 20% del tiempo para deuda técnica

5. **No apruebes trabajo incompleto**
   - Si no cumple criterios, no es Done
   - Mantén estándares altos
   - Mejor rechazar que aceptar mediocridad

6. **No trabajes aislado**
   - Colabora con el equipo
   - Escucha feedback
   - Toma decisiones juntos cuando sea posible

---

## Escenarios Comunes

### Escenario 1: Stakeholder Pide Feature Urgente

**Situación**: Un VP pide una feature nueva "urgente"

**Pasos**:
1. Escucha y documenta la solicitud
2. Pregunta: ¿Por qué es urgente? ¿Cuál es el impacto si esperamos?
3. Evalúa con RICE score
4. Compara con historias actuales en progreso
5. Si realmente es más prioritario:
   - Crea la historia
   - Refina rápidamente con equipo
   - Mueve algo de menor prioridad de vuelta a backlog
   - Comunica el cambio y razón al equipo
6. Si no es más prioritario:
   - Explica las prioridades actuales
   - Muestra el costo de interrumpir
   - Negocia el timing

### Escenario 2: Equipo Está Bloqueado

**Situación**: Historia en "In Progress" está bloqueada esperando tu decisión

**Pasos**:
1. Responde inmediatamente (< 2 horas)
2. Si necesitas investigar:
   - Comunica que estás en ello
   - Da timeline de respuesta
3. Si es decisión de producto:
   - Toma la decisión basada en valor
   - Explica el razonamiento
4. Si es decisión técnica:
   - Confía en el equipo para decidir
5. Documenta la decisión en la historia

### Escenario 3: Historia Completada No Cumple Criterios

**Situación**: Equipo dice historia está "Done" pero faltan criterios

**Pasos**:
1. Revisa todos los criterios de aceptación
2. Lista específicamente qué falta
3. Mueve de vuelta a "In Progress"
4. Comunica con empatía pero firmeza
5. Aclara si hay confusión en criterios
6. Ajusta Definition of Done si es necesario

### Escenario 4: Demasiadas Historias en "In Review"

**Situación**: 5 historias esperando tu aprobación

**Pasos**:
1. Bloquea tiempo inmediato para revisar
2. Prioriza las más antiguas primero
3. Revisa rápidamente (30 min por historia)
4. Aprueba lo que está listo
5. Da feedback específico en lo que no
6. Considera delegar review a otro stakeholder

---

## Checklist Semanal del Product Owner

### Lunes
- [ ] Revisar métricas de la semana pasada
- [ ] Preparar agenda de backlog refinement
- [ ] Refinement meeting
- [ ] Actualizar top 10 del backlog

### Martes-Jueves
- [ ] Daily standup (cada día)
- [ ] Revisar historias en "In Review" (cada día)
- [ ] Responder preguntas del equipo (< 2 horas)
- [ ] Agregar nuevas historias si es necesario
- [ ] Reuniones con stakeholders

### Viernes
- [ ] Delivery review
- [ ] Aprobar historias para deploy
- [ ] Actualizar métricas de la semana
- [ ] Comunicar progreso a stakeholders
- [ ] Preparar prioridades para próxima semana

### Mensual
- [ ] Retrospectiva (último viernes)
- [ ] Revisar roadmap
- [ ] Analizar tendencias de métricas
- [ ] Presentación a liderazgo
- [ ] Archivar historias obsoletas

---

## Recursos Adicionales

### Libros Recomendados
- "Kanban: Successful Evolutionary Change" - David J. Anderson
- "User Story Mapping" - Jeff Patton
- "Inspired" - Marty Cagan
- "The Lean Startup" - Eric Ries

### Cursos
- Kanban University: Kanban Management Professional
- Scrum.org: Professional Scrum Product Owner (también útil para Kanban)

### Templates y Herramientas
- [BACKLOG.md](../../BACKLOG.md)
- [Historia de Usuario Template](../backlog-template.md)
- [Kanban Guide](kanban-guide.md)

---

## Contacto y Soporte

Para dudas sobre este manual:
- **Slack**: #product-management
- **Email**: product@company.com

---

**Versión**: 1.0  
**Última actualización**: 2025-11-14  
**Autor**: Equipo de Arquitectura
