#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Modifica SOLO el offset exacto de Points a un valor razonable
"""

import struct
import os
import shutil
from datetime import datetime

def hacer_backup(archivo):
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
OFFSET_POINTS = 0x0000071a
NUEVO_VALOR = 2000000  # Probando limite maximo

print("="*70)
print("MODIFICANDO OFFSET EXACTO DE POINTS")
print("="*70)

with open(archivo, 'rb') as f:
    data = bytearray(f.read())

print(f"\nArchivo: {os.path.basename(archivo)}")
print(f"Offset: 0x{OFFSET_POINTS:08x}")

# Leer valor actual
valor_actual = struct.unpack('<i', data[OFFSET_POINTS:OFFSET_POINTS+4])[0]
print(f"Valor actual: {valor_actual}")
print(f"Nuevo valor: {NUEVO_VALOR}")

# Hacer backup
hacer_backup(archivo)

# Modificar
data[OFFSET_POINTS:OFFSET_POINTS+4] = struct.pack('<i', NUEVO_VALOR)

# Guardar
with open(archivo, 'wb') as f:
    f.write(data)

# Verificar
with open(archivo, 'rb') as f:
    data_verificacion = f.read()
    valor_verificado = struct.unpack('<i', data_verificacion[OFFSET_POINTS:OFFSET_POINTS+4])[0]

print(f"\nVerificacion: {valor_verificado}")

if valor_verificado == NUEVO_VALOR:
    print("\n" + "="*70)
    print("MODIFICACION EXITOSA")
    print("="*70)
    print(f"\nCarga el save y verifica si tienes {NUEVO_VALOR} puntos")
else:
    print("\nERROR en la verificacion")

