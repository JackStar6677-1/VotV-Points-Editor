#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Modifica TODOS los valores 52 a 10,000 en el save
Estrategia de fuerza bruta para encontrar los puntos reales
"""

import struct
import os
import shutil
from datetime import datetime

def hacer_backup(archivo):
    """Crea backup"""
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

archivo = r"C:\Users\JackStar\AppData\Local\VotV\Saved\SaveGames\s_09colege_0.sav"

if not os.path.exists(archivo):
    print(f"ERROR: No se encuentra {archivo}")
    exit(1)

print("="*70)
print("MODIFICANDO TODOS LOS VALORES 52 A 10,000")
print("="*70)

# Leer archivo
with open(archivo, 'rb') as f:
    data = bytearray(f.read())

print(f"\nArchivo: {os.path.basename(archivo)}")
print(f"Tamaño: {len(data):,} bytes")

# Buscar TODAS las ocurrencias de 52 como int32 little-endian
val_52 = struct.pack('<i', 52)
val_10k = struct.pack('<i', 10000)

print(f"\nBuscando valor 52 (0x{val_52.hex()})...")

offsets_52 = []
pos = 0
while True:
    pos = data.find(val_52, pos)
    if pos == -1:
        break
    offsets_52.append(pos)
    pos += 1

print(f"Encontradas {len(offsets_52)} ocurrencias de 52")

if len(offsets_52) == 0:
    print("\nNo se encontró el valor 52 en el archivo")
    print("¿Los puntos en el juego son exactamente 52?")
    exit(1)

print(f"\nOffsets encontrados:")
for i, off in enumerate(offsets_52[:20], 1):  # Mostrar primeros 20
    print(f"  {i}. 0x{off:08x} ({off})")
    
if len(offsets_52) > 20:
    print(f"  ... y {len(offsets_52) - 20} más")

# Hacer backup
hacer_backup(archivo)

# Modificar TODAS las ocurrencias
print(f"\nModificando TODOS los valores 52 -> 10,000...")
for offset in offsets_52:
    data[offset:offset+4] = val_10k

# Guardar
with open(archivo, 'wb') as f:
    f.write(data)

# Verificar
print(f"\nVerificando cambios...")
with open(archivo, 'rb') as f:
    data_verificacion = f.read()

count_10k = data_verificacion.count(val_10k)
count_52_restantes = data_verificacion.count(val_52)

print(f"  Valores 10,000 en archivo: {count_10k}")
print(f"  Valores 52 restantes: {count_52_restantes}")

print("\n" + "="*70)
print("PROCESO COMPLETADO")
print("="*70)
print("\n🎮 AHORA CARGA EL SAVE EN EL JUEGO")
print("Si alguno de esos valores era los puntos, deberías ver 10,000 puntos")
print("="*70)

