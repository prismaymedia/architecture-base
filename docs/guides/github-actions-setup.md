# 🤖 GitHub Actions - Procesamiento Automático de Ideas

## Resumen

Este workflow de GitHub Actions procesa automáticamente las ideas agregadas a `IDEAS.md` cada vez que se hace push a la rama `master`, utilizando Google Gemini AI para detectar duplicados y generar historias de usuario.

## ⚡ Setup Rápido (3 pasos)

### 1. Obtener Gemini API Key

1. Visita https://aistudio.google.com/app/apikey
2. Click en "Create API Key"
3. Copia la API key generada

### 2. Configurar Secret en GitHub

1. Ve a tu repositorio: `https://github.com/prismaymedia/architecture-base`
2. Click en **Settings** (pestaña superior)
3. En el menú lateral: **Secrets and variables** → **Actions**
4. Click en **New repository secret**
5. Configurar:
   - **Name**: `GEMINI_API_KEY`
   - **Secret**: Pega tu API key de Gemini
6. Click en **Add secret**

### 3. Listo - Ya Funciona!

El workflow se ejecutará automáticamente en cada push a `master` que modifique `IDEAS.md`.

## 📋 Cómo Usar

### Agregar Ideas

```bash
# 1. Editar IDEAS.md
vim IDEAS.md

# Agregar nueva idea:
### [ID-008] Mi Nueva Idea

- **Contexto**: Descripción del contexto
- **Problema**: Qué problema resuelve
- **Valor**: Qué valor aporta
- **Fecha**: 2025-11-14
- **Estado**: 💭 Por refinar

# 2. Commit y push
git add IDEAS.md
git commit -m "feat: add idea for feature X"
git push origin master
```

### Ver Ejecución

1. Ve a la pestaña **Actions** en GitHub
2. Click en el workflow "Process Ideas with Gemini AI"
3. Verás el progreso en tiempo real

### Resultados

Después de la ejecución:

- ✅ `IDEAS.md` actualizado con estados (✅ Convertida o ⚠️ Repetida)
- ✅ `BACKLOG.md` actualizado con nuevas user stories
- ✅ Commit automático del bot
- ✅ Resumen en la pestaña Actions

## 🔍 Verificar Cambios

```bash
# Después de que el workflow termine
git pull origin master

# Ver cambios en IDEAS.md
git log -1 --oneline IDEAS.md

# Ver nuevas user stories
git diff HEAD~1 BACKLOG.md
```

## ⚙️ Configuración del Workflow

### Archivo

`.github/workflows/process-ideas-gemini.yml`

### Triggers

El workflow se activa cuando:
- **Branch**: `master` o `main`
- **Archivos modificados**: `IDEAS.md`

### Permisos

```yaml
permissions:
  contents: write      # Para commitear cambios
  pull-requests: write # Para crear PRs (futuro)
```

### Variables de Entorno

```yaml
env:
  GEMINI_API_KEY: ${{ secrets.GEMINI_API_KEY }}
  AI_PROVIDER: gemini
```

## 🛠️ Troubleshooting

### Error: "GEMINI_API_KEY not found"

**Solución**: Verificar que el secret esté configurado correctamente en GitHub Settings.

```bash
# Verifica en: Settings → Secrets → Actions
# Debe existir: GEMINI_API_KEY
```

### El workflow no se ejecuta

**Causas posibles**:
1. No se modificó `IDEAS.md`
2. El push fue a otra rama (debe ser `master` o `main`)
3. El workflow está deshabilitado

**Solución**:
```bash
# Verificar rama actual
git branch

# Asegurarse de estar en master
git checkout master

# Verificar que IDEAS.md cambió
git status
```

### El bot no commitea cambios

**Causa**: No hay ideas nuevas para procesar

**Verificar**: Que las ideas tengan estado `💭 Por refinar`

## 📊 Ejemplo de Ejecución

### Input (IDEAS.md)

```markdown
### [ID-009] Sistema de Caché Redis

- **Contexto**: Consultas repetitivas a la base de datos
- **Problema**: Latencia alta en endpoints de lectura
- **Valor**: Reducir latencia de 500ms a 50ms
- **Fecha**: 2025-11-14
- **Estado**: 💭 Por refinar
```

### Workflow Execution

```
🚀 Idea Processor Initialized (using Gemini AI)

Step 1: Loading files...
✓ Found 9 ideas
✓ Found 11 existing user stories

Step 2: Parsing ideas and user stories...
📝 Ideas to process: 1

Step 3: Checking for duplicates...
Checking ID-009: Sistema de Caché Redis
  ✓ Unique idea

Step 4: Generating user stories...
  ✓ Generated US-012: Implementar Sistema de Caché Redis

Step 5: Updating files...
✓ IDEAS.md updated
✓ BACKLOG.md updated
```

### Output

**IDEAS.md actualizado**:
```markdown
### [ID-009] Sistema de Caché Redis

- **Estado**: ✅ Convertida a US-012
```

**BACKLOG.md actualizado**:
```markdown
#### US-012: Implementar Sistema de Caché con Redis
**Como** desarrollador del sistema
**Quiero** implementar caché con Redis
**Para** reducir latencia de consultas...
```

## 🔐 Seguridad

### Buenas Prácticas

1. ✅ **Nunca** commitear API keys en el código
2. ✅ Usar GitHub Secrets para credenciales
3. ✅ Limitar permisos del workflow al mínimo necesario
4. ✅ Revisar los commits del bot antes de mergear

### Rotar API Key

Si necesitas cambiar la API key:

1. Generar nueva key en Google AI Studio
2. Actualizar secret en GitHub:
   - Settings → Secrets → Actions
   - Click en `GEMINI_API_KEY`
   - Update secret
3. La próxima ejecución usará la nueva key

## 📈 Monitoreo

### Métricas

En la pestaña Actions puedes ver:
- ✅ Tiempo de ejecución (típicamente 1-2 minutos)
- ✅ Ideas procesadas por ejecución
- ✅ User stories generadas
- ✅ Duplicados detectados

### Logs

```bash
# Ver logs detallados
# GitHub → Actions → Select workflow run → View logs
```

## 🚀 Mejoras Futuras

Posibles mejoras al workflow:

1. **Notificaciones**: Enviar notificación cuando se procesen ideas
2. **Pull Requests**: Crear PR en lugar de commit directo
3. **Validación**: Agregar revisión humana antes de aprobar
4. **Métricas**: Dashboard con estadísticas de procesamiento
5. **Múltiples Providers**: Soporte para elegir entre Gemini/OpenAI

## 📚 Recursos

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Google Gemini API](https://ai.google.dev/docs)
- [Workflow File](.github/workflows/process-ideas-gemini.yml)
- [Main README](README.md)

## 💡 Tips

1. **Prueba Local Primero**: Usa `--dry-run` antes de hacer push
   ```bash
   export GEMINI_API_KEY='your-key'
   export AI_PROVIDER='gemini'
   python -m scripts.idea_processor.cli --dry-run
   ```

2. **Batch Ideas**: Agrega múltiples ideas antes de hacer push para procesar en batch

3. **Revisa el Summary**: GitHub Actions genera un resumen útil en cada ejecución

4. **Mantén el Formato**: Asegúrate de que las ideas sigan el formato correcto en IDEAS.md

## ❓ FAQ

**P: ¿Puedo usar OpenAI en lugar de Gemini?**  
R: Sí, modifica el workflow para usar `OPENAI_API_KEY` y `AI_PROVIDER=openai`

**P: ¿El workflow consume muchos créditos de API?**  
R: No, típicamente 1-2 requests por idea (~$0.001 por idea con Gemini)

**P: ¿Puedo ejecutarlo manualmente?**  
R: Sí, en Actions → Select workflow → Run workflow

**P: ¿Funciona con otras ramas?**  
R: Por defecto solo `master/main`, pero puedes modificar el workflow

## 📞 Soporte

Si tienes problemas:
1. Revisa los logs en la pestaña Actions
2. Verifica que el secret esté configurado
3. Prueba localmente primero con `--dry-run`
4. Consulta la documentación completa en `README.md`
