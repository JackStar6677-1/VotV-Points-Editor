#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Busca manualmente la propiedad Points en s_09colege_0.sav
"""

import struct
import os

archivo = r"C:\Users\JackStar\AppData\Local\VotV\Saved\SaveGames\s_09colege_0.sav"

with open(archivo, 'rb') as f:
    data = f.read()

print("Buscando string 'Points' en el archivo...")

# Buscar "Points\x00" (null-terminated)
patron = b'Points\x00'
pos = data.find(patron)

if pos == -1:
    print("No se encontró 'Points'")
else:
    print(f"\nEncontrado 'Points' en offset 0x{pos:08x}")
    
    # Mostrar contexto amplio
    start = max(0, pos - 100)
    end = min(len(data), pos + 150)
    
    print(f"\nContexto completo:\n")
    for i in range(start, end, 16):
        hex_str = ' '.join(f'{b:02x}' for b in data[i:i+16])
        ascii_str = ''.join(chr(b) if 32 <= b < 127 else '.' for b in data[i:i+16])
        marker = ">>>" if i <= pos < i + 16 else "   "
        print(f"{marker} 0x{i:08x}  {hex_str:<48}  {ascii_str}")
    
    # Intentar leer el valor después de Points
    # Formato típico: Points\x00 + tipo (IntProperty) + tamaño + valor
    offset_after_points = pos + 7  # Después de "Points\x00"
    
    print(f"\nIntentar interpretar estructura después de 'Points':")
    print(f"Offset después de 'Points\\x00': 0x{offset_after_points:08x}")
    
    # Ver si viene IntProperty
    if data[offset_after_points:offset_after_points+12] == b'\x0c\x00\x00\x00IntProperty':
        print("  ✓ Encontrado IntProperty después de Points")
        
        # Saltar IntProperty y leer el valor
        # IntProperty = 12 bytes + 4 bytes de tamaño + otros metadatos
        # Estructura: tipo_size(4) + IntProperty(12) + data_size(4) + padding(8) + value(4)
        value_offset = offset_after_points + 12 + 4 + 4 + 8
        
        if value_offset + 4 <= len(data):
            valor = struct.unpack('<i', data[value_offset:value_offset+4])[0]
            print(f"  Valor leído en offset 0x{value_offset:08x}: {valor}")

# Buscar todas las ocurrencias de valor 62 como int32
print(f"\n\nBuscando TODOS los valores 62 en el archivo...")
val_62 = struct.pack('<i', 62)
occurrences = []
pos = 0
while True:
    pos = data.find(val_62, pos)
    if pos == -1:
        break
    occurrences.append(pos)
    pos += 1

print(f"Total de ocurrencias de 62: {len(occurrences)}")
print(f"Primeras 10 ocurrencias:")
for i, off in enumerate(occurrences[:10]):
    print(f"  {i+1}. Offset 0x{off:08x}")

