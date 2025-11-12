#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VotV Points Editor - Versión 0.9.0 ALPHA
Modifica los puntos en archivos de guardado de Voices of the Void v0.9.0

DESCUBRIMIENTO DEL OFFSET:
- Offset: 0x0000071a
- Tipo: IntProperty (4 bytes, little-endian)
- Propiedad: "Points"
- Confirmado funcional hasta 2,000,000 puntos

Uso:
    python set_puntos.py <cantidad_puntos>
    
Ejemplo:
    python set_puntos.py 50000
"""

import os
import sys
import struct
import shutil
import glob
from datetime import datetime

# Ruta base de los saves
SAVE_DIR = r"C:\Users\JackStar\AppData\Local\VotV\Saved\SaveGames"

# Offset confirmado para VotV 0.9.0 (propiedad "Points")
OFFSET_POINTS_V09 = 0x0000071a

def hacer_backup(archivo):
    """Crea una copia de seguridad del archivo en carpeta separada"""
    saves_dir = os.path.dirname(archivo)
    backup_dir = os.path.join(saves_dir, "backups")
    
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    nombre_archivo = os.path.basename(archivo)
    backup = os.path.join(backup_dir, f"{nombre_archivo}.backup_{timestamp}")
    
    shutil.copy2(archivo, backup)
    print(f"  [BACKUP] {nombre_archivo}.backup_{timestamp}")
    return backup

def modificar_save_v09(archivo_save, nuevos_puntos):
    """
    Modifica el archivo de save de VotV 0.9.0 para establecer los puntos.
    
    Args:
        archivo_save: Ruta completa al archivo .sav
        nuevos_puntos: Cantidad de puntos a establecer
        
    Returns:
        tuple: (exito: bool, mensaje: str)
    """
    try:
        with open(archivo_save, 'rb') as f:
            contenido = bytearray(f.read())
        
        # Verificar que el archivo sea lo suficientemente grande
        if len(contenido) <= OFFSET_POINTS_V09 + 4:
            return False, "Archivo demasiado pequeño o corrupto"
        
        # Leer los puntos actuales
        puntos_actuales = struct.unpack('<i', contenido[OFFSET_POINTS_V09:OFFSET_POINTS_V09+4])[0]
        
        # Hacer backup
        hacer_backup(archivo_save)
        
        # Escribir los nuevos puntos
        contenido[OFFSET_POINTS_V09:OFFSET_POINTS_V09+4] = struct.pack('<i', nuevos_puntos)
        
        with open(archivo_save, 'wb') as f:
            f.write(contenido)
        
        return True, f"{puntos_actuales} -> {nuevos_puntos}"
        
    except FileNotFoundError:
        return False, "Archivo no encontrado"
    except Exception as e:
        return False, f"Error: {e}"

def modificar_data_sav(puntos):
    """Modifica data.sav (perfil global)"""
    archivo_data = os.path.join(SAVE_DIR, "data.sav")
    
    if not os.path.exists(archivo_data):
        print("  [SKIP] data.sav no encontrado")
        return False
    
    print("\n[1] Modificando data.sav (perfil global)...")
    exito, mensaje = modificar_save_v09(archivo_data, puntos)
    
    if exito:
        print(f"  [OK] data.sav: {mensaje}")
        return True
    else:
        print(f"  [ERROR] data.sav: {mensaje}")
        return False

def modificar_saves_individuales(puntos):
    """Modifica todos los archivos s_*.sav"""
    patron = os.path.join(SAVE_DIR, "s_*.sav")
    archivos_save = glob.glob(patron)
    
    if not archivos_save:
        print("\n[2] No se encontraron archivos de partida (s_*.sav)")
        return
    
    print(f"\n[2] Modificando archivos de partida individuales ({len(archivos_save)} encontrados)...")
    
    modificados = 0
    omitidos = 0
    
    for archivo_save in sorted(archivos_save):
        nombre = os.path.basename(archivo_save)
        exito, mensaje = modificar_save_v09(archivo_save, puntos)
        
        if exito:
            print(f"  [OK] {nombre}: {mensaje}")
            modificados += 1
        else:
            print(f"  [SKIP] {nombre}: {mensaje}")
            omitidos += 1
    
    print(f"\n  Total: {modificados} modificados, {omitidos} omitidos")

def main():
    if len(sys.argv) < 2:
        print("="*70)
        print("  VotV Points Editor - Version 0.9.0 ALPHA")
        print("="*70)
        print("\nUso:")
        print("  python set_puntos.py <cantidad_puntos>")
        print("\nEjemplo:")
        print("  python set_puntos.py 50000")
        print("\nLimite probado:")
        print("  Hasta 2,000,000 puntos funcionan correctamente")
        print("="*70)
        sys.exit(1)
    
    try:
        puntos = int(sys.argv[1])
        if puntos < 0:
            print("ERROR: Los puntos no pueden ser negativos")
            sys.exit(1)
        if puntos > 2000000:
            print("ADVERTENCIA: Valores superiores a 2,000,000 no han sido probados")
    except ValueError:
        print("ERROR: La cantidad de puntos debe ser un numero entero")
        sys.exit(1)
    
    print("="*70)
    print("  VotV Points Editor - Version 0.9.0 ALPHA")
    print("="*70)
    print(f"  Puntos a establecer: {puntos:,}")
    print(f"  Directorio: {SAVE_DIR}")
    print(f"  Offset: 0x{OFFSET_POINTS_V09:08x}")
    print("="*70)
    
    # Modificar data.sav
    modificar_data_sav(puntos)
    
    # Modificar saves individuales
    modificar_saves_individuales(puntos)
    
    print("\n" + "="*70)
    print("  PROCESO COMPLETADO")
    print("="*70)
    print("\n  Los backups se guardaron en:")
    print(f"  {os.path.join(SAVE_DIR, 'backups')}")
    print("\n  Carga el juego para verificar los cambios")
    print("="*70)

if __name__ == "__main__":
    main()

