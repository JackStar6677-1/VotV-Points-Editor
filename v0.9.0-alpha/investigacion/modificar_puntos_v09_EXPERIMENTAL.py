#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EXPERIMENTAL: Modifica puntos en archivos de save de VotV 0.9.0
Basado en hallazgos de offset 0x00000865 en testpoints.sav
"""

import struct
import os
import shutil
from datetime import datetime

def hacer_backup(archivo):
    """Crea una copia de seguridad del archivo"""
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

def buscar_points_property(data):
    """Busca la propiedad Points en el archivo"""
    # Buscar el patron: "Points\x00" seguido de "\x0c\x00\x00\x00IntProperty"
    patron = b'Points\x00\x0c\x00\x00\x00IntProperty'
    
    pos = data.find(patron)
    if pos == -1:
        return None, "No se encontro la propiedad Points"
    
    # El valor está 32 bytes después del inicio de "Points"
    # Points[7 bytes] + \x0c\x00\x00\x00 [4 bytes] + IntProperty[12 bytes] + padding[13 bytes] = 36 bytes
    valor_offset = pos + 36
    
    if valor_offset + 4 > len(data):
        return None, "Offset fuera de rango"
    
    # Leer el valor actual
    valor_actual = struct.unpack('<i', data[valor_offset:valor_offset+4])[0]
    
    return valor_offset, valor_actual

def modificar_save(archivo, nuevos_puntos):
    """Modifica los puntos en un archivo de save v0.9"""
    
    print(f"\nAnalizando: {os.path.basename(archivo)}")
    
    # Leer archivo
    with open(archivo, 'rb') as f:
        data = bytearray(f.read())
    
    # Buscar propiedad Points
    offset, resultado = buscar_points_property(data)
    
    if offset is None:
        print(f"  ERROR: {resultado}")
        return False
    
    print(f"  Puntos actuales: {resultado}")
    print(f"  Offset encontrado: 0x{offset:08x}")
    
    # Hacer backup
    hacer_backup(archivo)
    
    # Modificar valor
    data[offset:offset+4] = struct.pack('<i', nuevos_puntos)
    
    # Guardar
    with open(archivo, 'wb') as f:
        f.write(data)
    
    # Verificar
    with open(archivo, 'rb') as f:
        data_verificacion = f.read()
        valor_verificado = struct.unpack('<i', data_verificacion[offset:offset+4])[0]
    
    if valor_verificado == nuevos_puntos:
        print(f"  OK: Modificado a {nuevos_puntos} puntos")
        return True
    else:
        print(f"  ERROR: Verificacion fallo")
        return False

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Uso: python modificar_puntos_v09_EXPERIMENTAL.py <puntos>")
        print("\nEjemplo: python modificar_puntos_v09_EXPERIMENTAL.py 50000")
        sys.exit(1)
    
    try:
        nuevos_puntos = int(sys.argv[1])
    except ValueError:
        print("ERROR: El valor debe ser un numero entero")
        sys.exit(1)
    
    saves_dir = r"C:\Users\JackStar\AppData\Local\VotV\Saved\SaveGames"
    
    print("="*70)
    print("EXPERIMENTAL: Modificador de puntos VotV 0.9.0")
    print("="*70)
    print(f"\nNuevos puntos: {nuevos_puntos}")
    
    # Solo probar con testpoints primero
    archivo_test = os.path.join(saves_dir, "s_testpoints.sav")
    
    if not os.path.exists(archivo_test):
        print(f"\nERROR: No se encuentra {archivo_test}")
        sys.exit(1)
    
    exito = modificar_save(archivo_test, nuevos_puntos)
    
    if exito:
        print("\n" + "="*70)
        print("EXITO: Ahora carga el save 'testpoints' en el juego para verificar")
        print("="*70)
    else:
        print("\n" + "="*70)
        print("ERROR: No se pudo modificar el archivo")
        print("="*70)

