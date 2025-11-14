# Guía de Kanban para el Equipo

> **Metodología**: Kanban  
> **Audiencia**: Todo el equipo de desarrollo  
> **Proyecto**: Sistema de Microservicios E-commerce

---

## Índice

1. [¿Qué es Kanban?](#qué-es-kanban)
2. [Nuestro Tablero Kanban](#nuestro-tablero-kanban)
3. [Flujo de Trabajo](#flujo-de-trabajo)
4. [Límites WIP](#límites-wip)
5. [Políticas del Equipo](#políticas-del-equipo)
6. [Ceremonias](#ceremonias)
7. [Métricas](#métricas)
8. [Mejores Prácticas](#mejores-prácticas)
9. [FAQ](#faq)

---

## ¿Qué es Kanban?

Kanban es un método ágil para gestionar el trabajo de manera visual y continua. En lugar de trabajar en sprints fijos, el trabajo fluye continuamente a través de diferentes estados.

### Principios Fundamentales

1. **Visualizar el trabajo**: Ver todo el trabajo en un tablero
2. **Limitar WIP**: No tener demasiado trabajo en progreso simultáneamente
3. **Gestionar el flujo**: Optimizar cómo fluye el trabajo
4. **Políticas explícitas**: Reglas claras para todos
5. **Feedback continuo**: Revisiones regulares
6. **Mejorar colaborativamente**: Evolucionar el proceso juntos

### Beneficios para Nuestro Equipo

- ✅ Flexibilidad para cambiar prioridades
- ✅ Deploy continuo sin esperar sprints
- ✅ Cada servicio puede avanzar a su ritmo
- ✅ Transparencia del estado del trabajo
- ✅ Identificación rápida de bloqueadores
- ✅ Reducción de context switching

---

## Nuestro Tablero Kanban

### Estructura del Tablero

```
┌─────────────┬──────────────┬──────────────┬─────────────┐
│   To Do     │ In Progress  │  In Review   │    Done     │
│             │  (WIP: 5)    │  (WIP: 3)    │             │
├─────────────┼──────────────┼──────────────┼─────────────┤
│ US-001      │ US-004       │ US-002       │ US-003      │
│ US-005      │ US-007       │              │             │
│ US-006      │              │              │             │
│ ...         │              │              │             │
└─────────────┴──────────────┴──────────────┴─────────────┘
```

### Columnas

#### 1. To Do (Backlog)
**Definición**: Historias priorizadas y listas para trabajarse

**Características**:
- Refinadas por Product Owner
- Criterios de aceptación claros
- Dependencias identificadas
- Priorizadas de arriba a abajo

**Quién la gestiona**: Product Owner

---

#### 2. In Progress (Development)
**Definición**: Historias en desarrollo activo

**Entrada** (Pull from To Do):
- Desarrollador disponible
- WIP limit no alcanzado
- Historia refinada y clara

**Actividades**:
- Diseño técnico
- Implementación
- Unit tests
- Actualización de documentación

**Salida** (Push to In Review):
- Código completado
- Tests pasando
- PR creado
- Ready for review

**WIP Limit**: Máximo 5 historias

**Quién la gestiona**: Equipo de desarrollo

---

#### 3. In Review (QA/Code Review)
**Definición**: Historias en code review o testing

**Entrada**:
- PR creado y listo
- CI/CD pipeline verde
- Self-review completado

**Actividades**:
- Code review por peers
- Testing manual/automatizado
- Validación de criterios de aceptación
- Validación por Product Owner

**Salida**:
- Al menos 2 approvals
- Todos los tests pasando
- PO aprueba funcionalidad
- Ready to merge

**WIP Limit**: Máximo 3 historias

**Quién la gestiona**: Todo el equipo (reviews), QA, Product Owner

---

#### 4. Done (Deployed)
**Definición**: Historias completadas y en producción

**Criterios para mover aquí**:
- ✅ Merged a main
- ✅ Deployed a producción
- ✅ Monitoreado 24h sin issues
- ✅ Aceptado por Product Owner
- ✅ Documentación actualizada

**Quién la gestiona**: Product Owner (mueve después de validar)

---

## Flujo de Trabajo

### Para Desarrolladores

#### Tomar Nueva Historia

**Paso 1**: Verifica capacidad
```
- ¿Tengo otra historia en progreso? → Termina primero
- ¿Se alcanzó WIP limit? → No tomes nueva historia
- ¿Hay algo en Review que puedas ayudar? → Prioriza review
```

**Paso 2**: Selecciona historia
```
- Toma la de mayor prioridad en "To Do"
- Verifica que esté refinada y clara
- Si no está clara, pregunta a PO antes de empezar
```

**Paso 3**: Mueve a "In Progress"
```
- Actualiza BACKLOG.md
- Notifica en Slack: "Tomando US-XXX"
- Auto-asígnate en sistema de tracking
```

**Paso 4**: Desarrolla
```
- Crea branch: feature/US-XXX-description
- Implementa según criterios de aceptación
- Escribe tests (>80% coverage)
- Actualiza documentación
```

#### Durante Desarrollo

**Daily**:
- Participa en standup
- Reporta progreso y bloqueadores
- Pide ayuda si la necesitas

**Si te bloqueas**:
1. Intenta resolver por 30 minutos
2. Pide ayuda a un compañero
3. Si persiste, comunica en standup
4. Considera mover a otra historia mientras se resuelve

#### Mover a Review

**Checklist antes de mover**:
- [ ] Código completado según criterios
- [ ] Unit tests escritos y pasando
- [ ] Integration tests (si aplica)
- [ ] Self-review del código
- [ ] PR creado con descripción clara
- [ ] CI/CD pipeline verde
- [ ] Documentación actualizada
- [ ] Eventos documentados (si aplica)

**Crear PR**:
```markdown
## US-XXX: [Título de la Historia]

### Descripción
Breve descripción de lo implementado

### Criterios de Aceptación
- [x] Criterio 1
- [x] Criterio 2
- [ ] Criterio 3 (pendiente validación PO)

### Cambios Técnicos
- Implementado OrderCreatedEvent
- Agregado handler en Inventory API
- Actualizado schema de base de datos

### Testing
- Unit tests: 85% coverage
- Integration tests: 3 nuevos tests
- Manual testing: ✅

### Documentación
- Actualizado catálogo de eventos
- Actualizado .copilot-context.md

### Screenshots (si aplica)
[Agregar screenshots]

### Checklist
- [x] Tests pasando
- [x] Self-review completado
- [x] Documentación actualizada
- [x] No hay secrets hardcoded
```

**Mover tarjeta**:
1. Actualiza `BACKLOG.md` → Mueve historia a "In Review"
2. Notifica en Slack: "US-XXX lista para review"
3. Tag reviewers en el PR

---

### Para Code Reviewers

#### Hacer Code Review

**Prioridad**: Reviews tienen prioridad sobre nuevo trabajo

**Timeframe**: Responde reviews en < 4 horas

**Checklist de Review**:
- [ ] Código sigue coding standards
- [ ] Lógica es clara y mantenible
- [ ] Tests son adecuados
- [ ] Sin vulnerabilidades de seguridad
- [ ] Sin secrets hardcoded
- [ ] Performance considerado
- [ ] Documentación actualizada
- [ ] Eventos correctamente implementados

**Tipos de comentarios**:
- **🔴 Blocker**: Debe cambiar antes de merge
- **🟡 Suggestion**: Considera cambiar, pero no blocker
- **💡 Nit**: Comentario menor (estilo, typo)
- **👍 Praise**: Algo bien hecho

**Aprobar o Rechazar**:
```
✅ Aprobar si:
- Cumple todos los criterios
- Cambios menores pueden hacerse después

❌ Request Changes si:
- Hay issues críticos de seguridad/funcionalidad
- No cumple criterios de aceptación
- Tests insuficientes
```

**Después de Review**:
- Si aprobaste: Comentar que está listo para merge
- Si rechazaste: Explicar específicamente qué cambiar
- Estar disponible para segunda ronda de review

---

### Para Product Owner

#### Validar Historia

**Timeframe**: < 24 horas después de que entra a Review

**Proceso**:
1. Revisar PR description
2. Testear funcionalidad en staging
3. Validar cada criterio de aceptación
4. Verificar que cumple Definition of Done

**Si aprueba**:
```
1. Aprobar PR (si tienes permisos)
2. Comentar: "Aprobado por PO, listo para merge"
3. Después de merge y deploy, mover a "Done"
```

**Si rechaza**:
```
1. Listar específicamente qué falta
2. Mover de vuelta a "In Progress"
3. Explicar razón al equipo
```

---

## Límites WIP

### ¿Por Qué Limitar WIP?

**Problemas de demasiado WIP**:
- ❌ Context switching constante
- ❌ Nada se termina rápido
- ❌ Más bugs
- ❌ Menor calidad
- ❌ Lead time más largo

**Beneficios de limitar WIP**:
- ✅ Enfoque en terminar trabajo
- ✅ Flujo más rápido
- ✅ Menos context switching
- ✅ Mayor calidad
- ✅ Identificar bloqueadores más fácil

### Nuestros Límites

| Columna | Límite | Razón |
|---------|--------|-------|
| To Do | Sin límite | Backlog puede crecer |
| In Progress | 5 | Max 5 desarrolladores trabajando simultáneamente |
| In Review | 3 | Reviews deben ser rápidas |
| Done | Sin límite | Archive ocasionalmente |

### ¿Qué Hacer Cuando se Alcanza el Límite?

**Si "In Progress" está lleno**:
1. ❌ NO tomes nueva historia
2. ✅ Ayuda a terminar historias existentes
3. ✅ Haz code reviews de historias en "In Review"
4. ✅ Trabaja en deuda técnica pequeña
5. ✅ Mejora tests o documentación

**Si "In Review" está lleno**:
1. ❌ NO muevas más historias a review
2. ✅ Prioriza hacer reviews
3. ✅ Contacta a PO para que valide
4. ✅ Investiga por qué reviews están lentas

---

## Políticas del Equipo

### Pull System

Kanban es un **pull system**: los desarrolladores "jalan" trabajo cuando tienen capacidad.

❌ **No Push**:
- Nadie te asigna trabajo
- No se "empuja" trabajo al equipo

✅ **Sí Pull**:
- Tomas historia cuando terminas la anterior
- Basado en prioridad del backlog
- Respetando WIP limits

### Definition of Ready (DoR)

Una historia está "lista" para entrar a "In Progress" si:

- [ ] Tiene formato de historia de usuario
- [ ] Criterios de aceptación están claros
- [ ] Dependencias identificadas
- [ ] Estimación completada (si se estima)
- [ ] Aceptada por equipo en refinement

### Definition of Done (DoD)

Una historia está "Done" cuando:

1. ✅ Código implementado y committeado
2. ✅ Tests escritos y pasando (>80% coverage)
3. ✅ Code review aprobado (mínimo 2 personas)
4. ✅ Documentación actualizada
5. ✅ Eventos documentados (si aplica)
6. ✅ Desplegado en staging
7. ✅ Probado por QA
8. ✅ Aceptado por Product Owner
9. ✅ Desplegado en producción
10. ✅ Monitoreado 24h sin incidentes

### Bloqueadores

**Definición**: Cualquier cosa que impide el progreso de una historia

**Cómo identificar**:
- Historia en "In Progress" por > 3 días sin avanzar
- Esperando decisión externa
- Dependencia técnica no resuelta
- Ambiente de desarrollo caído

**Proceso**:
1. Identificar y comunicar en standup
2. Marcar visualmente en tablero (🚫)
3. Escalar si no se resuelve en 24h
4. Product Owner prioriza resolución
5. Equipo ayuda a resolver

### Prioridades

Siempre en este orden:

1. **🔥 Incidentes de producción**: Prioridad absoluta
2. **🚫 Bloqueadores**: Desbloquear a otros
3. **👀 Reviews**: Mantener el flujo
4. **⏰ Historias casi terminadas**: Terminar antes de empezar nuevas
5. **🆕 Nuevas historias**: Solo después de lo anterior

---

## Ceremonias

### Daily Standup

**Cuándo**: Todos los días 9:30 AM  
**Duración**: 15 minutos máximo  
**Formato**: Enfocado en el tablero, no en personas

**Estructura**:
```
1. Revisar "In Review" (derecha a izquierda)
   - ¿Qué necesita aprobación?
   - ¿Hay bloqueadores?

2. Revisar "In Progress"
   - ¿Algo está stuck?
   - ¿Alguien necesita ayuda?
   - ¿Qué se va a mover a review hoy?

3. Revisar "To Do"
   - ¿Quién va a tomar siguiente historia?
   - ¿Algo no está claro?

4. Verificar WIP limits
   - ¿Estamos dentro de límites?
```

**NO es para**:
- ❌ Reportes detallados de lo que hiciste ayer
- ❌ Resolver problemas técnicos (hacerlo después)
- ❌ Discutir implementación

**SÍ es para**:
- ✅ Identificar bloqueadores
- ✅ Coordinar el trabajo del día
- ✅ Pedir ayuda
- ✅ Mantener flujo

### Backlog Refinement

**Cuándo**: Lunes 10:00 AM  
**Duración**: 1 hora  
**Participantes**: PO, Tech Lead, algunos desarrolladores (rotativo)

**Objetivo**: Preparar historias para ser trabajadas

**Actividades**:
1. Revisar top 10 historias del backlog
2. Aclarar criterios de aceptación
3. Identificar dependencias técnicas
4. Dividir historias grandes
5. Estimar (si el equipo lo hace)
6. Mover historias refinadas a "Ready"

### Delivery Review

**Cuándo**: Viernes 3:00 PM  
**Duración**: 1 hora  
**Participantes**: Equipo + stakeholders opcionales

**Objetivo**: Demo y validación del trabajo completado

**Estructura**:
1. Demo de historias completadas esta semana
2. Q&A con stakeholders
3. Feedback
4. Product Owner aprueba para producción

### Retrospectiva

**Cuándo**: Último viernes del mes  
**Duración**: 1.5 horas  
**Participantes**: Todo el equipo

**Objetivo**: Mejorar continuamente el proceso

**Formato**:
```
1. Set the Stage (5 min)
   - Check-in, crear ambiente seguro

2. Gather Data (20 min)
   - ¿Qué pasó este mes?
   - Revisar métricas

3. Generate Insights (30 min)
   - ¿Qué fue bien? 
   - ¿Qué puede mejorar?

4. Decide What to Do (30 min)
   - 3 acciones concretas para próximo mes
   - Asignar owners

5. Close (5 min)
   - Resumen y agradecimientos
```

---

## Métricas

### Lead Time

**Definición**: Tiempo total desde creación hasta done

**Fórmula**: `Fecha Done - Fecha Creación`

**Meta**: < 10 días para historias de 5 puntos

**Cómo mejorar**:
- Reducir tamaño de historias
- Eliminar bloqueadores rápido
- Mejorar refinement

### Cycle Time

**Definición**: Tiempo desde que se empieza a trabajar hasta done

**Fórmula**: `Fecha Done - Fecha "In Progress"`

**Meta**: < 5 días para historias de 5 puntos

**Cómo mejorar**:
- Mejorar claridad de historias
- Reducir interrupciones
- Hacer reviews más rápido

### Throughput

**Definición**: Historias completadas por semana

**Meta**: 3-5 historias/semana

**Cómo mejorar**:
- Mantener historias pequeñas
- Reducir WIP
- Eliminar bloqueadores

### WIP

**Definición**: Historias en progreso ahora mismo

**Meta**: Dentro de límites (5 en Progress, 3 en Review)

**Cómo mejorar**:
- Respetar límites
- Terminar antes de empezar
- Priorizar reviews

---

## Mejores Prácticas

### Para Todo el Equipo

1. **Visualiza el trabajo**
   - Mantén BACKLOG.md actualizado
   - Mueve cards cuando cambien de estado
   - Marca bloqueadores visualmente

2. **Respeta WIP limits**
   - No los veas como sugerencias
   - Son límites duros
   - Ayuda a otros a terminar

3. **Prioriza terminar sobre empezar**
   - Finish-to-start mindset
   - Reviews antes que nuevo trabajo
   - Ayudar a desbloquear otros

4. **Comunica proactivamente**
   - No esperes al standup para reportar bloqueadores
   - Pide ayuda temprano
   - Comparte conocimiento

5. **Mejora continuamente**
   - Experimenta con el proceso
   - Propón cambios en retros
   - Mide el impacto

### Para Desarrolladores

1. **Pull, no push**
   - Toma trabajo cuando tienes capacidad
   - No acumules múltiples historias
   - Una cosa a la vez, hazla bien

2. **Escribe tests**
   - Tests son parte del DoD
   - >80% coverage mínimo
   - Tests de integración para eventos

3. **Documenta mientras trabajas**
   - No dejes documentación para el final
   - Actualiza .copilot-context.md
   - Documenta eventos en catálogo

4. **Haz self-review**
   - Revisa tu propio código antes de PR
   - Verifica que cumple standards
   - Limpia código comentado

### Para Reviewers

1. **Revisa rápido**
   - < 4 horas para primera respuesta
   - Reviews tienen prioridad
   - No dejes PRs esperando

2. **Sé constructivo**
   - Explica el "por qué" de tus comentarios
   - Sugiere soluciones
   - Reconoce lo bien hecho

3. **Sé específico**
   - No solo "esto está mal"
   - Explica qué y cómo mejorar
   - Da ejemplos si ayuda

---

## FAQ

### ¿Puedo trabajar en múltiples historias simultáneamente?

**R**: No recomendado. Enfócate en terminar una antes de empezar otra. Context switching reduce productividad.

**Excepción**: Si estás completamente bloqueado y no puede resolverse rápido.

---

### ¿Qué hago si el WIP limit está alcanzado y terminé mi trabajo?

**R**: 
1. Ayuda con code reviews
2. Ayuda a desbloquear a otros
3. Trabaja en deuda técnica pequeña
4. Mejora documentación o tests
5. Aprende algo nuevo

NO tomes nueva historia hasta que haya espacio.

---

### ¿Cómo manejar bugs urgentes?

**R**: 
- Bug crítico de producción → Se trata como historia P0, bypass de WIP limit
- Bug menor → Crear historia y priorizar en backlog normal

---

### ¿Puedo saltarme historias del backlog para tomar una más interesante?

**R**: No. Toma siempre la de mayor prioridad. Si crees que la priorización está mal, discútelo con Product Owner.

---

### ¿Qué pasa si una historia toma mucho más tiempo de lo estimado?

**R**:
1. Comunica en standup
2. Pide ayuda al equipo
3. Considera dividir la historia
4. Aprende para próximas estimaciones

---

### ¿Puedo mover una historia de "In Review" de vuelta a "In Progress"?

**R**: Sí, si el review identifica cambios significativos necesarios. Pero idealmente, cambios menores se hacen sin mover la card.

---

### ¿Cómo saber si una historia está bien refinada?

**R**: Si después de leerla puedes empezar a trabajar sin hacer preguntas, está bien refinada. Si tienes dudas, pide refinement.

---

## Recursos

- [BACKLOG.md](../../BACKLOG.md) - Nuestro backlog actual
- [Product Owner Guide](product-owner-guide.md) - Para entender rol de PO
- [Plantilla de Historia](../backlog-template.md) - Para crear historias
- [Coding Standards](coding-standards.md) - Estándares de código

---

## Glosario

- **WIP**: Work In Progress - Trabajo en progreso
- **Lead Time**: Tiempo total de una historia desde creación hasta done
- **Cycle Time**: Tiempo desde que se empieza a trabajar hasta done
- **Throughput**: Cantidad de trabajo completado en un período
- **Blocker**: Algo que impide el progreso
- **DoR**: Definition of Ready - Cuándo una historia está lista para trabajarse
- **DoD**: Definition of Done - Cuándo una historia está completada
- **Epic**: Grupo de historias relacionadas con objetivo común
- **Story Points**: Unidad de estimación de esfuerzo relativo

---

**Versión**: 1.0  
**Última actualización**: 2025-11-14  
**Mantiene**: Equipo completo
