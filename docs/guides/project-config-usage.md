# Guía de Uso: project_config.yaml

> **Archivo**: `project_config.yaml`  
> **Ubicación**: Raíz del repositorio  
> **Propósito**: Centralizar métricas de tareas para valoración y seguimiento

---

## Tabla de Contenido

1. [Introducción](#introducción)
2. [Estructura del Archivo](#estructura-del-archivo)
3. [Actualización Manual](#actualización-manual)
4. [Uso Programático](#uso-programático)
5. [Integración con Documentación](#integración-con-documentación)
6. [Integración con CI/CD](#integración-con-cicd)
7. [Casos de Uso](#casos-de-uso)
8. [Mejores Prácticas](#mejores-prácticas)

---

## Introducción

El archivo `project_config.yaml` es un archivo de configuración centralizado que contiene métricas relacionadas con la valoración de tareas en el proyecto. Este archivo permite que scripts, herramientas de automatización y documentación accedan a métricas actualizadas de forma consistente.

### Ventajas

- ✅ **Centralización**: Un único punto de verdad para métricas de tareas
- ✅ **Accesibilidad**: Fácil de leer para humanos y programas
- ✅ **Versionado**: Las métricas se versionan con el código
- ✅ **Automatización**: Scripts y CI/CD pueden consumir los valores
- ✅ **Transparencia**: Todo el equipo ve las mismas métricas

---

## Estructura del Archivo

```yaml
# Archivo de configuración para la valoración de tareas
project_metrics:
  backlog_tasks_count: 0          # Número de tareas en backlog (Actualizar manualmente).
  qa_tasks_pending_count: 0       # Número de tareas pendientes en QA (Actualizar manualmente).
  qa_tasks_in_progress_count: 0   # Número de tareas en curso en QA (Actualizar manualmente).
```

### Campos Disponibles

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `backlog_tasks_count` | Integer | Número total de tareas en el backlog (To Do) |
| `qa_tasks_pending_count` | Integer | Número de tareas pendientes de revisión en QA |
| `qa_tasks_in_progress_count` | Integer | Número de tareas actualmente siendo revisadas en QA |

---

## Actualización Manual

### Cuándo Actualizar

Actualiza los valores cuando:
- ✏️ Se agreguen nuevas tareas al backlog
- ✅ Tareas pasen de backlog a desarrollo
- 🔍 Tareas entren a QA (pending o in progress)
- ✅ Tareas completen QA y pasen a Done

### Cómo Actualizar

1. **Abre el archivo**:
   ```bash
   nano project_config.yaml
   # o usa tu editor favorito
   ```

2. **Actualiza los números**:
   ```yaml
   project_metrics:
     backlog_tasks_count: 15        # Actualizado
     qa_tasks_pending_count: 3      # Actualizado
     qa_tasks_in_progress_count: 2  # Actualizado
   ```

3. **Valida la sintaxis YAML**:
   ```bash
   python3 -c "import yaml; yaml.safe_load(open('project_config.yaml'))"
   ```

4. **Commit los cambios**:
   ```bash
   git add project_config.yaml
   git commit -m "Update project metrics: backlog=15, qa_pending=3, qa_in_progress=2"
   git push
   ```

### Ejemplo de Actualización Semanal

```bash
# Lunes por la mañana, después de revisar el estado del proyecto
# Backlog: 12 tareas
# QA Pending: 4 tareas
# QA In Progress: 2 tareas

# Editar el archivo y actualizar valores
vim project_config.yaml

# Commit con descripción clara
git add project_config.yaml
git commit -m "Weekly metrics update (Week 47): backlog=12, qa_pending=4, qa_in_progress=2"
git push
```

---

## Uso Programático

### Python

```python
import yaml

# Leer configuración
with open('project_config.yaml', 'r') as f:
    config = yaml.safe_load(f)

# Acceder a métricas
metrics = config['project_metrics']
backlog_count = metrics['backlog_tasks_count']
qa_pending = metrics['qa_tasks_pending_count']
qa_in_progress = metrics['qa_tasks_in_progress_count']

# Calcular métricas derivadas
total_qa_tasks = qa_pending + qa_in_progress
print(f"Backlog: {backlog_count}")
print(f"QA Total: {total_qa_tasks} (Pending: {qa_pending}, In Progress: {qa_in_progress})")
```

### Node.js / JavaScript

```javascript
const yaml = require('js-yaml');
const fs = require('fs');

// Leer configuración
const config = yaml.load(fs.readFileSync('project_config.yaml', 'utf8'));

// Acceder a métricas
const metrics = config.project_metrics;
console.log(`Backlog: ${metrics.backlog_tasks_count}`);
console.log(`QA Pending: ${metrics.qa_tasks_pending_count}`);
console.log(`QA In Progress: ${metrics.qa_tasks_in_progress_count}`);
```

### Bash / Shell Scripts

```bash
#!/bin/bash

# Usando yq (YAML processor)
BACKLOG_COUNT=$(yq eval '.project_metrics.backlog_tasks_count' project_config.yaml)
QA_PENDING=$(yq eval '.project_metrics.qa_tasks_pending_count' project_config.yaml)
QA_IN_PROGRESS=$(yq eval '.project_metrics.qa_tasks_in_progress_count' project_config.yaml)

echo "Backlog: $BACKLOG_COUNT"
echo "QA Pending: $QA_PENDING"
echo "QA In Progress: $QA_IN_PROGRESS"
```

### GitHub Actions

```yaml
name: Check Project Metrics

on: [push]

jobs:
  metrics:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Read Project Metrics
        run: |
          pip install pyyaml
          python3 << EOF
          import yaml
          with open('project_config.yaml') as f:
              metrics = yaml.safe_load(f)['project_metrics']
              print(f"📊 Project Metrics:")
              print(f"  Backlog: {metrics['backlog_tasks_count']}")
              print(f"  QA Pending: {metrics['qa_tasks_pending_count']}")
              print(f"  QA In Progress: {metrics['qa_tasks_in_progress_count']}")
          EOF
```

---

## Integración con Documentación

### Generación Dinámica de README

Puedes crear scripts que lean el config y actualicen automáticamente secciones del README:

```python
# scripts/update_readme_metrics.py
import yaml
import re

# Leer métricas
with open('project_config.yaml') as f:
    metrics = yaml.safe_load(f)['project_metrics']

# Leer README
with open('README.md', 'r') as f:
    readme = f.read()

# Actualizar sección de métricas
metrics_section = f"""
## 📊 Métricas Actuales

- 📋 **Backlog**: {metrics['backlog_tasks_count']} tareas
- ⏳ **QA Pending**: {metrics['qa_tasks_pending_count']} tareas
- 🔍 **QA In Progress**: {metrics['qa_tasks_in_progress_count']} tareas

_Última actualización: automática desde project_config.yaml_
"""

# Reemplazar o insertar la sección
# (implementar lógica de reemplazo según necesidad)
```

### Badges Dinámicos

Genera badges para mostrar en el README:

```python
# scripts/generate_badges.py
import yaml

with open('project_config.yaml') as f:
    metrics = yaml.safe_load(f)['project_metrics']
    backlog = metrics['backlog_tasks_count']

# Generar URL de badge
badge_url = f"https://img.shields.io/badge/Backlog-{backlog}_tasks-blue"
print(f"![Backlog]({badge_url})")
```

Resultado en README:
```markdown
![Backlog](https://img.shields.io/badge/Backlog-15_tasks-blue)
![QA Pending](https://img.shields.io/badge/QA_Pending-3_tasks-yellow)
![QA In Progress](https://img.shields.io/badge/QA_In_Progress-2_tasks-orange)
```

---

## Integración con CI/CD

### Validación en Pull Requests

```yaml
# .github/workflows/validate-metrics.yml
name: Validate Project Config

on:
  pull_request:
    paths:
      - 'project_config.yaml'

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Validate YAML Syntax
        run: |
          pip install pyyaml
          python3 -c "import yaml; yaml.safe_load(open('project_config.yaml'))"
      
      - name: Validate Metrics Values
        run: |
          python3 << EOF
          import yaml
          with open('project_config.yaml') as f:
              metrics = yaml.safe_load(f)['project_metrics']
              
          # Validar que todos los valores sean >= 0
          for key, value in metrics.items():
              assert isinstance(value, int), f"{key} debe ser un entero"
              assert value >= 0, f"{key} debe ser >= 0"
          
          print("✅ Todas las métricas son válidas")
          EOF
```

### Alertas Automáticas

```yaml
# .github/workflows/metrics-alert.yml
name: Metrics Alert

on:
  push:
    paths:
      - 'project_config.yaml'
    branches:
      - main

jobs:
  alert:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Check High Backlog
        run: |
          python3 << EOF
          import yaml
          with open('project_config.yaml') as f:
              backlog = yaml.safe_load(f)['project_metrics']['backlog_tasks_count']
          
          if backlog > 20:
              print(f"⚠️ ALERTA: Backlog muy alto ({backlog} tareas)")
              print("Considera priorizar y refinamiento de tareas")
          else:
              print(f"✅ Backlog bajo control ({backlog} tareas)")
          EOF
```

---

## Casos de Uso

### 1. Dashboard de Métricas

Crea un script que genere un dashboard visual:

```python
# scripts/generate_dashboard.py
import yaml
from datetime import datetime

with open('project_config.yaml') as f:
    metrics = yaml.safe_load(f)['project_metrics']

print("=" * 50)
print("       DASHBOARD DE MÉTRICAS DEL PROYECTO")
print("=" * 50)
print(f"\n📅 Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
print(f"📋 Backlog Tasks:        {metrics['backlog_tasks_count']:>3}")
print(f"⏳ QA Pending:           {metrics['qa_tasks_pending_count']:>3}")
print(f"🔍 QA In Progress:       {metrics['qa_tasks_in_progress_count']:>3}")
print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
qa_total = metrics['qa_tasks_pending_count'] + metrics['qa_tasks_in_progress_count']
print(f"📊 Total QA:             {qa_total:>3}")
print(f"📈 Total Tasks:          {metrics['backlog_tasks_count'] + qa_total:>3}")
print("=" * 50)
```

### 2. Reporte Semanal Automatizado

```python
# scripts/weekly_report.py
import yaml
from datetime import datetime

with open('project_config.yaml') as f:
    metrics = yaml.safe_load(f)['project_metrics']

# Generar reporte
report = f"""
# Reporte Semanal de Métricas
**Fecha**: {datetime.now().strftime('%Y-%m-%d')}

## Estado Actual
- Backlog: {metrics['backlog_tasks_count']} tareas
- QA Pending: {metrics['qa_tasks_pending_count']} tareas  
- QA In Progress: {metrics['qa_tasks_in_progress_count']} tareas

## Análisis
- Total en QA: {metrics['qa_tasks_pending_count'] + metrics['qa_tasks_in_progress_count']}
- Tasa QA/Backlog: {((metrics['qa_tasks_pending_count'] + metrics['qa_tasks_in_progress_count']) / max(metrics['backlog_tasks_count'], 1) * 100):.1f}%

## Recomendaciones
{"⚠️ Backlog muy alto, priorizar refinamiento" if metrics['backlog_tasks_count'] > 20 else "✅ Backlog bajo control"}
{"⚠️ QA saturado, considerar más revisores" if metrics['qa_tasks_pending_count'] > 5 else "✅ QA fluyendo bien"}
"""

print(report)

# Opcional: enviar por email o Slack
```

### 3. Integración con ClickUp

```python
# scripts/sync_to_clickup.py
import yaml
import requests

with open('project_config.yaml') as f:
    metrics = yaml.safe_load(f)['project_metrics']

# Actualizar custom fields en ClickUp
CLICKUP_API_TOKEN = "your_token"
LIST_ID = "your_list_id"

headers = {"Authorization": CLICKUP_API_TOKEN}
data = {
    "backlog_count": metrics['backlog_tasks_count'],
    "qa_pending": metrics['qa_tasks_pending_count'],
    "qa_in_progress": metrics['qa_tasks_in_progress_count']
}

# Actualizar campos personalizados
# (implementar según API de ClickUp)
```

---

## Mejores Prácticas

### ✅ DO: Hacer

1. **Actualiza regularmente**: Establece una cadencia (diaria o semanal) para actualizar métricas
2. **Commits descriptivos**: Usa mensajes claros al actualizar: `"Update metrics: backlog=15, qa_pending=3"`
3. **Valida antes de commit**: Siempre valida sintaxis YAML antes de hacer commit
4. **Documenta cambios**: Si hay cambios significativos, explica el por qué en el commit message
5. **Automatiza lecturas**: Usa scripts para leer y mostrar métricas en dashboards
6. **Versionamiento**: El archivo está en git, así que puedes ver histórico de métricas

### ❌ DON'T: Evitar

1. **No automatices escritura sin validación**: Actualización manual permite control de calidad
2. **No uses para datos sensibles**: Este archivo es público en el repo
3. **No agregues campos sin documentar**: Mantén esta guía actualizada si agregas campos
4. **No ignores valores negativos**: Las métricas deben ser >= 0
5. **No olvides validar YAML**: Sintaxis incorrecta puede romper scripts

---

## Preguntas Frecuentes

### ¿Por qué actualización manual y no automática?

La actualización manual permite:
- Control consciente de las métricas
- Validación humana de los números
- Flexibilidad para ajustar según contexto
- Evita sincronización automática que puede fallar

### ¿Puedo agregar más campos?

Sí, puedes agregar campos adicionales. Ejemplo:

```yaml
project_metrics:
  backlog_tasks_count: 15
  qa_tasks_pending_count: 3
  qa_tasks_in_progress_count: 2
  # Nuevos campos
  done_tasks_this_week: 8
  blocked_tasks_count: 1
  avg_cycle_time_days: 4.5
```

Recuerda actualizar esta documentación cuando agregues campos.

### ¿Cómo ver el histórico de métricas?

Usa git para ver cambios históricos:

```bash
# Ver todos los cambios al archivo
git log --oneline -- project_config.yaml

# Ver diferencias entre commits
git diff HEAD~5 HEAD -- project_config.yaml

# Ver valor en fecha específica
git show <commit>:project_config.yaml
```

### ¿Puedo integrar con herramientas externas?

Sí, puedes crear scripts que:
- Lean el archivo y envíen a Slack/Discord
- Actualicen dashboards en Notion/Confluence
- Sincronicen con Jira/ClickUp/Trello
- Generen gráficos con matplotlib/plotly

---

## Ejemplos Completos

### Script de Monitoreo Completo

```python
#!/usr/bin/env python3
"""
Monitor de Métricas del Proyecto
Uso: python3 scripts/monitor_metrics.py
"""

import yaml
import sys
from datetime import datetime

def load_metrics():
    """Carga métricas desde project_config.yaml"""
    try:
        with open('project_config.yaml', 'r') as f:
            config = yaml.safe_load(f)
            return config['project_metrics']
    except FileNotFoundError:
        print("❌ Error: project_config.yaml no encontrado")
        sys.exit(1)
    except yaml.YAMLError as e:
        print(f"❌ Error de sintaxis YAML: {e}")
        sys.exit(1)

def analyze_metrics(metrics):
    """Analiza métricas y genera insights"""
    backlog = metrics['backlog_tasks_count']
    qa_pending = metrics['qa_tasks_pending_count']
    qa_in_progress = metrics['qa_tasks_in_progress_count']
    
    insights = []
    
    # Análisis de backlog
    if backlog > 20:
        insights.append("⚠️ Backlog muy alto - Considerar refinamiento")
    elif backlog < 5:
        insights.append("⚠️ Backlog muy bajo - Planear próximas features")
    else:
        insights.append("✅ Backlog saludable")
    
    # Análisis de QA
    qa_total = qa_pending + qa_in_progress
    if qa_total > 8:
        insights.append("⚠️ QA saturado - Considerar más revisores")
    elif qa_total == 0 and backlog > 0:
        insights.append("⚠️ Sin tareas en QA - Verificar flujo")
    else:
        insights.append("✅ QA fluyendo bien")
    
    # Análisis de ratio
    if backlog > 0:
        ratio = (qa_total / backlog) * 100
        if ratio > 50:
            insights.append("⚠️ Ratio QA/Backlog alto - Posible cuello de botella")
    
    return insights

def print_dashboard(metrics):
    """Imprime dashboard visual"""
    print("\n" + "=" * 60)
    print("          🎯 DASHBOARD DE MÉTRICAS DEL PROYECTO")
    print("=" * 60)
    print(f"\n📅 Actualizado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    backlog = metrics['backlog_tasks_count']
    qa_pending = metrics['qa_tasks_pending_count']
    qa_in_progress = metrics['qa_tasks_in_progress_count']
    qa_total = qa_pending + qa_in_progress
    total = backlog + qa_total
    
    print(f"📋 Backlog Tasks:          {backlog:>4}")
    print(f"⏳ QA Pending:             {qa_pending:>4}")
    print(f"🔍 QA In Progress:         {qa_in_progress:>4}")
    print(f"{'─' * 60}")
    print(f"📊 Total en QA:            {qa_total:>4}")
    print(f"📈 Total de Tasks:         {total:>4}")
    
    if backlog > 0:
        qa_ratio = (qa_total / backlog) * 100
        print(f"📉 Ratio QA/Backlog:       {qa_ratio:>5.1f}%")
    
    print("\n" + "=" * 60)
    
    # Insights
    print("\n💡 INSIGHTS:")
    for insight in analyze_metrics(metrics):
        print(f"   {insight}")
    
    print("\n" + "=" * 60 + "\n")

if __name__ == "__main__":
    metrics = load_metrics()
    print_dashboard(metrics)
```

Guarda como `scripts/monitor_metrics.py` y ejecuta:

```bash
python3 scripts/monitor_metrics.py
```

---

## Recursos Adicionales

- 📖 [Manual de Product Owner](product-owner-guide.md)
- 📖 [Guía de Kanban](kanban-guide.md)
- 📋 [BACKLOG.md](../../BACKLOG.md)
- 🔧 [GitHub Actions para validación](.github/workflows/)

---

**Última actualización**: 2025-11-14  
**Mantenedor**: @prismaymedia
