#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Compara s_09colege.sav con s_09colege_0.sav para encontrar los 62 puntos
"""

import struct
import os

saves_dir = r"C:\Users\JackStar\AppData\Local\VotV\Saved\SaveGames"

archivo_original = os.path.join(saves_dir, "s_09colege.sav")
archivo_62pts = os.path.join(saves_dir, "s_09colege_0.sav")

print("="*70)
print("COMPARANDO SAVES DE V0.9.0 PARA ENCONTRAR PUNTOS")
print("="*70)

with open(archivo_original, 'rb') as f:
    data_original = f.read()

with open(archivo_62pts, 'rb') as f:
    data_62 = f.read()

print(f"\nArchivo original: {len(data_original):,} bytes")
print(f"Archivo 62 pts:   {len(data_62):,} bytes")
print(f"Diferencia:       {len(data_62) - len(data_original):,} bytes")

# Buscar el valor 62 como int32 little endian
val_62 = struct.pack('<i', 62)

print(f"\nBuscando valor 62 (0x{val_62.hex()}) en archivo de 62 puntos...")
pos_62 = []
pos = 0
while True:
    pos = data_62.find(val_62, pos)
    if pos == -1:
        break
    pos_62.append(pos)
    pos += 1

print(f"Encontradas {len(pos_62)} ocurrencias de 62 en el archivo con 62 puntos")

# Comparar offsets cercanos en ambos archivos
print(f"\nBuscando cuál de esas ocurrencias cambió desde el original...\n")

candidatos = []
for offset in pos_62[:100]:  # Revisar las primeras 100 ocurrencias
    if offset + 4 <= len(data_original):
        valor_original = struct.unpack('<i', data_original[offset:offset+4])[0]
        
        # Si en el original NO era 62, entonces cambió!
        if valor_original != 62:
            candidatos.append((offset, valor_original, 62))
            print(f"*** CAMBIO ENCONTRADO en offset 0x{offset:08x} ***")
            print(f"    Original: {valor_original} -> Nuevo: 62")
            
            # Mostrar contexto
            start = max(0, offset - 80)
            end = min(len(data_62), offset + 80)
            
            # Buscar si hay "Points" o strings relevantes cerca
            chunk = data_62[start:end]
            if b'Points' in chunk or b'points' in chunk:
                print(f"    *** Contiene 'Points' cerca! ***")
            if b'IntProperty' in chunk:
                print(f"    *** Tiene IntProperty cerca ***")
            if b'money' in chunk or b'Money' in chunk:
                print(f"    *** Tiene 'money' cerca (podría ser dinero, no puntos) ***")
            
            print(f"\n    Contexto ORIGINAL ({valor_original}):")
            for i in range(start, end, 16):
                if i + 16 <= len(data_original):
                    hex_str = ' '.join(f'{b:02x}' for b in data_original[i:i+16])
                    ascii_str = ''.join(chr(b) if 32 <= b < 127 else '.' for b in data_original[i:i+16])
                    marker = "    >>>" if i <= offset < i + 16 else "       "
                    print(f"{marker}0x{i:08x}  {hex_str:<48}  {ascii_str}")
            
            print(f"\n    Contexto NUEVO (62):")
            for i in range(start, end, 16):
                hex_str = ' '.join(f'{b:02x}' for b in data_62[i:i+16])
                ascii_str = ''.join(chr(b) if 32 <= b < 127 else '.' for b in data_62[i:i+16])
                marker = "    >>>" if i <= offset < i + 16 else "       "
                print(f"{marker}0x{i:08x}  {hex_str:<48}  {ascii_str}")
            
            print()

print("="*70)
print(f"TOTAL DE CAMBIOS ENCONTRADOS: {len(candidatos)}")
if candidatos:
    print(f"\nResumen de offsets:")
    for off, old_val, new_val in candidatos:
        print(f"  0x{off:08x}: {old_val} -> {new_val}")
print("="*70)

