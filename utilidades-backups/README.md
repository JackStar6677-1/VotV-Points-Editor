# Utilidades de Manejo de Backups

Scripts para gestionar los backups de saves de **Voices of the Void**.

## 🎯 Características

- ✅ **Detecta automáticamente** el usuario de Windows actual
- ✅ **Funciona en cualquier PC** sin modificar código
- ✅ **Seguro**: Siempre pide confirmación antes de eliminar
- ✅ **Informativo**: Muestra estadísticas y detalles

---

## 📂 Ubicación de Backups

Los scripts buscan automáticamente en:

```
%LOCALAPPDATA%\VotV\Saved\SaveGames\backups\
```

Esto se traduce a:
```
C:\Users\<TU_USUARIO>\AppData\Local\VotV\Saved\SaveGames\backups\
```

---

## 🛠️ Scripts Disponibles

### 1. `listar_backups.py`

Lista todos los backups disponibles con información detallada.

```bash
python listar_backups.py
```

**Muestra:**
- Archivos originales con sus backups
- Fecha y hora de cada backup
- Tamaño de cada archivo
- Marca el backup más reciente

**Salida de ejemplo:**
```
======================================================================
  BACKUPS DISPONIBLES
======================================================================

Directorio: C:\Users\TuUsuario\AppData\Local\VotV\Saved\SaveGames\backups
Total de archivos originales: 3
Total de backups: 12

======================================================================

[data.sav] - 5 backup(s)
----------------------------------------------------------------------
  1. 20251112_140534
     Fecha: 2025-11-12 14:05:34  [MAS RECIENTE]
     Tamaño: 145.2 KB
     Ruta: data.sav.backup_20251112_140534

  2. 20251112_135012
     Fecha: 2025-11-12 13:50:12
     Tamaño: 145.1 KB
     Ruta: data.sav.backup_20251112_135012

[s_09colege_0.sav] - 4 backup(s)
----------------------------------------------------------------------
  ...
```

---

### 2. `restaurar_backup.py`

Restaura un backup específico con menú interactivo.

```bash
python restaurar_backup.py
```

**Funciones:**
- Menú de selección por archivo
- Lista de backups ordenados por fecha
- Confirma antes de restaurar
- Crea backup del archivo actual antes de reemplazar
- Seguro y reversible

**Flujo:**
1. Selecciona el archivo original
2. Selecciona qué backup restaurar
3. Confirma la operación
4. Se crea backup del archivo actual
5. Se restaura el backup seleccionado

**Salida de ejemplo:**
```
======================================================================
  SELECCIONA EL ARCHIVO A RESTAURAR
======================================================================
  1. data.sav
     Backups: 5 | Ultimo: 2025-11-12 14:05:34
  2. s_09colege_0.sav
     Backups: 4 | Ultimo: 2025-11-12 13:46:43

  0. Salir
======================================================================

Selecciona un archivo (numero): 2

======================================================================
  BACKUPS DE: s_09colege_0.sav
======================================================================

  1. 20251112_134643
     Fecha: 2025-11-12 13:46:43  <-- MAS RECIENTE
     Archivo: s_09colege_0.sav.backup_20251112_134643

  2. 20251112_134302
     Fecha: 2025-11-12 13:43:02
     Archivo: s_09colege_0.sav.backup_20251112_134302

  0. Volver al menu anterior
======================================================================

Selecciona un backup (numero): 2

======================================================================
  CONFIRMACION
======================================================================

Vas a restaurar:
  s_09colege_0.sav.backup_20251112_134302
  Fecha: 2025-11-12 13:43:02

Esto reemplazara el archivo actual:
  s_09colege_0.sav

(Se creara un backup del archivo actual antes de restaurar)

Continuar? (s/n): s

[SEGURIDAD] Backup del archivo actual creado:
  s_09colege_0.sav.before_restore_20251112_140823

[EXITO] Backup restaurado correctamente!
  Desde: s_09colege_0.sav.backup_20251112_134302
  Hacia: s_09colege_0.sav
  Fecha del backup: 2025-11-12 13:43:02

[INFO] Puedes verificar cargando el juego
```

---

### 3. `limpiar_backups_antiguos.py`

Elimina backups antiguos para liberar espacio.

```bash
python limpiar_backups_antiguos.py
```

**Opciones:**
1. **Eliminar por antigüedad**: Elimina backups más antiguos que X días
2. **Mantener N más recientes**: Mantiene solo los N backups más recientes por archivo
3. **Eliminar TODOS**: Elimina todos los backups (requiere confirmación doble)
4. **Ver lista detallada**: Muestra todos los backups con detalles

**Muestra estadísticas:**
- Total de backups
- Espacio ocupado
- Backup más antiguo/reciente

**Salida de ejemplo:**
```
======================================================================
  ESTADISTICAS
======================================================================

Total de backups: 42
Espacio total: 5.87 GB
Backup mas antiguo: 2025-11-05 09:15:22
Backup mas reciente: 2025-11-12 14:05:34

======================================================================
  OPCIONES DE LIMPIEZA
======================================================================

  1. Eliminar backups mas antiguos que X dias
  2. Mantener solo los N backups mas recientes (por archivo)
  3. Eliminar TODOS los backups (peligroso)
  4. Ver lista detallada de backups

  0. Salir
======================================================================

Selecciona una opcion: 1

======================================================================
  ELIMINAR POR ANTIGUEDAD
======================================================================

Dias de antiguedad (ej: 7, 14, 30): 7

[INFO] Se encontraron 28 backups mas antiguos que 7 dias
[INFO] Espacio a liberar: 3.92 GB

Backups que seran eliminados:
  1. data.sav.backup_20251105_091522
     Fecha: 2025-11-05 09:15:22
  2. data.sav.backup_20251105_143045
     Fecha: 2025-11-05 14:30:45
  ...
  ... y 26 mas

Eliminar 28 backup(s)? (s/n): s

[EXITO] 28 backup(s) eliminados
[INFO] Espacio liberado: 3.92 GB
```

---

## 💡 Ejemplos de Uso

### Listar todos los backups disponibles

```bash
cd utilidades-backups
python listar_backups.py
```

---

### Restaurar un backup específico

```bash
cd utilidades-backups
python restaurar_backup.py
```

Luego sigue el menú interactivo.

---

### Limpiar backups de más de 30 días

```bash
cd utilidades-backups
python limpiar_backups_antiguos.py
```

Selecciona opción `1` → ingresa `30`

---

### Mantener solo los 5 backups más recientes de cada archivo

```bash
cd utilidades-backups
python limpiar_backups_antiguos.py
```

Selecciona opción `2` → ingresa `5`

---

## 🔒 Seguridad

- ✅ **Siempre pide confirmación** antes de eliminar
- ✅ **Doble confirmación** para operaciones peligrosas
- ✅ **Crea backup antes de restaurar** (archivo `.before_restore_*`)
- ✅ **Muestra qué se va a eliminar** antes de hacerlo
- ✅ **No modifica archivos de save originales** (solo backups)

---

## ⚠️ Notas

### Detección Automática

Los scripts detectan automáticamente el usuario de Windows usando la variable de entorno `%LOCALAPPDATA%`:

```python
import os
localappdata = os.environ.get('LOCALAPPDATA')
saves_dir = os.path.join(localappdata, "VotV", "Saved", "SaveGames")
```

Esto funciona en **cualquier PC con Windows** sin necesidad de modificar el código.

---

### Formato de Backups

Los backups siguen el formato:

```
<archivo_original>.backup_<timestamp>
```

Ejemplo:
```
s_09colege_0.sav.backup_20251112_134643
```

- `s_09colege_0.sav`: Archivo original
- `20251112`: Fecha (YYYYMMDD)
- `134643`: Hora (HHMMSS)

---

## 🚀 Integración con el Editor

Estos scripts están diseñados para trabajar con los backups creados por:

- `v0.8.x/set_puntos.py`
- `v0.9.0-alpha/set_puntos.py`
- `v0.8.x/modificar_puntos.py`
- Cualquier script que use la misma estructura de backups

---

## 📝 Preguntas Frecuentes

### ¿Los scripts funcionan en Linux/Mac?

Actualmente están optimizados para Windows. Para Linux/Mac, cambiar:

```python
# Windows
saves_dir = os.path.join(localappdata, "VotV", "Saved", "SaveGames")

# Linux
saves_dir = os.path.expanduser("~/.config/VotV/Saved/SaveGames")
```

### ¿Puedo recuperar backups eliminados?

No, una vez eliminados con `limpiar_backups_antiguos.py`, no se pueden recuperar. Por eso siempre pide confirmación.

### ¿Los backups afectan el rendimiento del juego?

No, los backups están en una carpeta separada y el juego no los lee.

### ¿Cuánto espacio ocupan los backups?

Depende de cuántos backups tengas. Usa `listar_backups.py` o `limpiar_backups_antiguos.py` para ver estadísticas.

---

## 🛠️ Requisitos

- Python 3.7+
- Windows (para detección automática del usuario)
- Los backups deben estar en la ubicación estándar de VotV

---

**¡Gestiona tus backups de forma segura y eficiente!** 🎮

