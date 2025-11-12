# VotV Points Editor - Version 0.8.x

Editor de puntos para **Voices of the Void Alpha 0.8.x** - Totalmente funcional y probado.

## Estado: ESTABLE

Esta version funciona perfectamente con todos los archivos de guardado de VotV 0.8.x.

## Uso Rapido

### Windows (más fácil)
Doble click en:
- **`PRUEBA_RAPIDA.bat`**: Establece 50,000 puntos
- **`VERIFICAR_PUNTOS.bat`**: Ver puntos actuales

### Línea de comandos

```bash
# Establecer puntos específicos
python set_puntos.py 50000

# Ver valores actuales
python set_puntos.py
```

## Scripts Disponibles

- **`set_puntos.py`**: Script principal (recomendado)
- **`modificar_puntos.py`**: Version interactiva con menu
- **`buscar_puntos_todos_saves.py`**: Diagnostico y verificacion
- **`set_puntos_todos_saves.py`**: Version alternativa standalone
- **`PRUEBA_RAPIDA.bat`**: Acceso rapido Windows
- **`VERIFICAR_PUNTOS.bat`**: Verificacion rapida

## Como Funciona

Voices of the Void 0.8.x almacena los puntos en **DOS ubicaciones**:

1. **`data.sav`** (archivo global):
   - `total_points_42`: Total de puntos ganados
   - `points_spent_43`: Puntos gastados

2. **Archivos de partida** (`s_*.sav`):
   - `Points`: Puntos disponibles en esa partida
   - **Este es el valor que el juego lee**

El script modifica **AMBOS** para asegurar sincronización perfecta.

## Importante

- **Cierra el juego** antes de modificar
- Los backups se crean automaticamente en `SaveGames/backups/`
- Compatible SOLO con VotV 0.8.x

## Ejemplos

```bash
# Inicio del juego
python set_puntos.py 10000

# Progresión media
python set_puntos.py 50000

# Modo sandbox
python set_puntos.py 500000
```

## Volver

Ver [README principal](../README.md) para mas informacion.

