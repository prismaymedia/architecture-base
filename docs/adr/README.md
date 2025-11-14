# Architecture Decision Records (ADRs)

Este directorio contiene todas las decisiones arquitectónicas importantes del proyecto. Cada ADR documenta una decisión significativa, su contexto, alternativas consideradas y consecuencias.

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
| [003](003-iis-web-server.md) | Uso de IIS como Servidor Web | Aceptado | 2025-11-14 |
| [004](004-bit-components-platform.md) | BIT como Plataforma de Componentes | Aceptado | 2025-11-14 |

## Decisiones Fundamentales

Las decisiones 001-004 forman el núcleo de nuestra arquitectura:

1. **Event-Driven**: Comunicación asíncrona entre servicios
2. **Database per Service**: Independencia de datos
3. **IIS**: Plataforma de hosting
4. **BIT Components**: Compartir código de manera estructurada

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

- [ ] Estrategia de API Versioning
- [ ] Autenticación y Autorización (OAuth 2.0 / JWT)
- [ ] Estrategia de Testing (Unit, Integration, E2E)
- [ ] Observabilidad y Monitoring (Application Insights)
- [ ] Estrategia de Cache (Redis)
- [ ] CI/CD Pipeline Architecture
- [ ] Disaster Recovery y Backup Strategy
- [ ] Performance Testing Strategy
- [ ] Data Migration Strategy
- [ ] API Gateway Pattern

## Referencias

- [Architecture Overview](../architecture/README.md)
- [Guías de Desarrollo](../guides/README.md)
- [Catálogo de Eventos](../events/README.md)

## Recursos Externos

- [ADR GitHub Organization](https://adr.github.io/)
- [Documenting Architecture Decisions](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions)
- [ThoughtWorks ADR Tools](https://github.com/npryce/adr-tools)
