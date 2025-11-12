# VotV Points Editor - Version 0.9.0 Alpha

Editor de puntos para **Voices of the Void Alpha 0.9.0** ✅ **FUNCIONAL**

## ✅ Estado: COMPLETAMENTE FUNCIONAL

**¡RESUELTO!** El offset de los puntos en VotV 0.9.0 fue descubierto y confirmado.

- **Offset**: `0x0000071a`
- **Tipo**: `IntProperty` (4 bytes, little-endian)
- **Propiedad**: `"Points"`
- **Probado hasta**: 2,000,000 puntos ✅

![2 millones de puntos funcionando](https://img.shields.io/badge/Tested-2M_points-success)

---

## 🚀 Uso Rápido

### Modificar puntos

```bash
python set_puntos.py 50000
```

**Ejemplos:**

```bash
# 50,000 puntos
python set_puntos.py 50000

# 500 puntos
python set_puntos.py 500

# 2 millones (probado y funcional)
python set_puntos.py 2000000
```

---

## 📋 Características

✅ Modifica `data.sav` (perfil global)  
✅ Modifica todos los archivos de partida `s_*.sav`  
✅ Crea backups automáticos en `SaveGames/backups/`  
✅ Verifica cambios antes de escribir  
✅ Soporte para valores de 0 hasta 2,000,000+ puntos

---

## ⚙️ Cómo Funciona

### Descubrimiento del Offset

El offset de los puntos en VotV 0.9.0 fue descubierto mediante:

1. **Comparación de saves**: Se compararon dos archivos con diferentes cantidades de puntos (52 vs duplicado)
2. **Búsqueda de contexto**: Se buscó la propiedad `"Points"` en el archivo binario
3. **Validación**: Se confirmó que el offset `0x0000071a` contiene el valor correcto
4. **Pruebas exhaustivas**: Se probaron valores desde 500 hasta 2,000,000 puntos

### Estructura del Save

```
Offset 0x000006f6: "Points\x00"
Offset 0x00000701: "IntProperty"
Offset 0x0000071a: [4 bytes] Valor de los puntos (little-endian)
                    ^^^^^^^^
                    ESTE ES EL OFFSET CORRECTO
```

---

## 🔧 Scripts Disponibles

### `set_puntos.py` ⭐ (Principal)

Modifica los puntos en `data.sav` y todos los archivos `s_*.sav`

```bash
python set_puntos.py <cantidad_puntos>
```

**Salida:**
```
======================================================================
  VotV Points Editor - Version 0.9.0 ALPHA
======================================================================
  Puntos a establecer: 50,000
  Directorio: C:\Users\...\SaveGames
  Offset: 0x0000071a
======================================================================

[1] Modificando data.sav (perfil global)...
  [BACKUP] data.sav.backup_20251112_135012
  [OK] data.sav: 62 -> 50000

[2] Modificando archivos de partida individuales (3 encontrados)...
  [BACKUP] s_09colege.sav.backup_20251112_135012
  [OK] s_09colege.sav: 62 -> 50000
  [BACKUP] s_09colege_0.sav.backup_20251112_135013
  [OK] s_09colege_0.sav: 52 -> 50000
  [BACKUP] s_testpoints.sav.backup_20251112_135013
  [OK] s_testpoints.sav: 107 -> 50000

  Total: 3 modificados, 0 omitidos

======================================================================
  PROCESO COMPLETADO
======================================================================

  Los backups se guardaron en:
  C:\Users\...\SaveGames\backups

  Carga el juego para verificar los cambios
======================================================================
```

---

## 📂 Estructura del Proyecto

```
v0.9.0-alpha/
│
├── set_puntos.py              # ⭐ Script principal (FUNCIONAL)
├── README.md                  # Este archivo
│
└── investigacion/             # Scripts de investigación
    ├── buscar_valor_107.py
    ├── buscar_52_con_contexto.py
    ├── modificar_todos_los_52.py
    ├── investigar_v09.py
    ├── comparar_saves.py
    ├── buscar_cambio_107_109.py
    ├── analizar_contexto_puntos.py
    ├── comparar_colege_62pts.py
    ├── buscar_points_manual.py
    ├── modificar_points_offset_exacto.py
    └── INVESTIGACION.md       # Documentación del proceso
```

---

## 🔍 Proceso de Investigación

El descubrimiento del offset tomó múltiples intentos:

1. ❌ Búsqueda inicial falló (offset incorrecto)
2. ❌ Modificación de 107 a 5000 corrompió el save
3. ✅ Comparación de saves con 52 puntos encontró 356 ocurrencias
4. ✅ Búsqueda de contexto identificó 2 candidatos con "Points" cerca
5. ✅ Prueba con 500 puntos en offset `0x0000071a` funcionó
6. ✅ Confirmación con 2,000,000 puntos exitosa

Ver [`investigacion/INVESTIGACION.md`](investigacion/INVESTIGACION.md) para detalles técnicos completos.

---

## 🛡️ Backups

Todos los archivos modificados se respaldan automáticamente:

**Ubicación**: `C:\Users\TU_USUARIO\AppData\Local\VotV\Saved\SaveGames\backups\`

**Formato**: `archivo.sav.backup_YYYYMMDD_HHMMSS`

### Restaurar un Backup

```bash
# PowerShell
copy "SaveGames\backups\s_09colege_0.sav.backup_20251112_135013" "SaveGames\s_09colege_0.sav"
```

---

## ⚠️ Limitaciones Conocidas

- ✅ Valores hasta **2,000,000** confirmados funcionales
- ⚠️ Valores superiores no han sido probados
- ⚠️ Valores negativos no están permitidos

---

## 🤝 Contribuciones

Si encuentras problemas o mejoras:

1. Prueba con diferentes cantidades de puntos
2. Verifica si funciona con otros saves
3. Reporta en [GitHub Issues](https://github.com/JackStar6677-1/VotV-Points-Editor/issues)

---

## 📝 Changelog

**12 de Noviembre de 2025**:
- ✅ **DESCUBIERTO** el offset correcto: `0x0000071a`
- ✅ Script principal `set_puntos.py` creado y probado
- ✅ Confirmado funcionamiento con 500, 10K, 50K, 500K, 2M puntos
- ✅ Backups automáticos implementados
- ✅ Documentación completa del proceso

---

**Estado**: ✅ Completamente funcional  
**Última actualización**: 12 de noviembre de 2025  
**Contribuciones**: Bienvenidas en [GitHub](https://github.com/JackStar6677-1/VotV-Points-Editor)
