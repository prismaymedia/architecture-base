# 🚀 Quick Start: Procesador Automático de Ideas

Esta guía te ayudará a comenzar a usar el procesador automático de ideas en menos de 5 minutos.

## 📋 Prerrequisitos

1. **Python 3.10+** instalado
2. **OpenAI API Key** (obtén una en https://platform.openai.com/api-keys)
3. Acceso a este repositorio

## ⚡ Instalación Rápida

### Paso 1: Instalar Dependencias

```bash
# Desde el directorio raíz del proyecto
cd /home/runner/work/architecture-base/architecture-base

# Instalar dependencias
pip install -r scripts/idea_processor/requirements.txt
```

### Paso 2: Configurar OpenAI API Key

```bash
# Opción A: Variable de entorno temporal
export OPENAI_API_KEY='sk-tu-api-key-aqui'

# Opción B: Archivo .env permanente
cp .env.example .env
# Edita .env y agrega tu API key
```

### Paso 3: Probar en Modo Preview

```bash
# Ver qué haría el script sin modificar archivos
./process-ideas.sh --dry-run
```

### Paso 4: Ejecutar

```bash
# Procesar ideas y actualizar archivos
./process-ideas.sh
```

## 📖 Uso Básico

### Agregar Ideas para Procesar

1. Abre `IDEAS.md`
2. Agrega tu idea en la sección de prioridad apropiada:

```markdown
### [ID-XXX] Título de tu Idea

- **Contexto**: ¿Quién necesita esto y por qué?
- **Problema**: ¿Qué problema específico resuelve?
- **Valor**: ¿Qué impacto tendrá?
- **Fecha**: 2025-11-14
- **Estado**: 💭 Por refinar
```

3. Guarda el archivo

### Procesar Ideas

```bash
# Ejecutar el procesador
./process-ideas.sh
```

El script automáticamente:
- ✅ Encuentra ideas con estado "💭 Por refinar"
- ✅ Detecta si son duplicadas (compara con US existentes y otras ideas)
- ✅ Marca duplicadas en IDEAS.md con referencia a la US similar
- ✅ Genera historias de usuario para ideas únicas
- ✅ Agrega nuevas US a BACKLOG.md
- ✅ Marca ideas como convertidas en IDEAS.md

### Revisar Resultados

```bash
# Ver cambios en IDEAS.md
git diff IDEAS.md

# Ver nuevas user stories en BACKLOG.md
git diff BACKLOG.md
```

## 🎨 Ejemplos de Output

### Ideas Duplicadas Detectadas

```
⚠️  Duplicate Ideas Found
┌──────────┬─────────────────────────────┬──────────────┬────────────┐
│ Idea ID  │ Title                       │ Similar To   │ Similarity │
├──────────┼─────────────────────────────┼──────────────┼────────────┤
│ ID-002   │ Sistema de Retry Int...     │ US-003       │ 87%        │
└──────────┴─────────────────────────────┴──────────────┴────────────┘
```

### User Stories Generadas

```
✨ Generated User Stories
┌────────┬──────────────────────────┬────────────┬──────────┬────────────┐
│ US ID  │ Title                    │ Priority   │ Points   │ Epic       │
├────────┼──────────────────────────┼────────────┼──────────┼────────────┤
│ US-011 │ Dashboard de Métricas    │ Alta 🔴    │ 8        │ Analytics  │
│ US-012 │ Versionado Automático    │ Media 🟡   │ 5        │ DevOps     │
└────────┴──────────────────────────┴────────────┴──────────┴────────────┘
```

## 🔧 Comandos Útiles

```bash
# Preview sin modificar archivos
./process-ideas.sh --dry-run

# Ajustar umbral de similitud (más estricto = menos duplicados)
./process-ideas.sh --threshold 0.90

# Ver ayuda completa
./process-ideas.sh --help

# Modo verbose para debugging
./process-ideas.sh --verbose
```

## ❓ Troubleshooting

### "OpenAI API key not found"

**Solución:**
```bash
export OPENAI_API_KEY='sk-tu-key-aqui'
```

### "Module 'openai' not found"

**Solución:**
```bash
pip install -r scripts/idea_processor/requirements.txt
```

### Falsos Duplicados

**Solución:** Aumenta el threshold
```bash
./process-ideas.sh --threshold 0.90
```

### No Detecta Duplicados Obvios

**Solución:** Reduce el threshold
```bash
./process-ideas.sh --threshold 0.75
```

## 📚 Más Información

- [README Completo](scripts/idea_processor/README.md) - Documentación detallada
- [Flujo Ideas → Tasks](docs/guides/idea-to-task-flow.md) - Proceso completo
- [BACKLOG.md](BACKLOG.md) - Ver historias de usuario
- [IDEAS.md](IDEAS.md) - Ver ideas capturadas

## 💡 Tips

1. **Siempre usa --dry-run primero** para ver qué cambios se harían
2. **Revisa las US generadas** antes de moverlas a "In Progress"
3. **Ajusta manualmente** criterios de aceptación si es necesario
4. **Refina las ideas** antes de procesarlas para mejores resultados
5. **Usa prioridades** (🔴🟡🟢) para organizar mejor

## 🎯 Workflow Recomendado

1. **Captura ideas** en IDEAS.md durante la semana
2. **Viernes**: Ejecuta `./process-ideas.sh --dry-run` para preview
3. **Revisas** las US que se generarían
4. **Si está bien**: Ejecuta `./process-ideas.sh` para aplicar cambios
5. **Refinamiento**: Ajusta las US generadas según necesidad
6. **Siguiente sprint**: Usa Copilot para generar tareas técnicas

---

**¿Necesitas ayuda?** Consulta la documentación completa en `scripts/idea_processor/README.md`
