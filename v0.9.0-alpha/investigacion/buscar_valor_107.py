#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Busca el valor 107 en el archivo testpoints
"""

import struct
import os

archivo = r"C:\Users\JackStar\AppData\Local\VotV\Saved\SaveGames\s_testpoints.sav"

with open(archivo, 'rb') as f:
    data = f.read()

print(f"Buscando valor 107 en {os.path.basename(archivo)}")
print(f"Tamano: {len(data):,} bytes\n")

# Buscar 107 como int32 little endian
valor_buscado = 107
bytes_buscados = struct.pack('<i', valor_buscado)

print(f"Valor: {valor_buscado}")
print(f"Bytes (little endian): {bytes_buscados.hex()}")
print("\nOcurrencias encontradas:\n")

pos = 0
contador = 0
while True:
    pos = data.find(bytes_buscados, pos)
    if pos == -1:
        break
    
    contador += 1
    
    # Mostrar contexto
    start = max(0, pos - 32)
    end = min(len(data), pos + 32)
    
    print(f"Ocurrencia {contador}: Offset 0x{pos:08x} ({pos})")
    
    # Buscar si hay "Points" cerca
    search_start = max(0, pos - 100)
    search_end = min(len(data), pos + 100)
    chunk = data[search_start:search_end]
    
    if b'Points' in chunk:
        points_pos = chunk.find(b'Points')
        abs_points_pos = search_start + points_pos
        print(f"  *** ENCONTRADO cerca de 'Points' en offset 0x{abs_points_pos:08x}")
    
    if b'IntProperty' in chunk:
        print(f"  *** Tiene IntProperty cerca")
    
    # Mostrar contexto hexadecimal
    print(f"  Contexto:")
    for i in range(start, end, 16):
        hex_str = ' '.join(f'{b:02x}' for b in data[i:i+16])
        ascii_str = ''.join(chr(b) if 32 <= b < 127 else '.' for b in data[i:i+16])
        marker = "  >>> " if i <= pos < i + 16 else "      "
        print(f"{marker}0x{i:08x}  {hex_str:<48}  {ascii_str}")
    print()
    
    pos += 1

print(f"\nTotal de ocurrencias: {contador}")

