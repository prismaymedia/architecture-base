# Decisión Arquitectónica 005: React con Vite para el Frontend

**Estado**: Aceptado  
**Fecha**: 2025-11-14  
**Decisores**: Equipo de Arquitectura  
**Reemplaza**: ADR-003 (IIS Web Server), ADR-004 (BIT Components Platform) - parcialmente

## Contexto

El proyecto requiere un frontend moderno y reactivo para interactuar con nuestro sistema de microservicios. Necesitamos una tecnología que:
- Permita desarrollo rápido con hot-reload
- Tenga excelente rendimiento en build y runtime
- Soporte TypeScript para type-safety
- Tenga un ecosistema maduro y amplia comunidad
- Sea compatible con arquitecturas de microservicios

## Decisión

Implementaremos el frontend utilizando **React 18+** con **Vite** como build tool y development server.

## Justificación

### React

#### Ventajas
1. **Ecosistema Maduro**: Amplia variedad de librerías y componentes
2. **Component-Based**: Arquitectura modular que facilita reutilización
3. **Performance**: Virtual DOM y optimizaciones automáticas
4. **TypeScript Support**: Excelente integración con TypeScript
5. **Comunidad**: Gran comunidad y abundante documentación
6. **Hooks**: API moderna para gestión de estado y side effects
7. **React Server Components**: Preparado para futuras optimizaciones

#### Desventajas
1. **Curva de Aprendizaje**: Requiere entender conceptos como hooks, context, etc.
2. **Boilerplate**: Puede requerir configuración adicional para proyectos complejos
3. **Bundle Size**: Sin optimización puede generar bundles grandes

### Vite

#### Ventajas
1. **Velocidad**: Dev server extremadamente rápido con HMR instantáneo
2. **Build Optimizado**: Usa Rollup para producción con tree-shaking
3. **ESM Native**: Aprovecha ES modules nativos del navegador
4. **TypeScript Built-in**: Soporte de TypeScript sin configuración adicional
5. **Plugin Ecosystem**: Amplio ecosistema de plugins
6. **Zero Config**: Funciona out-of-the-box con configuración mínima

#### Desventajas
1. **Relativamente Nuevo**: Menor madurez que Webpack
2. **Compatibilidad**: Algunos paquetes antiguos pueden requerir configuración adicional

## Alternativas Consideradas

### 1. Angular + Angular CLI
- **Rechazado**: Framework más opinionado y pesado
- Mayor curva de aprendizaje
- Menos flexibilidad

### 2. Vue.js + Vite
- **Rechazado**: Aunque excelente, React tiene mayor adopción en el mercado
- Menor ecosistema de componentes enterprise

### 3. Next.js
- **Rechazado**: Framework más opinionado con SSR/SSG
- Overhead innecesario para nuestra arquitectura de microservicios
- Preferimos mayor control sobre el routing y data fetching

### 4. Create React App
- **Rechazado**: Más lento en desarrollo
- Configuración más compleja
- Webpack es más pesado que Vite

### 5. .NET Blazor
- **Rechazado**: Ecosistema más limitado
- Comunidad más pequeña
- WebAssembly overhead

## Consecuencias

### Positivas
- Desarrollo extremadamente rápido con Vite HMR
- Build times reducidos significativamente
- Excelente experiencia de desarrollo
- Fácil integración con APIs REST y GraphQL
- Amplio ecosistema de componentes UI (Material-UI, Ant Design, etc.)
- Soporte moderno de TypeScript
- Facilita implementación de micro-frontends si es necesario

### Negativas
- Equipo debe aprender React si no está familiarizado
- Necesidad de gestionar estado global (Redux, Zustand, React Query)
- Requiere tooling adicional para testing (Vitest, Testing Library)
- Build process adicional comparado con server-side rendering tradicional

## Stack Tecnológico del Frontend

### Core
- **React**: ^18.3.0 (latest)
- **TypeScript**: ^5.6.0
- **Vite**: ^5.4.0

### Routing
- **React Router**: ^6.x (client-side routing)

### State Management
- **React Query / TanStack Query**: Para server state
- **Zustand**: Para client state global (alternativa ligera a Redux)
- **Context API**: Para estado compartido simple

### UI Libraries (Recomendadas)
- **shadcn/ui**: Componentes modernos con Tailwind CSS
- **Material-UI (MUI)**: Componentes enterprise-ready
- **Ant Design**: Alternativa robusta para dashboards

### Styling
- **Tailwind CSS**: Utility-first CSS framework
- **CSS Modules**: Para estilos component-scoped

### Testing
- **Vitest**: Test runner (compatible con Vite)
- **React Testing Library**: Testing de componentes
- **MSW (Mock Service Worker)**: Mocking de APIs

### Build & Dev Tools
- **ESLint**: Linting
- **Prettier**: Code formatting
- **TypeScript ESLint**: Type-aware linting

## Arquitectura del Frontend

### Estructura de Proyecto

```
frontend/
├── src/
│   ├── components/          # Componentes reutilizables
│   │   ├── common/          # Componentes compartidos
│   │   └── features/        # Componentes específicos de features
│   ├── pages/               # Componentes de página (routes)
│   ├── hooks/               # Custom React hooks
│   ├── services/            # API clients y servicios
│   ├── stores/              # State management (Zustand stores)
│   ├── types/               # TypeScript types y interfaces
│   ├── utils/               # Funciones utilitarias
│   ├── config/              # Configuración de la app
│   ├── assets/              # Imágenes, fonts, etc.
│   ├── App.tsx              # Componente raíz
│   ├── main.tsx             # Entry point
│   └── vite-env.d.ts        # Vite types
├── public/                  # Assets estáticos
├── tests/                   # Tests
├── .env.example             # Variables de entorno de ejemplo
├── .eslintrc.cjs            # Configuración ESLint
├── .prettierrc              # Configuración Prettier
├── tsconfig.json            # Configuración TypeScript
├── vite.config.ts           # Configuración Vite
└── package.json
```

### Patrones de Diseño

1. **Component Composition**: Favor composition over inheritance
2. **Custom Hooks**: Lógica reutilizable en hooks personalizados
3. **Separation of Concerns**: Separar UI, lógica y data fetching
4. **Error Boundaries**: Manejo de errores en componentes
5. **Lazy Loading**: Code splitting para rutas y componentes pesados

## Integración con Backend

El frontend se comunicará con los microservicios Python mediante:
- **REST APIs**: Para operaciones CRUD estándar
- **WebSockets**: Para notificaciones en tiempo real (opcional)
- **GraphQL**: Si se implementa capa de agregación (futuro)

### API Client Pattern

```typescript
// services/api-client.ts
import axios from 'axios';

const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
  timeout: 10000,
});

// Interceptors para auth, logging, etc.
```

## Implementación

### Fase 1: Setup Inicial
1. Crear proyecto con Vite: `npm create vite@latest frontend -- --template react-ts`
2. Configurar ESLint y Prettier
3. Configurar path aliases en tsconfig
4. Setup básico de routing
5. Implementar layout base

### Fase 2: Core Features
1. Implementar autenticación y autorización
2. Setup de React Query para data fetching
3. Implementar manejo de errores global
4. Crear componentes base del design system

### Fase 3: Features Específicas
1. Implementar features por microservicio (orders, inventory, etc.)
2. Integrar con APIs Python
3. Testing de integración

### Fase 4: Optimización
1. Implementar code splitting
2. Optimizar bundle size
3. Implementar PWA features (opcional)
4. Performance monitoring

## Notas

- El frontend será un SPA (Single Page Application)
- Para SEO crítico, considerar agregar pre-rendering o SSR en el futuro
- Mantener TypeScript strict mode habilitado
- Seguir convenciones de React y mejores prácticas
- Documentar componentes con JSDoc/TSDoc

## Referencias

- [React Documentation](https://react.dev/)
- [Vite Documentation](https://vitejs.dev/)
- [TypeScript Documentation](https://www.typescriptlang.org/)
- [React Router](https://reactrouter.com/)
- [TanStack Query](https://tanstack.com/query/latest)
