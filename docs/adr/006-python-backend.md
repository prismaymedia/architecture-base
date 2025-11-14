# Decisión Arquitectónica 006: Python para Backend de Microservicios

**Estado**: Aceptado  
**Fecha**: 2025-11-14  
**Decisores**: Equipo de Arquitectura  
**Reemplaza**: Decisión previa de usar .NET con IIS

## Contexto

Necesitamos seleccionar una tecnología backend para implementar nuestros microservicios (Orders, Inventory, Payments, Notifications). Los requisitos incluyen:
- Soporte robusto para APIs REST
- Facilidad de desarrollo y mantenimiento
- Buena integración con message brokers
- Performance adecuado para nuestro caso de uso
- Ecosistema maduro con librerías para eventos, validación, ORM, etc.

## Decisión

Implementaremos los microservicios backend utilizando **Python 3.12+** con **FastAPI** como framework principal para las APIs REST.

## Justificación

### Python

#### Ventajas
1. **Productividad**: Sintaxis clara y concisa, desarrollo rápido
2. **Ecosistema Rico**: Amplia variedad de librerías para cualquier necesidad
3. **Type Hints**: Soporte moderno de tipos con Python 3.10+
4. **Comunidad**: Gran comunidad y abundante documentación
5. **Versatilidad**: Excelente para APIs, data processing, ML/AI
6. **Developer Experience**: Fácil de aprender y mantener
7. **Async Support**: Soporte nativo para operaciones asíncronas (asyncio)

#### Desventajas
1. **Performance**: Menor performance raw que lenguajes compilados
2. **GIL**: Global Interpreter Lock limita concurrencia con threads
3. **Deployment**: Requiere runtime Python en el servidor
4. **Type Safety**: Tipos opcionales, no enforced en runtime

### FastAPI

#### Ventajas
1. **Performance**: Uno de los frameworks Python más rápidos (comparable a Node.js)
2. **Modern Python**: Aprovecha async/await y type hints
3. **Auto Documentation**: OpenAPI/Swagger automático
4. **Data Validation**: Pydantic integrado para validación de datos
5. **Type Safety**: Validación basada en tipos en development time
6. **Dependency Injection**: Sistema robusto de DI
7. **Standards-Based**: Basado en OpenAPI y JSON Schema

#### Desventajas
1. **Relativamente Nuevo**: Menos maduro que Django o Flask
2. **Async Required**: Requiere entender async/await
3. **Menos Plugins**: Ecosistema de plugins menor que Django

## Alternativas Consideradas

### 1. .NET (ASP.NET Core)
- **Rechazado**: Aunque excelente, requiere mayor overhead de infraestructura
- Menor velocidad de desarrollo
- Ecosistema más limitado para data science/ML (futuro)

### 2. Node.js (Express/NestJS)
- **Considerado Seriamente**: Excelente performance y ecosistema
- **Rechazado**: Python ofrece mejor experiencia para nuestro equipo
- Type safety menos natural que con Python type hints

### 3. Go
- **Rechazado**: Mejor performance pero mayor curva de aprendizaje
- Menos flexible para rapid development
- Ecosistema más limitado

### 4. Java (Spring Boot)
- **Rechazado**: Excesivo boilerplate
- Mayor overhead de memoria
- Desarrollo más lento

### 5. Django REST Framework
- **Rechazado**: Framework más pesado y opinionado
- Menor performance que FastAPI
- Incluye mucho que no necesitamos (ORM, admin, templates)

## Stack Tecnológico del Backend

### Core Framework
- **Python**: ^3.12 (latest stable)
- **FastAPI**: ^0.115.0
- **Uvicorn**: ASGI server para producción
- **Pydantic**: ^2.9.0 (validación de datos)

### Database & ORM
- **SQLAlchemy**: ^2.0 (ORM)
- **Alembic**: Migraciones de base de datos
- **asyncpg**: Driver PostgreSQL asíncrono
- **PostgreSQL**: Base de datos principal (database per service)

### Message Broker
- **Pika**: Cliente RabbitMQ
- **aio-pika**: Cliente RabbitMQ asíncrono
- **Celery**: Para tareas asíncronas (opcional)

### Validation & Serialization
- **Pydantic**: Validación de schemas
- **python-dotenv**: Gestión de variables de entorno

### Testing
- **pytest**: Framework de testing
- **pytest-asyncio**: Testing de código async
- **httpx**: Cliente HTTP para testing
- **pytest-cov**: Code coverage
- **factory-boy**: Test fixtures

### API & Documentation
- **FastAPI**: Auto-genera OpenAPI/Swagger
- **OpenAPI**: Especificación de API

### Monitoring & Logging
- **structlog**: Logging estructurado
- **prometheus-client**: Métricas
- **OpenTelemetry**: Distributed tracing

### Development Tools
- **black**: Code formatting
- **ruff**: Linting (reemplazo moderno de flake8)
- **mypy**: Type checking
- **pre-commit**: Git hooks para calidad

## Arquitectura del Backend

### Estructura de Proyecto por Microservicio

```
services/
├── orders-api/
│   ├── app/
│   │   ├── api/                    # API endpoints
│   │   │   ├── v1/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── orders.py       # Orders endpoints
│   │   │   │   └── health.py       # Health check
│   │   │   └── deps.py             # Dependencies (DI)
│   │   ├── core/                   # Core configuration
│   │   │   ├── __init__.py
│   │   │   ├── config.py           # Settings con Pydantic
│   │   │   ├── security.py         # Auth & security
│   │   │   └── events.py           # Event bus setup
│   │   ├── domain/                 # Domain layer
│   │   │   ├── __init__.py
│   │   │   ├── models.py           # Domain models (Pydantic)
│   │   │   ├── entities.py         # Business entities
│   │   │   └── value_objects.py    # Value objects
│   │   ├── application/            # Application layer
│   │   │   ├── __init__.py
│   │   │   ├── commands.py         # Command handlers
│   │   │   ├── queries.py          # Query handlers
│   │   │   └── services.py         # Application services
│   │   ├── infrastructure/         # Infrastructure layer
│   │   │   ├── __init__.py
│   │   │   ├── database.py         # DB setup
│   │   │   ├── repositories.py     # Repository implementations
│   │   │   ├── messaging.py        # Message broker
│   │   │   └── cache.py            # Cache (Redis)
│   │   ├── events/                 # Event definitions
│   │   │   ├── __init__.py
│   │   │   ├── handlers.py         # Event handlers
│   │   │   ├── publishers.py       # Event publishers
│   │   │   └── schemas.py          # Event schemas
│   │   ├── schemas/                # API schemas (Pydantic)
│   │   │   ├── __init__.py
│   │   │   ├── requests.py         # Request schemas
│   │   │   └── responses.py        # Response schemas
│   │   ├── utils/                  # Utilities
│   │   │   └── __init__.py
│   │   └── main.py                 # Application entry point
│   ├── tests/
│   │   ├── unit/
│   │   ├── integration/
│   │   └── conftest.py
│   ├── alembic/                    # Database migrations
│   │   ├── versions/
│   │   └── env.py
│   ├── .env.example
│   ├── .dockerignore
│   ├── Dockerfile
│   ├── pyproject.toml              # Dependencies & config
│   ├── README.md
│   └── .copilot-context.md
```

### Capas de Arquitectura (Clean Architecture)

1. **API Layer** (`api/`): Controladores FastAPI, validación de entrada
2. **Application Layer** (`application/`): Use cases, orchestration
3. **Domain Layer** (`domain/`): Business logic, entities, value objects
4. **Infrastructure Layer** (`infrastructure/`): Database, messaging, external services

### Patrones de Diseño

1. **Repository Pattern**: Abstracción de acceso a datos
2. **Dependency Injection**: FastAPI's DI system
3. **Command/Query Separation (CQRS)**: Separar reads y writes cuando convenga
4. **Event-Driven**: Comunicación asíncrona entre servicios
5. **Saga Pattern**: Para transacciones distribuidas

## Integración con Message Broker

### RabbitMQ con Pika

```python
# infrastructure/messaging.py
import aio_pika
from typing import Callable

class EventBus:
    def __init__(self, connection_url: str):
        self.connection_url = connection_url
        self.connection = None
        self.channel = None
    
    async def connect(self):
        self.connection = await aio_pika.connect_robust(self.connection_url)
        self.channel = await self.connection.channel()
    
    async def publish(self, exchange: str, routing_key: str, message: dict):
        await self.channel.default_exchange.publish(
            aio_pika.Message(body=json.dumps(message).encode()),
            routing_key=routing_key
        )
    
    async def subscribe(self, queue: str, callback: Callable):
        queue = await self.channel.declare_queue(queue, durable=True)
        await queue.consume(callback)
```

## API Standards

### REST Endpoint Conventions

- **GET** `/api/v1/orders` - List orders
- **GET** `/api/v1/orders/{order_id}` - Get single order
- **POST** `/api/v1/orders` - Create order
- **PUT** `/api/v1/orders/{order_id}` - Update order
- **DELETE** `/api/v1/orders/{order_id}` - Delete order
- **GET** `/health` - Health check
- **GET** `/metrics` - Prometheus metrics

### Response Format

```json
{
  "success": true,
  "data": {...},
  "error": null,
  "metadata": {
    "timestamp": "2025-11-14T10:30:00Z",
    "request_id": "uuid"
  }
}
```

### Error Format

```json
{
  "success": false,
  "data": null,
  "error": {
    "code": "ORDER_NOT_FOUND",
    "message": "Order with ID 123 not found",
    "details": {}
  },
  "metadata": {...}
}
```

## Configuration Management

### Using Pydantic Settings

```python
# core/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # App
    app_name: str = "Orders API"
    debug: bool = False
    api_v1_prefix: str = "/api/v1"
    
    # Database
    database_url: str
    
    # RabbitMQ
    rabbitmq_url: str
    
    # Redis
    redis_url: str
    
    class Config:
        env_file = ".env"

settings = Settings()
```

## Testing Strategy

### Unit Tests
- Test business logic en domain layer
- Test services en application layer
- Usar mocks para dependencies

### Integration Tests
- Test endpoints de API
- Test event handlers
- Usar test database

### Contract Tests
- Validar schemas de eventos
- Validar API contracts

## Deployment

### Docker
Cada microservicio tendrá su Dockerfile:

```dockerfile
FROM python:3.12-slim

WORKDIR /app

# Install dependencies
COPY pyproject.toml ./
RUN pip install poetry && poetry install --no-dev

# Copy app
COPY app/ ./app/

# Run
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Docker Compose (Development)
Para desarrollo local con todos los servicios

## Consecuencias

### Positivas
- Desarrollo rápido y productivo
- Excelente experiencia de desarrollador
- Auto-documentación con OpenAPI/Swagger
- Type safety con Pydantic
- Performance adecuado para nuestras necesidades
- Fácil integración con message brokers
- Excelente para testing
- Futuro-proof para ML/AI features

### Negativas
- Menor performance que lenguajes compilados (mitigado con async)
- Requiere disciplina con type hints
- GIL puede ser limitante en casos extremos (mitigado con arquitectura de microservicios)
- Deployment requiere gestionar Python runtime

## Implementación

### Fase 1: Setup Base (Sprint 1)
1. Crear estructura de proyecto para cada microservicio
2. Setup de FastAPI con configuración básica
3. Implementar health checks
4. Setup de database con SQLAlchemy
5. Configurar logging estructurado

### Fase 2: Core Features (Sprint 2-3)
1. Implementar domain models
2. Implementar repositories
3. Crear endpoints básicos CRUD
4. Setup de event bus
5. Implementar event handlers

### Fase 3: Integration (Sprint 4)
1. Integrar todos los microservicios
2. Implementar sagas para flujos complejos
3. Testing end-to-end
4. Performance tuning

### Fase 4: Production Ready (Sprint 5)
1. Monitoring y observability
2. Security hardening
3. CI/CD pipeline
4. Documentation

## Notas

- Usar Python 3.12+ para mejor performance y features
- Activar strict mode en mypy
- Usar async/await para todas las operaciones I/O
- Implementar idempotency keys en event handlers
- Documentar todos los endpoints con docstrings
- Usar environment variables para toda configuración

## Referencias

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Python Type Hints](https://docs.python.org/3/library/typing.html)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Clean Architecture in Python](https://www.cosmicpython.com/)
