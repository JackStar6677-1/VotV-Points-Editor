#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Modificador de Puntos para VotV 0.9.0 - VERSIÓN FUNCIONAL
Basado en hallazgos: La propiedad Points existe y funciona igual que en v0.8.x
"""

import os
import sys
import struct
import shutil
from datetime import datetime
import glob

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
    print(f"[OK] Backup creado: {nombre_archivo}.backup_{timestamp}")
    return backup

def buscar_propiedad_points(data):
    """Busca la propiedad Points en el archivo"""
    # Buscar el patrón: Points\x00 + IntProperty
    patron = b'Points\x00\x0c\x00\x00\x00IntProperty'
    
    pos = data.find(patron)
    if pos == -1:
        return None, "No se encontró la propiedad Points"
    
    # El valor está después de: Points\x00 (7) + \x0c\x00\x00\x00 (4) + IntProperty (12) + padding (13)
    # Total: 7 + 4 + 12 + 13 = 36 bytes
    valor_offset = pos + 36
    
    if valor_offset + 4 > len(data):
        return None, "Offset fuera de rango"
    
    # Leer el valor actual
    valor_actual = struct.unpack('<i', data[valor_offset:valor_offset+4])[0]
    
    return valor_offset, valor_actual

def modificar_save_individual(archivo, puntos_disponibles):
    """Modifica un archivo de partida individual (.s_*.sav)"""
    
    nombre = os.path.basename(archivo)
    
    try:
        # Leer archivo
        with open(archivo, 'rb') as f:
            data = bytearray(f.read())
        
        # Buscar la propiedad Points
        offset, valor_actual = buscar_propiedad_points(data)
        
        if offset is None:
            return False, f"OMITIDO: {valor_actual}"
        
        # Hacer backup
        hacer_backup(archivo)
        
        # Modificar el valor
        data[offset:offset+4] = struct.pack('<i', puntos_disponibles)
        
        # Guardar archivo modificado
        with open(archivo, 'wb') as f:
            f.write(data)
        
        # Verificar
        with open(archivo, 'rb') as f:
            data_verificacion = f.read()
            valor_verificado = struct.unpack('<i', data_verificacion[offset:offset+4])[0]
        
        if valor_verificado == puntos_disponibles:
            return True, f"OK: {nombre} ({valor_actual} -> {puntos_disponibles})"
        else:
            return False, f"ERROR: Verificación falló"
            
    except Exception as e:
        return False, f"ERROR: {str(e)}"

def modificar_data_sav(saves_dir, puntos_disponibles):
    """Modifica data.sav (archivo global de perfil)"""
    archivo_data = os.path.join(saves_dir, "data.sav")
    
    if not os.path.exists(archivo_data):
        print("  [!] data.sav no encontrado, omitiendo...")
        return False
    
    print(f"\n2. Modificando data.sav (perfil global)...")
    
    try:
        with open(archivo_data, 'rb') as f:
            data = bytearray(f.read())
        
        # Buscar total_points_42
        patron_total = b'total_points_42\x00'
        pos_total = data.find(patron_total)
        
        if pos_total != -1:
            hacer_backup(archivo_data)
            
            # Buscar el offset del valor (similar a v0.8.x)
            # Después de total_points_42\x00 viene IntProperty y luego el valor
            offset_valor = pos_total + len(patron_total) + 4 + 12 + 13
            
            if offset_valor + 4 <= len(data):
                data[offset_valor:offset_valor+4] = struct.pack('<i', puntos_disponibles)
                
                with open(archivo_data, 'wb') as f:
                    f.write(data)
                
                print(f"  OK: data.sav modificado")
                return True
        
        print(f"  [!] No se encontró total_points_42 en data.sav")
        return False
        
    except Exception as e:
        print(f"  ERROR: {str(e)}")
        return False

def establecer_puntos_disponibles(saves_dir, puntos_disponibles):
    """Establece los puntos disponibles en todos los archivos de save"""
    
    print(f"\n1. Modificando archivos de partida individuales (s_*.sav)...")
    
    # Buscar todos los archivos s_*.sav
    patron_saves = os.path.join(saves_dir, "s_*.sav")
    archivos_save = glob.glob(patron_saves)
    
    if archivos_save:
        modificados = 0
        omitidos = 0
        
        for archivo_save in sorted(archivos_save):
            nombre = os.path.basename(archivo_save)
            exito, mensaje = modificar_save_individual(archivo_save, puntos_disponibles)
            
            if exito:
                print(f"  {mensaje}")
                modificados += 1
            else:
                print(f"  {mensaje}")
                omitidos += 1
        
        print(f"\n  Total: {modificados} modificados, {omitidos} omitidos")
    else:
        print(f"  No se encontraron archivos de partida")
    
    # Modificar data.sav
    modificar_data_sav(saves_dir, puntos_disponibles)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("="*70)
        print("MODIFICADOR DE PUNTOS - VotV 0.9.0")
        print("="*70)
        print("\nUso: python set_puntos_v09_FUNCIONAL.py <puntos>")
        print("\nEjemplo:")
        print("  python set_puntos_v09_FUNCIONAL.py 50000")
        print("\nNota: Este script crea backups automáticamente en SaveGames/backups/")
        print("="*70)
        sys.exit(1)
    
    try:
        puntos_disponibles = int(sys.argv[1])
    except ValueError:
        print("ERROR: El valor debe ser un número entero")
        sys.exit(1)
    
    # Ruta predeterminada de saves
    saves_dir = r"C:\Users\JackStar\AppData\Local\VotV\Saved\SaveGames"
    
    if not os.path.exists(saves_dir):
        print(f"ERROR: No se encuentra la carpeta de saves: {saves_dir}")
        sys.exit(1)
    
    print("="*70)
    print("MODIFICADOR DE PUNTOS - VotV 0.9.0")
    print("="*70)
    print(f"\nCarpeta de saves: {saves_dir}")
    print(f"Puntos a establecer: {puntos_disponibles:,}")
    
    establecer_puntos_disponibles(saves_dir, puntos_disponibles)
    
    print("\n" + "="*70)
    print("PROCESO COMPLETADO")
    print("="*70)
    print("\n¡Carga el juego para verificar los cambios!")

