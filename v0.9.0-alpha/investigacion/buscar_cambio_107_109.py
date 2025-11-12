#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Busca específicamente donde cambió 107 a 109
"""

import struct
import os
import glob

saves_dir = r"C:\Users\JackStar\AppData\Local\VotV\Saved\SaveGames"
backup_dir = os.path.join(saves_dir, "backups")

# Save actual
actual = os.path.join(saves_dir, "s_testpoints.sav")

# Buscar backups
backups = sorted([f for f in glob.glob(os.path.join(backup_dir, "s_testpoints.sav.backup_*"))])

print("Backups encontrados:")
for b in backups:
    print(f"  - {os.path.basename(b)}")

if not backups:
    print("\nNo hay backups")
    exit(1)

# Necesitamos el backup ORIGINAL (antes de todas las modificaciones)
# El primer backup debería tener los 107 puntos originales
backup_original = backups[0]

print(f"\nUsando backup: {os.path.basename(backup_original)}")
print(f"Comparando con: s_testpoints.sav (actual)")

with open(backup_original, 'rb') as f:
    data_old = f.read()

with open(actual, 'rb') as f:
    data_new = f.read()

print(f"\nTamaño backup: {len(data_old):,} bytes")
print(f"Tamaño actual: {len(data_new):,} bytes")

# Buscar el valor 107 como int32 little endian
val_107 = struct.pack('<i', 107)
val_109 = struct.pack('<i', 109)

print(f"\nBuscando 107 (0x{val_107.hex()}) en backup...")
pos_107_in_old = []
pos = 0
while True:
    pos = data_old.find(val_107, pos)
    if pos == -1:
        break
    pos_107_in_old.append(pos)
    pos += 1

print(f"Encontradas {len(pos_107_in_old)} ocurrencias de 107 en backup")

print(f"\nBuscando 109 (0x{val_109.hex()}) en actual...")
pos_109_in_new = []
pos = 0
while True:
    pos = data_new.find(val_109, pos)
    if pos == -1:
        break
    pos_109_in_new.append(pos)
    pos += 1

print(f"Encontradas {len(pos_109_in_new)} ocurrencias de 109 en actual")

# Buscar offsets donde era 107 y ahora es 109
print(f"\nBuscando offsets donde 107 cambió a 109...")
candidatos = []

for offset in pos_107_in_old:
    if offset + 4 <= len(data_new):
        valor_nuevo = struct.unpack('<i', data_new[offset:offset+4])[0]
        if valor_nuevo == 109:
            candidatos.append(offset)
            print(f"\n*** ENCONTRADO en offset 0x{offset:08x} ***")
            
            # Mostrar contexto
            start = max(0, offset - 64)
            end = min(len(data_old), offset + 64)
            
            print(f"\nContexto BACKUP (107):")
            chunk = data_old[start:end]
            if b'Points' in chunk or b'points' in chunk:
                print("  *** Contiene 'Points' cerca! ***")
            
            for i in range(start, end, 16):
                hex_str = ' '.join(f'{b:02x}' for b in data_old[i:i+16])
                ascii_str = ''.join(chr(b) if 32 <= b < 127 else '.' for b in data_old[i:i+16])
                marker = ">>>" if i <= offset < i + 16 else "   "
                print(f"  {marker} 0x{i:08x}  {hex_str:<48}  {ascii_str}")
            
            print(f"\nContexto ACTUAL (109):")
            for i in range(start, end, 16):
                hex_str = ' '.join(f'{b:02x}' for b in data_new[i:i+16])
                ascii_str = ''.join(chr(b) if 32 <= b < 127 else '.' for b in data_new[i:i+16])
                marker = ">>>" if i <= offset < i + 16 else "   "
                print(f"  {marker} 0x{i:08x}  {hex_str:<48}  {ascii_str}")

print(f"\n\n{'='*70}")
print(f"TOTAL DE CAMBIOS 107->109: {len(candidatos)}")
if candidatos:
    print(f"\nOffsets encontrados:")
    for off in candidatos:
        print(f"  - 0x{off:08x} ({off})")
print('='*70)

