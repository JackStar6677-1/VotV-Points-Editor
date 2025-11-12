# VotV Points Editor - Versión 0.9.0 Alpha (EXPERIMENTAL)

Editor de puntos para **Voices of the Void Alpha 0.9.0** - EN DESARROLLO

## ⚠️ Estado: EXPERIMENTAL / NO FUNCIONAL

**IMPORTANTE**: Esta versión es **EXPERIMENTAL** y actualmente **NO funciona completamente**.

### 🔍 Problema Conocido

La versión 0.9.0 alpha (UNSTABLE) de Voices of the Void cambió la estructura de guardado:

- ✅ `data.sav` se puede modificar (mismo formato que 0.8.x)
- ❌ Los archivos de partida (`s_*.sav`) tienen estructura desconocida
- ❌ Los puntos NO se reflejan en el juego al cargar partidas

### 📊 Investigación en Curso

Estamos investigando cómo se almacenan los puntos en los archivos de save de 0.9.0 alpha.

**Lo que sabemos**:
- Los archivos de partida de v0.9 NO tienen la propiedad `Points` que existía en v0.8
- El formato de serialización cambió completamente
- Posiblemente usan un sistema diferente de almacenamiento de datos

**Lo que necesitamos descubrir**:
- Dónde están los puntos en los archivos `s_*.sav` de v0.9
- Cómo se serializan las propiedades en el nuevo formato
- Si el juego lee desde `data.sav` o desde los archivos individuales

## 🧪 Script Experimental

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

## 🤝 ¿Puedes Ayudar?

Si tienes conocimientos de:
- Ingeniería inversa de formatos de guardado
- Unreal Engine save files
- Serialización binaria

¡Tu ayuda sería muy valiosa! Abre un issue en GitHub con cualquier descubrimiento.

## 💡 Solución Temporal

**Si quieres usar el editor de puntos**:
1. Descarga VotV Alpha 0.8.2c (versión estable anterior)
2. Usa la versión del editor en la carpeta `v0.8.x/`
3. Funciona perfectamente con 0.8.x

## 📝 Para Desarrolladores

Si quieres investigar la estructura de v0.9:

```bash
# Los archivos de save están en:
C:\Users\TU_USUARIO\AppData\Local\VotV\Saved\SaveGames\

# Archivos clave:
- data.sav (global, modificable)
- s_*.sav (archivos de partida v0.9, estructura desconocida)
```

Herramientas útiles:
- Hex editor (HxD, 010 Editor)
- UE4 Save Game readers
- Binary diff tools

## 🔙 Recomendación

**Por ahora, usa la versión 0.8.x del editor** que funciona perfectamente.

Ver [v0.8.x/README.md](../v0.8.x/README.md)

---

**Estado actualizado**: 12 de noviembre de 2025  
**Contribuciones**: Bienvenidas en [GitHub Issues](https://github.com/JackStar6677-1/VotV-Points-Editor/issues)

