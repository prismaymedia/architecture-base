# 📘 Guía de Integración con ClickUp

> **Propósito**: Documentar cómo exportar tareas generadas automáticamente hacia ClickUp para ejecución por el equipo.

---

## 📊 Visión General

Una vez que has revisado y aprobado las tareas preliminares generadas por Copilot, necesitas crearlas en ClickUp para que el equipo pueda trabajar en ellas. Esta guía cubre tres métodos de exportación.

---

## 🎯 Prerequisitos

### Configuración de ClickUp

1. **Espacio/Proyecto configurado**:
   - Workspace en ClickUp
   - Project/List para el sprint actual
   - Folders organizados por Epic (opcional pero recomendado)

2. **Custom Fields creados**:
   - `Story Points` (Number field)
   - `Related US` (Text field para vincular a User Story)
   - `Epic` (Dropdown: Order Management, Inventory Control, Payments, Notifications, etc.)
   - `Service` (Dropdown: orders-api, inventory-api, payments-api, notifications-api)
   - `Technical Type` (Dropdown: API Endpoint, Domain Model, Repository, Event Handler, etc.)

3. **Priorities configuradas**:
   - 🔴 Urgent
   - 🟠 High
   - 🟡 Normal
   - 🟢 Low

4. **Statuses configurados**:
   - 📝 To Do
   - 🔨 In Progress
   - 🧪 In Testing
   - 👀 In Review
   - ✅ Done

---

## 📋 Método 1: Creación Manual (Copy-Paste)

**Mejor para**: Pocos tasks (< 5), control total del formato, primera vez configurando.

### Paso a Paso

1. **Prepara el archivo de exportación**:
   - Copilot genera `sprint-X-tasks.md` con todas las tareas aprobadas
   - Cada tarea está en formato Markdown completo

2. **Para cada tarea en ClickUp**:

   a. **Crea nueva tarea**:
      - Click en "+ New Task" en tu List/Project
      - Nombre: Copia el título (ej: "Implement Create Order API Endpoint")

   b. **Configura campos básicos**:
      - Priority: Convierte emoji a nivel (🔴 → Urgent, 🟡 → Normal, etc.)
      - Assignee: Selecciona developer (o deja sin asignar para Sprint Planning)
      - Due Date: Si aplica (fecha de fin del sprint)

   c. **Configura Custom Fields**:
      - Story Points: Copia el número del archivo
      - Related US: Ej: "US-001"
      - Epic: Ej: "Order Management"
      - Service: Ej: "orders-api"
      - Technical Type: Ej: "API Endpoint"

   d. **Pega la descripción**:
      - Abre el editor de descripción en ClickUp
      - Copia **toda** la sección de descripción del archivo generado:
        ```markdown
        ### 📋 Description
        [contenido completo]
        
        ### ✅ Functional Acceptance Criteria
        [contenido completo]
        
        ### 🔧 Technical Acceptance Criteria
        [contenido completo]
        
        ### 🏗️ Best Practices to Apply
        [contenido completo]
        
        ### 💡 Recommendations
        [contenido completo]
        
        ### 🔗 Related Resources
        [contenido completo]
        
        ### ✅ Definition of Done
        [contenido completo]
        ```
      - ClickUp renderiza Markdown automáticamente

   e. **Agrega Checklist**:
      - Los Acceptance Criteria y Best Practices tienen checkboxes `- [ ]`
      - ClickUp los convierte en checklist nativo automáticamente
      - Alternativamente, cópialos a la sección "Checklist" de ClickUp

   f. **Tags opcionales**:
      - Agrega tags como: `sprint-1`, `backend`, `event-driven`, etc.

3. **Repite para cada tarea**

### Ventajas

✅ Control total sobre formato y campos  
✅ Puedes ajustar en tiempo real  
✅ No requiere configuración técnica  
✅ Ideal para sprints pequeños  

### Desventajas

❌ Manual y repetitivo  
❌ Propenso a errores humanos (copy-paste incorrecto)  
❌ Lento para muchas tareas (>10)  

---

## 🚀 Método 2: ClickUp API (Automatizado)

**Mejor para**: Muchas tareas (>10), automatización repetida, equipos técnicos.

### Configuración Inicial

1. **Obtén API Key**:
   - Ve a ClickUp → Settings → Apps
   - Click en "Generate" en API Token section
   - Copia el token (ej: `pk_123456_ABCDEFGHIJKLMNOP`)
   - **Guárdalo de forma segura** (no lo commites al repo)

2. **Identifica IDs necesarios**:
   - **Workspace ID**: En la URL de ClickUp (ej: `https://app.clickup.com/123456/...`)
   - **Space ID**: Click en Space → Settings → URL tiene el ID
   - **List ID**: Click en List → Settings → Copy List ID
   - **Custom Field IDs**: Usa API para listarlos (ver script abajo)

3. **Configura variables de entorno**:
   ```bash
   # .env (NO commitar este archivo)
   CLICKUP_API_TOKEN=pk_123456_ABCDEFGHIJKLMNOP
   CLICKUP_WORKSPACE_ID=123456
   CLICKUP_SPACE_ID=789012
   CLICKUP_LIST_ID=345678
   CLICKUP_CUSTOM_FIELD_STORY_POINTS=abcd-1234-efgh-5678
   CLICKUP_CUSTOM_FIELD_RELATED_US=ijkl-9012-mnop-3456
   CLICKUP_CUSTOM_FIELD_EPIC=qrst-5678-uvwx-9012
   CLICKUP_CUSTOM_FIELD_SERVICE=yzab-3456-cdef-7890
   ```

### Script de Exportación

Copilot puede generar este script cuando lo solicites. Ejemplo:

```python
# scripts/export-to-clickup.py

import os
import json
import requests
from dotenv import load_dotenv
import markdown  # pip install markdown

load_dotenv()

API_TOKEN = os.getenv('CLICKUP_API_TOKEN')
LIST_ID = os.getenv('CLICKUP_LIST_ID')
BASE_URL = 'https://api.clickup.com/api/v2'

HEADERS = {
    'Authorization': API_TOKEN,
    'Content-Type': 'application/json'
}

def parse_task_from_markdown(task_md):
    """
    Parsea archivo Markdown de tarea y extrae campos estructurados.
    """
    # Implementación completa proporcionada por Copilot cuando lo solicites
    pass

def create_clickup_task(task_data):
    """
    Crea tarea en ClickUp vía API.
    """
    url = f"{BASE_URL}/list/{LIST_ID}/task"
    
    payload = {
        "name": task_data['title'],
        "description": task_data['description_md'],
        "priority": task_data['priority_id'],  # 1=urgent, 2=high, 3=normal, 4=low
        "custom_fields": [
            {
                "id": os.getenv('CLICKUP_CUSTOM_FIELD_STORY_POINTS'),
                "value": task_data['story_points']
            },
            {
                "id": os.getenv('CLICKUP_CUSTOM_FIELD_RELATED_US'),
                "value": task_data['related_us']
            },
            {
                "id": os.getenv('CLICKUP_CUSTOM_FIELD_EPIC'),
                "value": task_data['epic']
            },
            {
                "id": os.getenv('CLICKUP_CUSTOM_FIELD_SERVICE'),
                "value": task_data['service']
            }
        ],
        "tags": task_data['tags']
    }
    
    response = requests.post(url, json=payload, headers=HEADERS)
    
    if response.status_code == 200:
        task_id = response.json()['id']
        print(f"✅ Created: {task_data['title']} (ID: {task_id})")
        return task_id
    else:
        print(f"❌ Failed: {task_data['title']}")
        print(f"   Error: {response.text}")
        return None

def main(sprint_file):
    print(f"📋 Importing tasks from {sprint_file}...")
    
    # Parsea archivo generado por Copilot
    with open(sprint_file, 'r') as f:
        content = f.read()
    
    # Extrae tareas individuales (separadas por ## TASK-XXX)
    tasks = extract_tasks_from_file(content)
    
    print(f"Found {len(tasks)} tasks to import\n")
    
    for task_data in tasks:
        create_clickup_task(task_data)
        # Rate limiting: ClickUp allows 100 requests/min
        import time
        time.sleep(0.6)  # ~100 requests/min
    
    print(f"\n✅ Import complete! {len(tasks)} tasks created.")

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print("Usage: python export-to-clickup.py <sprint-tasks-file>")
        sys.exit(1)
    
    main(sys.argv[1])
```

### Uso

```bash
# Instala dependencias
pip install requests python-dotenv markdown

# Ejecuta script
python scripts/export-to-clickup.py sprint-1-tasks.md
```

### Output Esperado

```
📋 Importing tasks from sprint-1-tasks.md...
Found 11 tasks to import

✅ Created: Implement Create Order API Endpoint (ID: 8abc1234)
✅ Created: Implement Order Domain Model and Validation (ID: 8abc1235)
✅ Created: Implement Order Repository and Database Schema (ID: 8abc1236)
...
✅ Import complete! 11 tasks created.
```

### Ventajas

✅ Muy rápido (segundos vs minutos)  
✅ Sin errores humanos  
✅ Repetible para futuros sprints  
✅ Puede automatizarse en CI/CD  

### Desventajas

❌ Requiere configuración inicial (API token, IDs)  
❌ Necesita conocimiento técnico básico (Python, APIs)  
❌ Rate limits de ClickUp API (100 req/min)  

---

## 📄 Método 3: CSV Import

**Mejor para**: Importación ocasional, equipos no técnicos, cuando API no es opción.

### Generación de CSV

Copilot puede generar CSV a partir de las tareas aprobadas:

```
Usuario: Copilot, genera CSV para importar tareas de sprint 1 a ClickUp

Copilot: [Genera sprint-1-tasks.csv]
```

**Formato CSV**:

```csv
Name,Description,Priority,Story Points,Related US,Epic,Service,Status,Tags
"Implement Create Order API Endpoint","[Description completa en formato texto]",High,5,US-001,Order Management,orders-api,To Do,"sprint-1,backend,api"
"Implement Order Domain Model","[Description...]",High,3,US-001,Order Management,orders-api,To Do,"sprint-1,backend,domain"
...
```

### Importación en ClickUp

1. **Ve a tu List en ClickUp**
2. **Click en "..." → Import/Export → Import**
3. **Sube el archivo CSV**
4. **Mapea columnas**:
   - Name → Task Name
   - Description → Description
   - Priority → Priority
   - Story Points → Custom Field "Story Points"
   - Related US → Custom Field "Related US"
   - Epic → Custom Field "Epic"
   - Service → Custom Field "Service"
   - Status → Status
   - Tags → Tags

5. **Revisa preview** antes de confirmar
6. **Click en "Import"**

### Limitaciones de CSV

⚠️ **Formato limitado**:
- Description se importa como texto plano (sin Markdown rendering)
- Checklist no se importa automáticamente
- Links pueden no funcionar correctamente
- Pérdida de formato visual (emojis, headers)

**Workaround**: Después de importar, edita manualmente las primeras 2-3 tareas para agregar checklist y mejorar formato. El equipo puede hacer lo mismo con las que van a trabajar.

### Ventajas

✅ No requiere conocimiento técnico avanzado  
✅ Interfaz GUI familiar  
✅ Más rápido que manual copy-paste  

### Desventajas

❌ Pierde formato Markdown  
❌ Checklist no se importa  
❌ Requiere limpieza post-importación  

---

## 🔄 Post-Importación: Checklist

Después de crear las tareas en ClickUp (cualquier método):

### Verificación

- [ ] Todas las tareas fueron creadas (contar y comparar)
- [ ] Priorities están correctas (🔴 → Urgent, etc.)
- [ ] Story Points asignados
- [ ] Related US vinculadas
- [ ] Epic y Service configurados
- [ ] Descriptions completas (especialmente ACs)
- [ ] Checklist creado (si usaste CSV, agregar manualmente)

### Organización

- [ ] Ordena tareas por prioridad en la vista de List
- [ ] Crea Board view agrupado por Status
- [ ] Configura Timeline view por Story Points
- [ ] Agrega tareas al Sprint (si usas Sprints feature de ClickUp)

### Comunicación

- [ ] Notifica al equipo que las tareas están listas
- [ ] Comparte link a la List en Slack/Teams
- [ ] Agenda Sprint Planning meeting
- [ ] Prepara demo de tareas para el kickoff

### Documentación

- [ ] Actualiza `BACKLOG.md`: Marca US como "In Progress"
- [ ] Crea `docs/sprints/sprint-X.md` con resumen:
   ```markdown
   # Sprint X - 2025-11-18 to 2025-12-01
   
   ## Goals
   - Implementar creación de pedidos básica
   - Setup de infraestructura de eventos
   
   ## User Stories
   - US-001: Creación de Pedido Básico (13 pts)
   - US-002: Procesamiento de Pagos (8 pts)
   
   ## Tasks
   - Total: 11 tareas
   - Total Story Points: 26 pts
   - [Link a ClickUp List]
   
   ## Team Capacity
   - 3 developers × 2 weeks × 6 pts/week = 36 pts capacity
   - Planned: 26 pts (72% capacity)
   ```

---

## 🎯 Recomendación por Escenario

| Escenario | Método Recomendado | Razón |
|-----------|-------------------|-------|
| Primera vez configurando | **Manual (Copy-Paste)** | Aprender el proceso, ajustar custom fields |
| Sprint pequeño (< 5 tareas) | **Manual (Copy-Paste)** | Rápido y sin overhead de setup |
| Sprint medio (5-15 tareas) | **CSV Import** | Balance entre velocidad y simplicidad |
| Sprint grande (> 15 tareas) | **API Script** | Ahorra mucho tiempo, vale la pena el setup |
| Sprints recurrentes | **API Script** | Automatización full, reutilizable |
| Equipo no técnico | **CSV Import** | No requiere programación |
| Equipo técnico | **API Script** | Control total, extensible |

---

## 🛠️ Scripts y Automatización Avanzada

### GitHub Actions Integration

Puedes automatizar la creación de tareas en ClickUp cuando se aprueba un sprint:

```yaml
# .github/workflows/create-sprint-tasks.yml

name: Create Sprint Tasks in ClickUp

on:
  workflow_dispatch:
    inputs:
      sprint_file:
        description: 'Sprint tasks file (e.g., sprint-1-tasks.md)'
        required: true

jobs:
  create-tasks:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          pip install requests python-dotenv markdown
      
      - name: Create tasks in ClickUp
        env:
          CLICKUP_API_TOKEN: ${{ secrets.CLICKUP_API_TOKEN }}
          CLICKUP_LIST_ID: ${{ secrets.CLICKUP_LIST_ID }}
        run: |
          python scripts/export-to-clickup.py ${{ github.event.inputs.sprint_file }}
```

### Webhooks para Sincronización

Configura webhooks en ClickUp para sincronizar cambios de estado:

```python
# scripts/clickup-webhook-listener.py

from flask import Flask, request
import os

app = Flask(__name__)

@app.route('/clickup-webhook', methods=['POST'])
def handle_webhook():
    event = request.json
    
    if event['event'] == 'taskStatusUpdated':
        task_id = event['task_id']
        new_status = event['history_items'][0]['after']['status']
        
        # Actualiza docs/sprints/sprint-X.md automáticamente
        update_sprint_doc(task_id, new_status)
    
    return '', 200

if __name__ == '__main__':
    app.run(port=5000)
```

---

## 📊 Métricas y Tracking

### KPIs para Medir Efectividad

1. **Time to ClickUp**: Tiempo de tareas aprobadas → creadas en ClickUp
   - **Meta**: < 30 minutos con API, < 2 horas manual

2. **Task Clarity Score**: Preguntas/clarificaciones durante implementación
   - **Meta**: < 2 preguntas por tarea

3. **AC Completeness**: % de ACs marcados como done al finalizar tarea
   - **Meta**: 100% (si < 100%, los ACs estaban incompletos o mal definidos)

4. **Import Error Rate**: % de tareas con errores al importar
   - **Meta**: 0% (si > 0%, revisar script o formato CSV)

---

## 🆘 Troubleshooting

### Problema: API Token no funciona

**Síntomas**: `401 Unauthorized` al ejecutar script

**Soluciones**:
- Verifica que el token esté correcto (copia completo desde ClickUp)
- Asegúrate de tener permisos en el Workspace
- Regenera token si es necesario

### Problema: Custom Fields no se llenan

**Síntomas**: Tareas creadas pero campos vacíos

**Soluciones**:
- Verifica Custom Field IDs con `GET /list/{list_id}/field`
- Asegúrate de que los nombres coincidan exactamente
- Revisa que el tipo de dato sea correcto (Number para story points, etc.)

### Problema: CSV importa mal las descripciones

**Síntomas**: Descriptions cortadas o con caracteres raros

**Soluciones**:
- Exporta CSV con encoding UTF-8
- Escapa comillas dobles en el contenido (`""`)
- Usa método API si CSV sigue fallando

### Problema: Rate Limiting de ClickUp API

**Síntomas**: `429 Too Many Requests`

**Soluciones**:
- Agrega delay entre requests (0.6s = ~100 req/min)
- Usa batch create si ClickUp lo soporta
- Divide importación en múltiples runs

---

## 📚 Recursos Adicionales

- **ClickUp API Docs**: https://clickup.com/api
- **Task Template**: `/docs/task-template.md`
- **Flujo completo**: `/docs/guides/idea-to-task-flow.md`
- **Copilot Instructions**: `/.github/copilot-instructions.md`

---

## ✅ Checklist de Integración Exitosa

Antes de considerar la integración completa:

- [ ] Has creado al menos un sprint manualmente para entender el proceso
- [ ] Custom fields configurados en ClickUp
- [ ] Script de API probado con 1-2 tareas de prueba
- [ ] Equipo entrenado en cómo usar las tareas (checklists, ACs, recommendations)
- [ ] Proceso documentado en este archivo
- [ ] Backups de tareas (archivo generado guardado en `docs/sprints/`)
- [ ] Métricas definidas para medir efectividad

---

**Última actualización**: 2025-11-14  
**Próxima revisión**: Después del primer sprint usando este proceso
