#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Busca el valor 52 y analiza el contexto cerca de cada ocurrencia
"""

import struct
import os

archivo = r"C:\Users\JackStar\AppData\Local\VotV\Saved\SaveGames\backups\s_09colege_0.sav.backup_20251112_134302"

if not os.path.exists(archivo):
    print(f"ERROR: No se encuentra {archivo}")
    exit(1)

with open(archivo, 'rb') as f:
    data = f.read()

print("="*70)
print("BUSCANDO VALOR 52 CON CONTEXTO")
print("="*70)
print(f"\nArchivo: {os.path.basename(archivo)}")
print(f"Tamano: {len(data):,} bytes\n")

# Buscar todas las ocurrencias de 52
val_52 = struct.pack('<i', 52)
offsets = []
pos = 0
while True:
    pos = data.find(val_52, pos)
    if pos == -1:
        break
    offsets.append(pos)
    pos += 1

print(f"Total de ocurrencias de 52: {len(offsets)}\n")

# Analizar cada ocurrencia buscando "Points"
print("Buscando cual tiene 'Points' cerca...\n")

candidatos = []

for idx, offset in enumerate(offsets, 1):
    # Buscar en un rango de 200 bytes antes y despues
    start = max(0, offset - 200)
    end = min(len(data), offset + 200)
    chunk = data[start:end]
    
    # Buscar strings relacionados con puntos
    tiene_points = b'Points' in chunk or b'points' in chunk
    tiene_intproperty = b'IntProperty' in chunk
    
    if tiene_points:
        candidatos.append((offset, chunk, start))
        
        print(f"*** CANDIDATO #{len(candidatos)} - Offset 0x{offset:08x} ***")
        print(f"    Tiene 'Points' cerca: SI")
        print(f"    Tiene 'IntProperty': {'SI' if tiene_intproperty else 'NO'}")
        
        # Mostrar contexto
        print(f"\n    Contexto (100 bytes antes y despues):")
        ctx_start = max(0, offset - 100)
        ctx_end = min(len(data), offset + 100)
        
        for i in range(ctx_start, ctx_end, 16):
            hex_str = ' '.join(f'{b:02x}' for b in data[i:i+16])
            ascii_str = ''.join(chr(b) if 32 <= b < 127 else '.' for b in data[i:i+16])
            marker = "    >>>" if i <= offset < i + 16 else "       "
            print(f"{marker}0x{i:08x}  {hex_str:<48}  {ascii_str}")
        
        print()

if not candidatos:
    print("No se encontro ningun valor 52 cerca de 'Points'")
    print("\nPrimeras 10 ocurrencias de 52 (sin 'Points' cerca):")
    for i, off in enumerate(offsets[:10], 1):
        print(f"  {i}. Offset 0x{off:08x}")
else:
    print("="*70)
    print(f"TOTAL DE CANDIDATOS ENCONTRADOS: {len(candidatos)}")
    print("="*70)
    print("\nEl valor correcto probablemente es uno de estos candidatos.")

