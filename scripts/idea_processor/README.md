# Idea Processor - Automated Workflow

> **Automatiza la conversión de ideas en historias de usuario con validación de duplicados**

Este sistema automatiza el flujo descrito en el problema: lee ideas del archivo `IDEAS.md`, valida si son duplicadas o similares a historias de usuario existentes en `BACKLOG.md`, marca las duplicadas, y genera historias de usuario formales para las ideas únicas.

## 🎯 Características

- ✅ **Detección de Duplicados**: Usa embeddings de OpenAI para detectar similitudes semánticas
- ✅ **Generación Automática**: Convierte ideas en historias de usuario siguiendo el template del proyecto
- ✅ **Marcado Automático**: Marca ideas duplicadas en `IDEAS.md` con referencia a la US similar
- ✅ **Actualización de Backlog**: Agrega automáticamente nuevas US a `BACKLOG.md`
- ✅ **Modo Preview**: Opción `--dry-run` para ver cambios sin modificar archivos
- ✅ **Interface Rica**: Output con colores y tablas usando Rich

## 📋 Requisitos

### Software
- Python 3.10 o superior
- pip (gestor de paquetes de Python)
- Cuenta de OpenAI con API key

### Credenciales
- **OpenAI API Key**: Necesaria para detección de similitud y generación de historias

## 🚀 Instalación

### 1. Instalar Dependencias

```bash
# Desde el directorio raíz del proyecto
cd /home/runner/work/architecture-base/architecture-base

# Instalar dependencias del script
pip install -r scripts/idea_processor/requirements.txt
```

### 2. Configurar OpenAI API Key

```bash
# Opción 1: Variable de entorno (recomendado)
export OPENAI_API_KEY='sk-your-api-key-here'

# Opción 2: Crear archivo .env en el directorio raíz
echo "OPENAI_API_KEY=sk-your-api-key-here" > .env
```

Para obtener tu API key:
1. Visita https://platform.openai.com/api-keys
2. Crea una nueva API key
3. Copia el valor y configúralo como variable de entorno

## 📖 Uso

### Comando Básico

```bash
# Procesar ideas y actualizar archivos
python -m scripts.idea_processor.cli
```

### Modo Preview (Dry Run)

```bash
# Ver qué cambios se harían sin modificar archivos
python -m scripts.idea_processor.cli --dry-run
```

### Opciones Avanzadas

```bash
# Ajustar umbral de similitud (default: 0.80 = 80%)
python -m scripts.idea_processor.cli --threshold 0.85

# Modo verbose para debugging
python -m scripts.idea_processor.cli --verbose

# Combinar opciones
python -m scripts.idea_processor.cli --dry-run --threshold 0.85 --verbose
```

### Ayuda

```bash
python -m scripts.idea_processor.cli --help
```

## 🔄 Flujo de Trabajo

### Diagrama del Proceso

```
┌─────────────┐
│  IDEAS.md   │
│  (Captura)  │
└──────┬──────┘
       │
       ▼
┌─────────────────────────────────┐
│  1. Parse Ideas & User Stories  │
└──────┬──────────────────────────┘
       │
       ▼
┌─────────────────────────────────┐
│  2. Check Similarity with AI    │
│     - Use embeddings            │
│     - Compare semantically      │
└──────┬──────────────────────────┘
       │
       ├─────────────┬──────────────┐
       ▼             ▼              ▼
  ┌─────────┐  ┌─────────┐   ┌──────────┐
  │Duplicate│  │Duplicate│   │  Unique  │
  │ (US-XX) │  │ (ID-XX) │   │   Idea   │
  └────┬────┘  └────┬────┘   └────┬─────┘
       │            │              │
       ▼            ▼              ▼
  ┌──────────────────────┐   ┌─────────────────┐
  │ Mark as Duplicate    │   │ Generate US     │
  │ in IDEAS.md          │   │ using GPT-4     │
  └──────────────────────┘   └────┬────────────┘
                                   │
                                   ▼
                            ┌──────────────────┐
                            │ Append to        │
                            │ BACKLOG.md       │
                            └──────────────────┘
                                   │
                                   ▼
                            ┌──────────────────┐
                            │ Mark as          │
                            │ Converted in     │
                            │ IDEAS.md         │
                            └──────────────────┘
```

### Paso a Paso

1. **Carga de Archivos**
   - Lee `IDEAS.md` y parsea todas las ideas
   - Lee `BACKLOG.md` y parsea todas las historias de usuario existentes

2. **Filtrado**
   - Identifica ideas con estado "💭 Por refinar"
   - Estas son las ideas candidatas para procesamiento

3. **Detección de Duplicados**
   - Para cada idea candidata:
     - Genera embedding (vector) del texto completo
     - Compara con embeddings de todas las US existentes
     - Compara con otras ideas
     - Si similitud > threshold (default 80%):
       - Usa GPT-4 para análisis semántico detallado
       - Obtiene score de similitud y razón
       - Marca como duplicada si score > threshold

4. **Generación de User Stories**
   - Para cada idea única (no duplicada):
     - Usa GPT-4 para generar historia de usuario formal
     - Sigue el formato del template (`docs/backlog-template.md`)
     - Genera: título, Como/Quiero/Para, criterios de aceptación, estimación, etc.
     - Asigna ID secuencial (US-XXX)

5. **Actualización de Archivos**
   - **IDEAS.md**:
     - Marca duplicadas: `**Estado**: ⚠️ Repetida - Similar a US-XXX (similitud: 85%)`
     - Marca convertidas: `**Estado**: ✅ Convertida a US-XXX`
   - **BACKLOG.md**:
     - Agrega nuevas US en la sección de prioridad correspondiente
     - Mantiene formato y estructura existente

## 📁 Estructura del Código

```
scripts/idea_processor/
├── __init__.py           # Package init
├── cli.py                # Command-line interface
├── config.py             # Configuration settings
├── models.py             # Data models (Idea, UserStory, etc.)
├── parser.py             # Markdown parser
├── similarity.py         # Similarity checker with OpenAI
├── generator.py          # User story generator
├── processor.py          # Main workflow orchestrator
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## ⚙️ Configuración

### Archivo `config.py`

Puedes ajustar la configuración editando `scripts/idea_processor/config.py`:

```python
class Config(BaseModel):
    # Paths (auto-detectados)
    repo_root: Path
    ideas_file: Path
    backlog_file: Path
    
    # OpenAI
    openai_model: str = "gpt-4o"
    embedding_model: str = "text-embedding-3-small"
    
    # Similarity threshold
    similarity_threshold: float = 0.80  # 80%
    
    # Output
    verbose: bool = True
    dry_run: bool = False
```

### Variables de Entorno

Puedes usar un archivo `.env` en el directorio raíz:

```bash
# .env
OPENAI_API_KEY=sk-your-api-key-here
```

## 📊 Output Ejemplo

### Preview Mode (--dry-run)

```
🚀 Idea Processor Initialized

⚠️  Running in DRY RUN mode - no files will be modified

Step 1: Loading files...

Step 2: Parsing ideas and user stories...

✓ Found 6 ideas
✓ Found 10 existing user stories

📝 Ideas to process: 6

Step 3: Checking for duplicates...

Checking ID-001: Dashboard de Métricas en Tiempo Real
  ✓ Unique idea

Checking ID-002: Sistema de Retry Inteligente para Eventos
  ⚠️  Duplicate found - Similar to US-003 (score: 0.87)
  └─ Reason: Ambas tratan sobre manejo de eventos fallidos...

...

┌──────────────────────────────────────────────────┐
│          ⚠️  Duplicate Ideas Found               │
├──────────┬──────────────────────┬────────────────┤
│ Idea ID  │ Title                │ Similar To     │
├──────────┼──────────────────────┼────────────────┤
│ ID-002   │ Sistema de Retry...  │ US-003  (87%)  │
└──────────┴──────────────────────┴────────────────┘

Step 4: Generating user stories from 5 unique ideas...

Generating user story for ID-001...
  ✓ Generated US-011: Dashboard de Métricas en Tiempo Real

...

┌────────────────────────────────────────────────────┐
│          ✨ Generated User Stories                 │
├───────┬──────────────────────┬──────────┬─────────┤
│ US ID │ Title                │ Priority │ Points  │
├───────┼──────────────────────┼──────────┼─────────┤
│US-011 │ Dashboard de Mét...  │ Alta 🔴  │   8     │
│US-012 │ Versionado Auto...   │ Media 🟡 │   5     │
└───────┴──────────────────────┴──────────┴─────────┘

┌──────────────────────────────────────────────────┐
│                    Summary                        │
├──────────────────────────────────────────────────┤
│ 📊 Processing Complete!                          │
│                                                   │
│ Duplicate Ideas Found: 1                         │
│ New User Stories Generated: 5                    │
│                                                   │
│ Next Steps:                                      │
│ 1. Review generated user stories in BACKLOG.md  │
│ 2. Check marked duplicate ideas in IDEAS.md     │
│ 3. Refine user stories as needed                │
└──────────────────────────────────────────────────┘

Note: This was a dry run. No files were modified.
Run without --dry-run to apply changes.
```

## 🧪 Testing

### Test Manualmente

1. **Dry Run First**
   ```bash
   python -m scripts.idea_processor.cli --dry-run
   ```

2. **Verificar Output**
   - Revisa que las ideas detectadas como duplicadas sean correctas
   - Verifica que las historias generadas tengan sentido

3. **Aplicar Cambios**
   ```bash
   python -m scripts.idea_processor.cli
   ```

4. **Verificar Archivos**
   ```bash
   # Ver cambios en IDEAS.md
   git diff IDEAS.md
   
   # Ver cambios en BACKLOG.md
   git diff BACKLOG.md
   ```

### Test con Ideas de Ejemplo

El script funciona con las ideas existentes en `IDEAS.md`. Puedes agregar ideas de prueba:

```markdown
### [ID-999] Test Idea

- **Contexto**: Testing del sistema
- **Problema**: Validar el flujo automatizado
- **Valor**: Asegurar que funciona correctamente
- **Fecha**: 2025-11-14
- **Estado**: 💭 Por refinar
```

## 🔧 Troubleshooting

### Error: "OpenAI API key not found"

**Solución**: Asegúrate de que la variable de entorno esté configurada:
```bash
export OPENAI_API_KEY='sk-your-key-here'
```

### Error: "File not found: IDEAS.md"

**Solución**: Ejecuta el script desde el directorio raíz del proyecto:
```bash
cd /path/to/architecture-base
python -m scripts.idea_processor.cli
```

### Error: "Module not found"

**Solución**: Instala las dependencias:
```bash
pip install -r scripts/idea_processor/requirements.txt
```

### Similitud incorrecta

**Solución**: Ajusta el threshold:
```bash
# Más estricto (menos falsos positivos)
python -m scripts.idea_processor.cli --threshold 0.90

# Menos estricto (más sensible)
python -m scripts.idea_processor.cli --threshold 0.75
```

## 💰 Costos de OpenAI

### Estimación por Ejecución

Para procesar **6 ideas**:

- **Embeddings**: ~$0.001 por idea × 6 = $0.006
- **GPT-4 para similitud**: ~$0.01 por comparación × 6 = $0.06
- **GPT-4 para generación de US**: ~$0.02 por US × 5 = $0.10

**Total estimado**: ~$0.17 por ejecución

### Optimización de Costos

1. **Usar --dry-run primero**: Valida la lógica sin gastar en generación
2. **Ajustar threshold**: Evita comparaciones innecesarias
3. **Procesar por lotes**: Agrupa ideas para procesar menos frecuentemente

## 🔐 Seguridad

### Buenas Prácticas

1. **No commitar API keys**:
   ```bash
   # Agrega .env al .gitignore
   echo ".env" >> .gitignore
   ```

2. **Usar variables de entorno**:
   - Mejor que hardcodear en código
   - Fácil de rotar

3. **Limitar permisos de API key**:
   - En OpenAI dashboard, limita la API key a solo los modelos necesarios

## 📚 Recursos Relacionados

- [BACKLOG.md](../../BACKLOG.md) - Backlog del proyecto
- [IDEAS.md](../../IDEAS.md) - Archivo de ideas
- [docs/backlog-template.md](../../docs/backlog-template.md) - Template de US
- [docs/guides/idea-to-task-flow.md](../../docs/guides/idea-to-task-flow.md) - Flujo completo

## 🤝 Contribuir

Para agregar features o mejorar el script:

1. Crea una branch
2. Implementa cambios en `scripts/idea_processor/`
3. Prueba con `--dry-run`
4. Actualiza este README si es necesario
5. Crea PR

## 📝 Changelog

### v1.0.0 (2025-11-14)
- Implementación inicial
- Detección de duplicados con embeddings
- Generación automática de user stories
- CLI con rich output
- Modo dry-run

## 📄 Licencia

Este script es parte del proyecto architecture-base y sigue la misma licencia del proyecto principal.
