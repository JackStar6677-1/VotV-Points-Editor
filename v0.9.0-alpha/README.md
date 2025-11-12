# VotV Points Editor - Version 0.9.0 Alpha (EXPERIMENTAL)

Editor de puntos para **Voices of the Void Alpha 0.9.0** - EN DESARROLLO

## Estado: EXPERIMENTAL / NO FUNCIONAL

**IMPORTANTE**: Esta version es **EXPERIMENTAL** y actualmente **NO funciona completamente**.

### Problema Conocido

La version 0.9.0 alpha (UNSTABLE) de Voices of the Void cambio la estructura de guardado:

- `data.sav` se puede modificar (mismo formato que 0.8.x)
- Los archivos de partida (`s_*.sav`) tienen estructura desconocida
- Los puntos NO se reflejan en el juego al cargar partidas

### Investigacion en Curso

**HALLAZGO CLAVE**: Se confirmo que la estructura cambio completamente.

**v0.8.x**:
- Propiedad `Points` existe como `IntProperty` en offset predecible
- Modificable directamente

**v0.9.0 alpha**:
- La propiedad `Points` NO EXISTE en el formato de guardado
- La palabra solo aparece en textos descriptivos
- Estructura completamente reorganizada

**Teoria principal**: Los puntos se movieron a:
1. Una estructura compleja (StructProperty anidado)
2. Nombre de variable diferente (Currency, Money, Score)
3. GameInstance en vez de SaveGame
4. Sistema de guardado separado

Ver [INVESTIGACION.md](INVESTIGACION.md) para analisis tecnico completo.

## Script Experimental

### `set_puntos_v09.py`

Este script **SOLO modifica `data.sav`** pero los cambios probablemente **NO se reflejarán** en el juego.

```bash
python set_puntos_v09.py 50000
```

**Salida esperada**:
```
[EXITO] data.sav modificado!

⚠️  ADVERTENCIA: Los archivos de partida de v0.9.0 alpha
    tienen estructura desconocida y NO fueron modificados.
    Los puntos pueden NO reflejarse en el juego.
```

## Puedes Ayudar?

Si tienes conocimientos de:
- Ingeniería inversa de formatos de guardado
- Unreal Engine save files
- Serialización binaria

¡Tu ayuda sería muy valiosa! Abre un issue en GitHub con cualquier descubrimiento.

## Solucion Temporal

**Si quieres usar el editor de puntos**:
1. Descarga VotV Alpha 0.8.2c (versión estable anterior)
2. Usa la versión del editor en la carpeta `v0.8.x/`
3. Funciona perfectamente con 0.8.x

## Herramientas de Investigacion

### investigar_v09.py

Script de analisis que examina la estructura interna de archivos .sav:

```bash
# Analizar archivo de v0.9
python investigar_v09.py

# Analizar archivo especifico
python investigar_v09.py "C:\ruta\al\archivo.sav"

# Comparar con v0.8
python investigar_v09.py "C:\...\s_1.sav"
```

**Que hace**:
- Hexdump de primeros bytes
- Busca strings ASCII relevantes
- Identifica propiedades IntProperty
- Analiza estructura GVAS de Unreal Engine
- Compara patrones entre v0.8 y v0.9

## Para Desarrolladores

**Archivos de save**:
```
C:\Users\TU_USUARIO\AppData\Local\VotV\Saved\SaveGames\
```

**Archivos del juego**:
```
[Instalacion]\WindowsNoEditor\
```

**Herramientas recomendadas**:
- HxD / 010 Editor (hex editors)
- UE4 SaveGame readers
- Cheat Engine (memory scanning)
- Binary diff tools
- UAssetGUI (para archivos .pak)

**Documentacion**:
- [INVESTIGACION.md](INVESTIGACION.md) - Analisis tecnico completo
- [investigar_v09.py](investigar_v09.py) - Script de analisis

## Recomendacion

**Por ahora, usa la versión 0.8.x del editor** que funciona perfectamente.

Ver [v0.8.x/README.md](../v0.8.x/README.md)

---

**Estado actualizado**: 12 de noviembre de 2025  
**Contribuciones**: Bienvenidas en [GitHub Issues](https://github.com/JackStar6677-1/VotV-Points-Editor/issues)

