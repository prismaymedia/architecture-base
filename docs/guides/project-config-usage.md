# Guía de Uso: project_config.yaml

> **Archivo**: `project_config.yaml`  
> **Ubicación**: Raíz del repositorio  
> **Propósito**: Centralizar métricas de tareas y configuración del proyecto

---

## Tabla de Contenido

1. [Introducción](#introducción)
2. [Estructura del Archivo](#estructura-del-archivo)
3. [Configuración de Idiomas](#configuración-de-idiomas)
4. [Actualización Manual](#actualización-manual)
5. [Uso Programático](#uso-programático)
6. [Integración con Documentación](#integración-con-documentación)
7. [Integración con CI/CD](#integración-con-cicd)
8. [Casos de Uso](#casos-de-uso)
9. [Mejores Prácticas](#mejores-prácticas)

---

## Introducción

El archivo `project_config.yaml` es un archivo de configuración centralizado que contiene métricas relacionadas con la valoración de tareas en el proyecto y configuración de soporte de idiomas. Este archivo permite que scripts, herramientas de automatización y documentación accedan a configuración actualizada de forma consistente.

### Ventajas

- ✅ **Centralización**: Un único punto de verdad para métricas de tareas y configuración
- ✅ **Accesibilidad**: Fácil de leer para humanos y programas
- ✅ **Versionado**: Las métricas y configuración se versionan con el código
- ✅ **Automatización**: Scripts y CI/CD pueden consumir los valores
- ✅ **Transparencia**: Todo el equipo ve las mismas métricas y configuración
- ✅ **Multilenguaje**: Soporte para múltiples idiomas en documentación

---

## Estructura del Archivo

```yaml
# Archivo de configuración para la valoración de tareas
project_metrics:
  backlog_tasks_count: 0          # Número de tareas en backlog (Actualizar manualmente).
  qa_tasks_pending_count: 0       # Número de tareas pendientes en QA (Actualizar manualmente).
  qa_tasks_in_progress_count: 0   # Número de tareas en curso en QA (Actualizar manualmente).

# Configuración de soporte de idiomas para documentación
documentation:
  languages:
    default: es                    # Idioma por defecto para la documentación
    supported:                     # Lista de idiomas soportados
      - es                         # Español
      - en                         # Inglés
  environments:
    development:
      language: es                 # Idioma para entorno de desarrollo
      fallback_language: en        # Idioma de respaldo si no está disponible
    staging:
      language: es                 # Idioma para entorno de staging
      fallback_language: en        # Idioma de respaldo si no está disponible
    production:
      language: es                 # Idioma para entorno de producción
      fallback_language: en        # Idioma de respaldo si no está disponible
```

### Campos Disponibles

#### Project Metrics

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `backlog_tasks_count` | Integer | Número total de tareas en el backlog (To Do) |
| `qa_tasks_pending_count` | Integer | Número de tareas pendientes de revisión en QA |
| `qa_tasks_in_progress_count` | Integer | Número de tareas actualmente siendo revisadas en QA |

#### Documentation Configuration

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `documentation.languages.default` | String | Idioma por defecto (es, en) |
| `documentation.languages.supported` | Array[String] | Lista de idiomas soportados |
| `documentation.environments.<env>.language` | String | Idioma para el entorno específico |
| `documentation.environments.<env>.fallback_language` | String | Idioma de respaldo para el entorno |

---

## Configuración de Idiomas

### Idiomas Soportados

El proyecto soporta múltiples idiomas para documentación:

- **es**: Español (idioma principal)
- **en**: English (idioma secundario)

### Configuración por Entorno

Cada entorno puede tener su propia configuración de idioma:

```yaml
documentation:
  environments:
    development:
      language: es              # Idioma principal
      fallback_language: en     # Si falta traducción
    staging:
      language: es
      fallback_language: en
    production:
      language: es
      fallback_language: en
```

### Variables de Entorno

Para sobrescribir la configuración en tiempo de ejecución:

```bash
# En .env o variables de entorno
DOC_LANGUAGE=es                  # Idioma principal
DOC_FALLBACK_LANGUAGE=en         # Idioma de respaldo
ENVIRONMENT=development          # Entorno actual
```

### Casos de Uso de Idiomas

1. **Documentación en español por defecto**:
   - README, guías, ADRs en español
   - Comentarios de código en español
   - Mensajes de error en español

2. **Soporte para inglés**:
   - Traducciones opcionales de documentación
   - Colaboración internacional
   - API documentation en inglés

3. **Fallback automático**:
   - Si falta traducción en idioma principal, usa fallback
   - Scripts pueden detectar idioma disponible

---

## Actualización Manual

### Cuándo Actualizar

#### Métricas de Tareas

Actualiza los valores cuando:
- ✏️ Se agreguen nuevas tareas al backlog
- ✅ Tareas pasen de backlog a desarrollo
- 🔍 Tareas entren a QA (pending o in progress)
- ✅ Tareas completen QA y pasen a Done

#### Configuración de Idiomas

Actualiza cuando:
- 🌐 Se agregue soporte para un nuevo idioma
- 🔄 Se cambie el idioma por defecto de un entorno
- ✨ Se necesite habilitar/deshabilitar un idioma

### Cómo Actualizar

1. **Abre el archivo**:
   ```bash
   nano project_config.yaml
   # o usa tu editor favorito
   ```

2. **Actualiza los números (métricas)**:
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

#### Leer Métricas y Configuración de Idiomas

```python
import yaml
import os

# Leer configuración
with open('project_config.yaml', 'r') as f:
    config = yaml.safe_load(f)

# Acceder a métricas
metrics = config['project_metrics']
backlog_count = metrics['backlog_tasks_count']
qa_pending = metrics['qa_tasks_pending_count']
qa_in_progress = metrics['qa_tasks_in_progress_count']

# Acceder a configuración de idiomas
doc_config = config['documentation']
default_language = doc_config['languages']['default']
supported_languages = doc_config['languages']['supported']

# Obtener idioma para entorno específico
environment = os.getenv('ENVIRONMENT', 'development')
env_config = doc_config['environments'].get(environment, {})
language = os.getenv('DOC_LANGUAGE', env_config.get('language', default_language))
fallback = os.getenv('DOC_FALLBACK_LANGUAGE', env_config.get('fallback_language', 'en'))

print(f"Environment: {environment}")
print(f"Language: {language}")
print(f"Fallback: {fallback}")
print(f"Supported: {', '.join(supported_languages)}")

# Calcular métricas derivadas
total_qa_tasks = qa_pending + qa_in_progress
print(f"Backlog: {backlog_count}")
print(f"QA Total: {total_qa_tasks} (Pending: {qa_pending}, In Progress: {qa_in_progress})")
```

#### Función Helper para Idiomas

```python
import yaml
import os

def get_documentation_language(environment=None):
    """
    Obtiene el idioma de documentación para el entorno actual.
    
    Args:
        environment: Entorno específico (development, staging, production)
                    Si no se proporciona, se lee de ENVIRONMENT env var
    
    Returns:
        Tuple[str, str]: (language, fallback_language)
    """
    with open('project_config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    
    # Determinar entorno
    if environment is None:
        environment = os.getenv('ENVIRONMENT', 'development')
    
    doc_config = config['documentation']
    
    # Obtener idioma del entorno o usar default
    env_config = doc_config['environments'].get(environment, {})
    
    # Prioridad: ENV VAR > project_config > default
    language = os.getenv('DOC_LANGUAGE', 
                        env_config.get('language', 
                                     doc_config['languages']['default']))
    
    fallback = os.getenv('DOC_FALLBACK_LANGUAGE',
                        env_config.get('fallback_language', 'en'))
    
    return language, fallback

# Uso
lang, fallback = get_documentation_language()
print(f"Using language: {lang} (fallback: {fallback})")
```

#### Validar Idioma Soportado

```python
def is_language_supported(language):
    """
    Verifica si un idioma está soportado.
    
    Args:
        language: Código de idioma (es, en)
    
    Returns:
        bool: True si el idioma está soportado
    """
    with open('project_config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    
    supported = config['documentation']['languages']['supported']
    return language in supported

# Uso
if is_language_supported('es'):
    print("Spanish is supported")
```

### Node.js / JavaScript

#### Leer Configuración Completa

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

// Acceder a configuración de idiomas
const docConfig = config.documentation;
const defaultLanguage = docConfig.languages.default;
const supportedLanguages = docConfig.languages.supported;

// Obtener idioma para entorno
const environment = process.env.ENVIRONMENT || 'development';
const envConfig = docConfig.environments[environment] || {};
const language = process.env.DOC_LANGUAGE || envConfig.language || defaultLanguage;
const fallback = process.env.DOC_FALLBACK_LANGUAGE || envConfig.fallback_language || 'en';

console.log(`Environment: ${environment}`);
console.log(`Language: ${language}`);
console.log(`Fallback: ${fallback}`);
console.log(`Supported: ${supportedLanguages.join(', ')}`);
```

#### Función Helper para Idiomas (Node.js)

```javascript
const yaml = require('js-yaml');
const fs = require('fs');

/**
 * Obtiene el idioma de documentación para el entorno actual
 * @param {string} environment - Entorno específico (opcional)
 * @returns {{language: string, fallback: string}}
 */
function getDocumentationLanguage(environment) {
    const config = yaml.load(fs.readFileSync('project_config.yaml', 'utf8'));
    
    const env = environment || process.env.ENVIRONMENT || 'development';
    const docConfig = config.documentation;
    const envConfig = docConfig.environments[env] || {};
    
    const language = process.env.DOC_LANGUAGE || 
                    envConfig.language || 
                    docConfig.languages.default;
    
    const fallback = process.env.DOC_FALLBACK_LANGUAGE ||
                    envConfig.fallback_language || 
                    'en';
    
    return { language, fallback };
}

// Uso
const { language, fallback } = getDocumentationLanguage();
console.log(`Using language: ${language} (fallback: ${fallback})`);
```

### Bash / Shell Scripts

#### Leer Configuración con yq

```bash
#!/bin/bash

# Usando yq (YAML processor)
BACKLOG_COUNT=$(yq eval '.project_metrics.backlog_tasks_count' project_config.yaml)
QA_PENDING=$(yq eval '.project_metrics.qa_tasks_pending_count' project_config.yaml)
QA_IN_PROGRESS=$(yq eval '.project_metrics.qa_tasks_in_progress_count' project_config.yaml)

# Leer configuración de idiomas
DEFAULT_LANG=$(yq eval '.documentation.languages.default' project_config.yaml)
ENVIRONMENT=${ENVIRONMENT:-development}

# Obtener idioma para entorno específico
DOC_LANG=$(yq eval ".documentation.environments.${ENVIRONMENT}.language" project_config.yaml)
DOC_FALLBACK=$(yq eval ".documentation.environments.${ENVIRONMENT}.fallback_language" project_config.yaml)

# Usar variables de entorno si están definidas
DOC_LANG=${DOC_LANGUAGE:-$DOC_LANG}
DOC_FALLBACK=${DOC_FALLBACK_LANGUAGE:-$DOC_FALLBACK}

echo "Environment: $ENVIRONMENT"
echo "Language: $DOC_LANG"
echo "Fallback: $DOC_FALLBACK"
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
