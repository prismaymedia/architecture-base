# Guías de Desarrollo

Este directorio contiene guías y mejores prácticas para desarrollar en el sistema de microservicios.

## Contenido

### Patrones Arquitectónicos
- [Saga Pattern](saga-pattern.md) - Transacciones distribuidas
- [CQRS Pattern](cqrs-pattern.md) - Separación de comandos y consultas
- [Event-Driven Patterns](event-driven-patterns.md) - Patrones de comunicación por eventos

### Infraestructura
- [IIS Configuration](iis-configuration.md) - Configuración de IIS para microservicios
- [Event Bus Setup](event-bus-setup.md) - Configuración de RabbitMQ/Service Bus
- [Database Migrations](database-migrations.md) - Gestión de migraciones

### Desarrollo
- [Coding Standards](coding-standards.md) - Estándares de código .NET
- [API Design](api-design.md) - Diseño de APIs REST
- [Error Handling](error-handling.md) - Manejo de errores
- [Logging](logging.md) - Estrategia de logging estructurado

### Testing
- [Testing Strategy](testing.md) - Estrategia general de testing
- [Unit Testing](unit-testing.md) - Testing de unidades
- [Integration Testing](integration-testing.md) - Testing de integración
- [Contract Testing](contract-testing.md) - Testing de contratos de eventos

### Operaciones
- [Deployment](deployment.md) - Proceso de despliegue
- [Monitoring](monitoring.md) - Monitoreo y observabilidad
- [Troubleshooting](troubleshooting.md) - Resolución de problemas comunes

### Seguridad
- [Security Guidelines](security.md) - Guías de seguridad
- [PCI Compliance](pci-compliance.md) - Cumplimiento PCI para pagos

### BIT Components
- [BIT Components](bit-components.md) - Desarrollo con BIT
- [Versioning Strategy](versioning.md) - Estrategia de versionado

## Principios Generales

### 1. SOLID Principles

- **S**ingle Responsibility: Cada clase tiene una sola razón para cambiar
- **O**pen/Closed: Abierto para extensión, cerrado para modificación
- **L**iskov Substitution: Las subclases deben ser sustituibles por sus clases base
- **I**nterface Segregation: Interfaces específicas mejor que generales
- **D**ependency Inversion: Depender de abstracciones, no de concreciones

### 2. DRY (Don't Repeat Yourself)

- Extraer código repetido a funciones/clases
- Usar BIT components para compartir código entre servicios
- Crear utilidades comunes en shared libraries

### 3. KISS (Keep It Simple, Stupid)

- La solución más simple que funcione
- No sobre-ingeniería
- Código fácil de entender

### 4. YAGNI (You Aren't Gonna Need It)

- No implementar funcionalidad hasta que sea necesaria
- Evitar "prepararse para el futuro"
- Iterar basado en necesidades reales

## Flujo de Desarrollo

### 1. Planning
- Revisar arquitectura existente
- Documentar decisiones (ADRs si es significativo)
- Diseñar eventos si es necesario

### 2. Development
- Crear branch desde `main`
- Seguir coding standards
- Escribir tests
- Actualizar documentación

### 3. Testing
- Unit tests (mínimo 80% coverage)
- Integration tests para flujos críticos
- Contract tests para eventos

### 4. Code Review
- Al menos 2 approvals requeridos
- Verificar que sigue estándares
- Validar tests

### 5. Deployment
- CI/CD automático a dev
- Manual promotion a staging
- Approval requerido para production

## Convenciones de Código

### Naming

**C# / .NET**
- PascalCase para clases, métodos, propiedades
- camelCase para variables locales y parámetros
- Interfaces con prefijo `I` (ej: `IOrderRepository`)
- Async methods con sufijo `Async` (ej: `GetOrderAsync`)

**Archivos**
- Nombre de archivo = nombre de clase principal
- Un tipo público por archivo (excepto nested types)

**Bases de datos**
- PascalCase para tablas
- PascalCase para columnas
- Plural para tablas de entidades (ej: `Orders`, `Products`)

### Organización de Código

```csharp
// NOTA: Ejemplo conceptual de estructura
namespace Company.Service.Layer
{
    // 1. Using statements (ordenados)
    using System;
    using System.Collections.Generic;
    using Company.Shared;

    // 2. Clase con XML comments
    /// <summary>
    /// Description of the class
    /// </summary>
    public class MyClass
    {
        // 3. Fields (private)
        private readonly IService _service;

        // 4. Constructor
        public MyClass(IService service)
        {
            _service = service;
        }

        // 5. Properties
        public string Name { get; set; }

        // 6. Public methods
        public void PublicMethod()
        {
            // Implementation
        }

        // 7. Private methods
        private void PrivateMethod()
        {
            // Implementation
        }
    }
}
```

## Git Workflow

### Branches

- `main`: Producción
- `develop`: Integración
- `feature/XXX-description`: Nuevas features
- `bugfix/XXX-description`: Corrección de bugs
- `hotfix/XXX-description`: Fixes urgentes en producción

### Commits

Formato de commit messages:
```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: Nueva feature
- `fix`: Bug fix
- `docs`: Documentación
- `style`: Formato (no afecta lógica)
- `refactor`: Refactorización
- `test`: Tests
- `chore`: Mantenimiento

**Ejemplo:**
```
feat(orders): add order cancellation endpoint

Implement POST /api/orders/{id}/cancel endpoint
that allows users to cancel their pending orders.

Closes #123
```

## Herramientas Recomendadas

### IDE
- Visual Studio 2022
- Visual Studio Code con extensiones C#

### Extensions
- GitHub Copilot
- SonarLint
- .NET Core Test Explorer
- GitLens

### Análisis de Código
- SonarQube para code quality
- ReSharper / Rider para refactoring

## Recursos de Aprendizaje

### Documentación Oficial
- [ASP.NET Core Docs](https://docs.microsoft.com/en-us/aspnet/core/)
- [Entity Framework Core](https://docs.microsoft.com/en-us/ef/core/)
- [.NET Best Practices](https://docs.microsoft.com/en-us/dotnet/standard/design-guidelines/)

### Libros Recomendados
- "Domain-Driven Design" - Eric Evans
- "Building Microservices" - Sam Newman
- "Clean Code" - Robert C. Martin
- "Design Patterns" - Gang of Four

### Cursos
- Pluralsight: Microservices Architecture
- Microsoft Learn: ASP.NET Core Path

## Soporte

### Canales de Comunicación
- Slack: #architecture channel
- Teams: Desarrollo team
- Email: architecture@company.com

### Office Hours
- Martes 2-3pm: Consultas de arquitectura
- Jueves 10-11am: Code review sessions

## Checklist de Desarrollo

Antes de crear PR:

- [ ] Código sigue coding standards
- [ ] Tests escritos y pasando (>80% coverage)
- [ ] Documentación actualizada
- [ ] ADR creado si es decisión significativa
- [ ] Eventos documentados en catálogo
- [ ] Logs estructurados agregados
- [ ] Error handling implementado
- [ ] No hay secrets hardcoded
- [ ] Performance considerado
- [ ] Security review realizado

## Referencias

- [Architecture Overview](../architecture/README.md)
- [ADRs](../adr/README.md)
- [Event Catalog](../events/README.md)
