# Decisión Arquitectónica 003: Uso de IIS como Servidor Web

**Estado**: Superseded by [ADR-006](006-python-backend.md)  
**Fecha**: 2025-11-14  
**Decisores**: Equipo de Arquitectura  
**Superseded Date**: 2025-11-14

> **Nota**: Esta decisión fue reemplazada por ADR-006 (Python Backend), que utiliza Uvicorn como servidor ASGI en lugar de IIS.  

## Contexto

Necesitamos seleccionar un servidor web para hospedar nuestros microservicios ASP.NET Core. El servidor debe ser estable, escalable y bien integrado con el ecosistema Windows/Azure.

## Decisión

Utilizaremos Internet Information Services (IIS) como servidor web principal para hospedar todos nuestros microservicios ASP.NET Core.

## Justificación

### Ventajas

1. **Integración Windows**: Excelente integración con infraestructura Windows existente
2. **Madurez**: Tecnología probada con décadas de evolución
3. **Management**: Interfaz gráfica y herramientas de administración robustas
4. **Seguridad**: Features de seguridad enterprise integradas
5. **Performance**: Alto rendimiento con ASP.NET Core
6. **Certificaciones**: Cumplimiento con estándares de seguridad enterprise
7. **Familiaridad**: Equipo tiene experiencia con IIS
8. **Application Pools**: Aislamiento entre aplicaciones

### Desventajas

1. **Plataforma**: Limitado a Windows Server
2. **Complejidad**: Configuración puede ser compleja
3. **Recursos**: Consume más recursos que alternativas ligeras
4. **Licenciamiento**: Requiere licencias Windows Server

## Alternativas Consideradas

### 1. Kestrel Standalone
- **Rechazado para producción**: Aunque Kestrel es excelente, preferimos IIS para management enterprise
- Sin embargo, IIS usa Kestrel internamente con ASP.NET Core Module

### 2. Nginx
- **Rechazado**: Aunque es excelente, requeriría Linux o configuración adicional en Windows
- Menos familiar para el equipo

### 3. Docker + Kubernetes
- **Considerado para futuro**: Mantener como opción de evolución
- Actual complejidad operativa no justifica beneficios inmediatos

## Consecuencias

### Positivas
- Aprovechamos experiencia existente del equipo
- Herramientas de troubleshooting familiares
- Integración nativa con Active Directory
- Certificados y SSL management simplificado
- Application Request Routing (ARR) para load balancing

### Negativas
- Dependencia de Windows Server
- Costos de licenciamiento
- Menos portabilidad que containers

## Configuración

### Application Pools

Cada microservicio tendrá su propio Application Pool:

```
Application Pools:
├── OrdersAPI-Pool
│   ├── .NET CLR Version: No Managed Code
│   ├── Pipeline: Integrated
│   └── Identity: ApplicationPoolIdentity
├── InventoryAPI-Pool
├── PaymentsAPI-Pool
└── NotificationsAPI-Pool
```

**Beneficios**:
- Aislamiento de recursos
- Reciclaje independiente
- Configuración de memoria por servicio

### ASP.NET Core Module

- Usar ASP.NET Core Module v2
- In-Process hosting para mejor performance
- Stdout logging para debugging

### Sites Configuration

```
Sites:
├── orders.company.com → OrdersAPI
├── inventory.company.com → InventoryAPI
├── payments.company.com → PaymentsAPI
└── notifications.company.com → NotificationsAPI
```

### Health Monitoring

- Failed Request Tracing habilitado
- Application Initialization para warm-up
- Health checks configurados en IIS

### Load Balancing

- Application Request Routing (ARR) para load balancing
- Server farms con múltiples instancias
- Health checks automáticos
- Sticky sessions cuando sea necesario

## Deployment

### Pipeline CI/CD

1. Build en Azure DevOps / GitHub Actions
2. Publicar artifacts
3. Web Deploy a IIS
4. Validación de health checks
5. Activar nueva versión (Blue-Green)

### Estrategias de Deployment

- **Blue-Green Deployment**: Dos environments, swap entre ellos
- **Application Pool Recycling**: Para updates sin downtime
- **Web Deploy**: Automatización de despliegues

## Monitoreo

- IIS Logs para análisis
- Performance Counters expuestos
- Application Insights integration
- Failed Request Tracing

## Seguridad

- HTTPS obligatorio (redirect automático)
- HTTP/2 habilitado
- Request filtering configurado
- Rate limiting a nivel de IIS
- IP restrictions donde sea necesario

## Evolución Futura

Mantener puerta abierta a containerización:
- ASP.NET Core es portable
- Posible migración a Kubernetes en futuro
- IIS no debe acoplarse fuertemente al código de aplicación

## Referencias

- [IIS Configuration Guide](../guides/iis-configuration.md)
- [Deployment Guide](../guides/deployment.md)
- [Architecture Overview](../architecture/README.md)
