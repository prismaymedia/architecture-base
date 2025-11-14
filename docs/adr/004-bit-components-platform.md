# Decisión Arquitectónica 004: BIT como Plataforma de Componentes

**Estado**: Aceptado  
**Fecha**: 2025-11-14  
**Decisores**: Equipo de Arquitectura  

## Contexto

Necesitamos una forma de compartir código, componentes y contratos entre microservicios sin crear acoplamiento directo. El código compartido debe ser versionado, reutilizable y mantenible.

## Decisión

Utilizaremos BIT como plataforma de componentes para gestionar y compartir código común entre microservicios.

## Justificación

### Ventajas

1. **Componentes Independientes**: Cada componente es independiente y versionado
2. **Reutilización**: Compartir código sin duplicación
3. **Versionado Semántico**: Control preciso de versiones
4. **Desarrollo Aislado**: Componentes desarrollados y testeados aisladamente
5. **Descubrimiento**: Facilita descubrir componentes existentes
6. **CI/CD Integration**: Integración con pipelines de despliegue

### Desventajas

1. **Curva de Aprendizaje**: Equipo debe aprender BIT
2. **Complejidad**: Infraestructura adicional (BIT server)
3. **Dependencias**: Gestión de versiones de dependencias
4. **Overhead**: Proceso adicional para crear/publicar componentes

## Alternativas Consideradas

### 1. Shared Library (proyecto común)
- **Rechazado**: Acoplamiento temporal (todos actualizan a la vez)
- Dificulta versionado independiente
- Builds lentos

### 2. NuGet Packages
- **Considerado**: Buena opción pero menos flexible
- No facilita tanto el desarrollo aislado
- BIT ofrece mejores herramientas de desarrollo

### 3. Copy-Paste
- **Rechazado**: Duplicación, mantenimiento pesadilla
- Sin versionado
- Inconsistencias

## Consecuencias

### Positivas
- Componentes reusables entre todos los servicios
- Versionado independiente de cada componente
- Testing aislado de componentes
- Facilita extraer funcionalidad común
- Documentación centralizada de componentes

### Negativas
- Setup inicial de BIT infrastructure
- Aprendizaje de nuevas herramientas
- Proceso de publicación de componentes
- Gestión de breaking changes

## Estructura de Componentes BIT

### Componentes a Crear

```
bit-components/
├── contracts/
│   ├── events/           # Schemas de eventos
│   ├── commands/         # Schemas de comandos
│   └── dtos/            # Data Transfer Objects
├── infrastructure/
│   ├── event-bus/       # Abstracciones de mensajería
│   ├── logging/         # Configuración de logging
│   ├── health-checks/   # Health check utilities
│   └── resilience/      # Circuit breakers, retries
├── domain/
│   ├── value-objects/   # Value objects compartidos
│   └── exceptions/      # Excepciones de dominio
└── testing/
    ├── fixtures/        # Test fixtures
    └── helpers/         # Test helpers
```

### Convenciones de Nombrado

- **Scope**: `@company-name/component-name`
- **Versionado**: Semver estricto (major.minor.patch)
- **Tags**: Para categorización y búsqueda

### Componentes Prioritarios

#### 1. Event Contracts
```
@company/contracts.events.orders
@company/contracts.events.payments
@company/contracts.events.inventory
@company/contracts.events.notifications
```

Contienen:
- Schemas de eventos
- Versiones de eventos
- Documentación

#### 2. Event Bus Abstractions
```
@company/infrastructure.event-bus
```

Contiene:
- IEventPublisher interface
- IEventConsumer interface
- Implementaciones para RabbitMQ/Azure Service Bus
- Configuración

#### 3. Logging Infrastructure
```
@company/infrastructure.logging
```

Contiene:
- Configuración Serilog
- Enrichers personalizados
- Correlation ID handling

#### 4. Common DTOs
```
@company/contracts.dtos.common
```

Contiene:
- PagedResult<T>
- ApiResponse<T>
- ErrorDetails
- Validation result models

## Workflow de Desarrollo

### Crear Nuevo Componente

1. Inicializar componente BIT
2. Desarrollar y testear localmente
3. Versionar según semver
4. Publicar a BIT server
5. Consumir en microservicios

### Actualizar Componente

1. Hacer cambios en componente
2. Incrementar versión (major si breaking change)
3. Documentar cambios en CHANGELOG
4. Publicar nueva versión
5. Actualizar servicios gradualmente

### Breaking Changes

- Incrementar major version
- Mantener versión anterior por período de deprecación
- Documentar migración
- Comunicar a todos los equipos

## Versionado

### Semver Estricto

- **MAJOR**: Breaking changes
- **MINOR**: Nuevas features backwards compatible
- **PATCH**: Bug fixes

### Deprecación

- Marcar como deprecated en código
- Mantener por al menos 2 major versions
- Logging de warnings cuando se usa deprecated code

## Testing

- Unit tests requeridos para todos los componentes
- Integration tests cuando aplique
- CI pipeline para validar antes de publicar
- Contract tests para event schemas

## Documentación

Cada componente debe tener:
- README.md con descripción y ejemplos
- API documentation (JSDoc/XML comments)
- CHANGELOG.md
- Migration guides para breaking changes

## Gobernanza

### Ownership
- Cada componente tiene un owner/team responsable
- Code reviews requeridos antes de publicar
- Architecture review para nuevos componentes

### Publicación
- Solo CI/CD puede publicar a producción
- Tags para environments (dev, staging, prod)
- Approval process para cambios major

## Referencias

- [BIT Components Catalog](../guides/bit-components.md)
- [Event Contracts Guide](../events/README.md)
- [Versioning Strategy](../guides/versioning.md)
