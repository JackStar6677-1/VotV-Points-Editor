# VotV Points Editor

Editor de puntos para **[Voices of the Void](https://mrdrnose.itch.io/votv)**

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.7+-blue.svg)
![Platform](https://img.shields.io/badge/platform-Windows-lightgrey.svg)

## Elige tu Version

Este proyecto esta organizado en dos versiones segun la version de VotV que uses:

### [Version 0.8.x](v0.8.x/) - RECOMENDADO
- **Estado**: TOTALMENTE FUNCIONAL
- **Compatible con**: VotV Alpha 0.8.x (0.8.0, 0.8.1, 0.8.2, etc.)
- **Caracteristicas**: 
  - Modifica `data.sav` y todos los archivos de partida
  - Los cambios se reflejan perfectamente en el juego
  - Incluye scripts .bat para Windows

**[IR A v0.8.x](v0.8.x/)**

### [Version 0.9.0 Alpha](v0.9.0-alpha/) - FUNCIONAL ✅
- **Estado**: COMPLETAMENTE FUNCIONAL
- **Compatible con**: VotV Alpha 0.9.0 (UNSTABLE)
- **Caracteristicas**: 
  - Modifica `data.sav` y todos los archivos de partida
  - Los cambios se reflejan correctamente en el juego
  - Probado hasta 2,000,000 puntos
  - Offset descubierto: 0x0000071a

**[IR A v0.9.0-alpha](v0.9.0-alpha/)**

## Descripcion

Una herramienta simple y segura para modificar los puntos del jugador en Voices of the Void.

**Si tienes VotV 0.8.x** → Usa la [versión 0.8.x](v0.8.x/) que funciona perfectamente.

**Si tienes VotV 0.9.0 alpha** → Usa la [versión 0.9.0-alpha](v0.9.0-alpha/) que ahora funciona completamente.

## Caracteristicas (v0.8.x)

- **Seguro**: Crea backups automaticos antes de cualquier modificacion
- **Completo**: Modifica tanto `data.sav` como TODOS los archivos de partida
- **Simple**: Un solo comando para modificar tus puntos
- **Informativo**: Muestra valores actuales y confirma cambios
- **Sin dependencias**: Solo usa librerias estandar de Python
- **Scripts Windows**: Acceso rapido con doble click (.bat)

## Instalacion

### Requisitos
- Python 3.7 o superior
- **Voices of the Void** ([Descargar aqui](https://mrdrnose.itch.io/votv))

### Pasos

1. Clona este repositorio:
```bash
git clone https://github.com/JackStar6677-1/VotV-Points-Editor.git
cd VotV-Points-Editor
```

2. Elige tu version:
   - **VotV 0.8.x** -> `cd v0.8.x`
   - **VotV 0.9.0 alpha** -> `cd v0.9.0-alpha` (experimental)

3. Listo! No requiere dependencias adicionales.

## Uso Rapido

### Para VotV 0.8.x (RECOMENDADO)

```bash
cd v0.8.x

# Metodo 1: Windows (doble click)
PRUEBA_RAPIDA.bat

# Metodo 2: Linea de comandos
python set_puntos.py 50000
```

**[Documentacion completa v0.8.x](v0.8.x/README.md)**

### Para VotV 0.9.0 alpha (FUNCIONAL ✅)

```bash
cd v0.9.0-alpha

# Script funcional (modifica data.sav y todos los s_*.sav)
python set_puntos.py 50000
```

**CONFIRMADO**: Los cambios se reflejan correctamente en el juego.

**[Documentacion completa v0.9.0](v0.9.0-alpha/README.md)**

## Utilidades de Backups

Scripts para gestionar tus backups de forma segura (funciona con cualquier usuario):

```bash
cd utilidades-backups

# Listar todos los backups
python listar_backups.py

# Restaurar un backup (menu interactivo)
python restaurar_backup.py

# Limpiar backups antiguos
python limpiar_backups_antiguos.py
```

**[Documentacion completa de utilidades](utilidades-backups/README.md)**

## Como funciona (v0.8.x)

Para mas detalles tecnicos, consulta el README de cada version:
- **[Documentacion tecnica v0.8.x](v0.8.x/README.md)**
- **[Estado de investigacion v0.9.0](v0.9.0-alpha/README.md)**

## Ubicacion de archivos

```
C:\Users\TU_USUARIO\AppData\Local\VotV\Saved\SaveGames\
```

Los backups se guardan automaticamente en `SaveGames/backups/`

## Solucion de problemas

Para problemas especificos, consulta el README de tu version:
- **[Solucion de problemas v0.8.x](v0.8.x/README.md)**
- **[Estado y limitaciones v0.9.0](v0.9.0-alpha/README.md)**

### Problemas comunes:

**Error de permisos**: Ejecuta PowerShell o CMD como administrador

**Archivo no encontrado**: Verifica que la ruta sea correcta:
```
%LOCALAPPDATA%\VotV\Saved\SaveGames\
```

## Estructura del proyecto

```
VotV-Points-Editor/
│
├── v0.8.x/                          # VERSION ESTABLE
│   ├── set_puntos.py                   # Script principal
│   ├── modificar_puntos.py             # Script interactivo
│   ├── buscar_puntos_todos_saves.py    # Diagnostico
│   ├── set_puntos_todos_saves.py       # Version alternativa
│   ├── PRUEBA_RAPIDA.bat               # Windows: 50,000 puntos
│   ├── VERIFICAR_PUNTOS.bat            # Windows: Verificar
│   └── README.md                       # Documentacion v0.8.x
│
├── v0.9.0-alpha/                    # VERSION FUNCIONAL ✅
│   ├── set_puntos.py                   # Script principal (FUNCIONAL)
│   ├── README.md                       # Documentacion v0.9.0
│   └── investigacion/                  # Scripts de investigacion
│       ├── buscar_valor_107.py
│       ├── buscar_52_con_contexto.py
│       ├── modificar_todos_los_52.py
│       ├── investigar_v09.py
│       └── INVESTIGACION.md            # Proceso de descubrimiento
│
├── utilidades-backups/              # GESTION DE BACKUPS
│   ├── listar_backups.py               # Listar backups disponibles
│   ├── restaurar_backup.py             # Restaurar backups (interactivo)
│   ├── limpiar_backups_antiguos.py     # Limpiar backups viejos
│   └── README.md                       # Documentacion de utilidades
│
├── README.md                        # Este archivo (indice)
├── LICENSE                          # Licencia MIT
├── requirements.txt                 # Sin dependencias externas
└── .gitignore                       # Archivos ignorados
```

### Carpetas:

- **`v0.8.x/`**: Version totalmente funcional para VotV 0.8.x ✅
- **`v0.9.0-alpha/`**: Version totalmente funcional para VotV 0.9.0 ✅ (offset descubierto: 0x0000071a)
- **`utilidades-backups/`**: Scripts para gestionar backups (listar, restaurar, limpiar) - Funciona con cualquier usuario

## Contribuir

Las contribuciones son bienvenidas! Si encuentras un bug o tienes una sugerencia:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## Licencia

Este proyecto esta bajo la Licencia MIT. Ver el archivo [LICENSE](LICENSE) para mas detalles.

## Disclaimer

Este proyecto es una herramienta de terceros **no oficial**. No está afiliado, asociado, autorizado ni respaldado por mrdrnose o los desarrolladores de Voices of the Void.

**Voices of the Void** y todos sus derechos pertenecen a [mrdrnose](https://mrdrnose.itch.io/votv).

Usa esta herramienta bajo tu propio riesgo. Siempre haz backups de tus archivos de guardado.

**Compatibilidad de Versiones**:
- **VotV 0.8.x**: ✅ Funciona completamente. Usa la carpeta `v0.8.x/`
- **VotV 0.9.0 alpha**: ✅ Funciona completamente. Usa `v0.9.0-alpha/` (offset: 0x0000071a, probado hasta 2M puntos)

Los backups se crean automaticamente antes de cualquier modificacion.

## Sobre Voices of the Void

**Voices of the Void** es un juego de simulacion/horror desarrollado por [mrdrnose](https://mrdrnose.itch.io).

**Jugar**: [https://mrdrnose.itch.io/votv](https://mrdrnose.itch.io/votv)  
**Discord**: [Servidor oficial](https://discord.gg/votv)  
**Patreon**: [Apoya el desarrollo](https://www.patreon.com/mrdrnose)

## Agradecimientos

- [mrdrnose](https://mrdrnose.itch.io) - Desarrollador de Voices of the Void
- Comunidad de Voices of the Void
- Contribuidores del proyecto

## Contacto

Si tienes preguntas o sugerencias, abre un issue en GitHub.

---

**Disfruta tu partida con todos los puntos que necesites!**

---

## 🏷️ Tags / Keywords

`Voices of the Void` `VotV` `save editor` `save game editor` `points editor` `editor de puntos` `mrdrnose` `VotV mod` `VotV tools` `VotV save file` `VotV hack` `VotV cheats` `VotV trainer` `game save editor` `Unreal Engine save editor` `VotV 0.8` `VotV 0.9` `VotV alpha` `horror game` `simulation game` `signal simulator` `space game` `observatory game` `VotV español` `VotV tutorial` `VotV guide` `VotV modding` `save game modifier` `binary save editor` `GVAS save` `Unreal save format` `VotV points hack` `VotV unlimited points` `VotV money editor` `VotV currency editor` `game memory editor` `VotV utility` `VotV helper` `save file backup` `VotV backup tool` `Python save editor` `cross platform save editor`

**Related searches**: How to edit VotV saves, VotV save location, VotV save file editor, VotV points cheat, VotV trainer download, VotV mod tools, VotV save game location Windows, VotV AppData saves, VotV backup saves, VotV restore save, VotV corrupt save fix, VotV save editor 2025, Voices of the Void cheats, Voices of the Void save editor, Voices of the Void points, Voices of the Void mods, VotV alpha 0.8 save editor, VotV alpha 0.9 save editor

