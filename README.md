# VotV Points Editor

Editor de puntos para **[Voices of the Void](https://mrdrnose.itch.io/votv)** - Alpha 0.9.0

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.7+-blue.svg)
![Platform](https://img.shields.io/badge/platform-Windows-lightgrey.svg)
![VotV Version](https://img.shields.io/badge/VotV-0.9.0-green.svg)

## 📋 Descripción

Una herramienta simple y segura para modificar los puntos del jugador en Voices of the Void. 

**Actualización importante:** Esta versión corrige el problema donde los puntos no se guardaban correctamente. Ahora modifica tanto `data.sav` como todos los archivos de partida individuales (`s_*.sav`), asegurando que los cambios se reflejen en el juego.

> **Problema corregido:** La versión anterior solo modificaba `data.sav`, pero el juego lee los puntos desde los archivos de partida individuales. Ahora se modifican ambos.

## ✨ Características

- ✅ **Seguro**: Crea backups automáticos antes de cualquier modificación
- ✅ **Completo**: Modifica tanto `data.sav` como TODOS los archivos de partida
- ✅ **Simple**: Un solo comando para modificar tus puntos
- ✅ **Informativo**: Muestra valores actuales y confirma cambios
- ✅ **Sin dependencias**: Solo usa librerías estándar de Python
- ✅ **Multiplataforma**: Funciona en cualquier sistema con Python 3.7+

## 📥 Instalación

### Requisitos previos
- Python 3.7 o superior
- **Voices of the Void Alpha 0.9.0** ([Descargar aquí](https://mrdrnose.itch.io/votv))
  - **IMPORTANTE**: Esta herramienta está diseñada específicamente para la versión 0.9.0 del juego
  - No garantiza compatibilidad con otras versiones

### Pasos

1. Clona este repositorio:
```bash
git clone https://github.com/TU_USUARIO/VotV-Points-Editor.git
cd VotV-Points-Editor
```

2. ¡Listo! No requiere instalación de dependencias adicionales.

## 🚀 Uso

### Método ultra-rápido (Windows)

Doble click en:
- **`PRUEBA_RAPIDA.bat`**: Establece 50,000 puntos automáticamente
- **`VERIFICAR_PUNTOS.bat`**: Muestra los puntos actuales en todos los saves

### Método rápido (Línea de comandos)

```bash
python set_puntos.py <cantidad_de_puntos>
```

**Ejemplos:**
```bash
# Establecer 50,000 puntos
python set_puntos.py 50000

# Establecer 999,999 puntos
python set_puntos.py 999999

# Establecer 2,000,000 puntos
python set_puntos.py 2000000

# Ver valores actuales (sin modificar)
python set_puntos.py
```

### Método interactivo

```bash
python modificar_puntos.py
```

Este método te permite:
1. Ver valores actuales
2. Modificar Total Points
3. Modificar Points Spent
4. Establecer puntos disponibles específicos

## 📖 Cómo funciona

Voices of the Void almacena los puntos en **DOS ubicaciones**:

1. **`data.sav`** (archivo global):
   - **`total_points_42`**: Total de puntos ganados históricamente
   - **`points_spent_43`**: Puntos que ya has gastado
   - Disponibles: `total_points - points_spent`

2. **Archivos de partida individuales** (`s_*.sav`):
   - Cada partida tiene su propia propiedad **`Points`**
   - **Este es el valor que el juego lee cuando cargas una partida**

El script modifica **AMBOS** tipos de archivos para asegurar que los cambios se reflejen correctamente en el juego:
- Ajusta `total_points_42` en `data.sav`
- Actualiza `Points` en todos los archivos de partida (`s_*.sav`)

## 📁 Ubicación del archivo

El archivo `data.sav` se encuentra en:

```
Windows: %LOCALAPPDATA%\VotV\Saved\SaveGames\data.sav
```

Ruta completa típica:
```
C:\Users\TU_USUARIO\AppData\Local\VotV\Saved\SaveGames\data.sav
```

## ⚠️ Precauciones

- **Cierra el juego** antes de modificar los archivos
- **No modifiques** archivos mientras el juego esté abierto
- Los **backups se crean automáticamente** en la carpeta `SaveGames/backups/`
- Si algo sale mal, puedes restaurar el backup manualmente
- **Compatible solo con Voices of the Void Alpha 0.9.0**

## 🔧 Restaurar un backup

Si necesitas restaurar:

1. Cierra el juego
2. Ve a la carpeta `C:\Users\TU_USUARIO\AppData\Local\VotV\Saved\SaveGames\backups\`
3. Copia el backup que deseas restaurar
4. Pégalo en la carpeta superior (`SaveGames`)
5. Renombra el archivo eliminando la parte `.backup_YYYYMMDD_HHMMSS`
6. Inicia el juego

## 🐛 Solución de problemas

### El script no encuentra data.sav

Verifica la ruta. En algunos casos puede estar en:
```
%LOCALAPPDATA%\VotV\Saved\SaveGames\
```

### Los puntos no cambian en el juego

Esta versión corregida debería solucionar este problema. Asegúrate de:
1. Cerrar el juego completamente antes de ejecutar el script
2. El script mostró: "[EXITO] Puntos modificados en todos los saves!"
3. El script indica que modificó archivos de partida (ejemplo: "7 partidas modificadas")
4. Iniciar el juego después de la modificación

Si aún tienes problemas, ejecuta `python buscar_puntos_todos_saves.py` para diagnosticar.

### Error de permisos

Ejecuta PowerShell o CMD como administrador si tienes problemas de permisos.

## 📝 Estructura del proyecto

```
VotV-Points-Editor/
│
├── set_puntos.py                    # Script principal CORREGIDO (línea de comandos)
├── modificar_puntos.py              # Script interactivo con menú (ACTUALIZADO)
├── buscar_puntos_todos_saves.py     # Herramienta de diagnóstico
├── set_puntos_todos_saves.py        # Versión standalone alternativa
├── PRUEBA_RAPIDA.bat                # Prueba rápida: 50,000 puntos (Windows)
├── VERIFICAR_PUNTOS.bat             # Verificar puntos actuales (Windows)
├── SOLUCION_PROBLEMA.md             # Documentación técnica del problema corregido
├── README.md                        # Este archivo
├── LICENSE                          # Licencia MIT
└── .gitignore                       # Archivos a ignorar en git
```

### Scripts disponibles:

**Para Windows (doble click):**
- **`PRUEBA_RAPIDA.bat`**: Establece 50,000 puntos en todas las partidas
- **`VERIFICAR_PUNTOS.bat`**: Analiza y muestra los puntos en todos los archivos

**Línea de comandos:**
- **`set_puntos.py`**: Script principal recomendado (CORREGIDO)
- **`modificar_puntos.py`**: Versión interactiva con menú (ACTUALIZADO)
- **`buscar_puntos_todos_saves.py`**: Herramienta de diagnóstico detallada
- **`set_puntos_todos_saves.py`**: Versión standalone alternativa

## 🤝 Contribuir

Las contribuciones son bienvenidas! Si encuentras un bug o tienes una sugerencia:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📜 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo [LICENSE](LICENSE) para más detalles.

## ⚠️ Disclaimer

Este proyecto es una herramienta de terceros **no oficial**. No está afiliado, asociado, autorizado ni respaldado por mrdrnose o los desarrolladores de Voices of the Void.

**Voices of the Void** y todos sus derechos pertenecen a [mrdrnose](https://mrdrnose.itch.io/votv).

Usa esta herramienta bajo tu propio riesgo. Siempre haz backups de tus archivos de guardado. Esta herramienta está diseñada específicamente para **Voices of the Void Alpha 0.9.0** y puede no funcionar con otras versiones.

## 🎮 Sobre Voices of the Void

**Voices of the Void** es un juego de simulación/horror desarrollado por [mrdrnose](https://mrdrnose.itch.io).

🎮 **Jugar**: [https://mrdrnose.itch.io/votv](https://mrdrnose.itch.io/votv)  
💬 **Discord**: [Servidor oficial](https://discord.gg/votv)  
💰 **Patreon**: [Apoya el desarrollo](https://www.patreon.com/mrdrnose)

## 🙏 Agradecimientos

- [mrdrnose](https://mrdrnose.itch.io) - Desarrollador de Voices of the Void
- Comunidad de Voices of the Void
- Contribuidores del proyecto

## 📞 Contacto

Si tienes preguntas o sugerencias, abre un issue en GitHub.

---

**¡Disfruta tu partida con todos los puntos que necesites!** 🎮✨

