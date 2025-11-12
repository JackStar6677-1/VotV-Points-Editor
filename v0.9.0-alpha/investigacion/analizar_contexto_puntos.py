#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Analiza el contexto alrededor del offset de puntos
"""

import struct
import os

saves_dir = r"C:\Users\JackStar\AppData\Local\VotV\Saved\SaveGames"
archivo = os.path.join(saves_dir, "s_testpoints.sav")

offset_puntos = 0x00244bad

with open(archivo, 'rb') as f:
    data = f.read()

# Leer un rango amplio alrededor del offset
start = max(0, offset_puntos - 200)
end = min(len(data), offset_puntos + 200)

chunk = data[start:end]

print(f"Analizando contexto del offset 0x{offset_puntos:08x}")
print(f"Valor actual: {struct.unpack('<i', data[offset_puntos:offset_puntos+4])[0]}")
print(f"\nBuscando strings ASCII cerca...\n")

# Buscar strings ASCII
for i in range(len(chunk) - 4):
    abs_offset = start + i
    # Buscar secuencias de caracteres ASCII imprimibles
    string_chars = []
    j = i
    while j < len(chunk) and 32 <= chunk[j] < 127 and chunk[j] != 0:
        string_chars.append(chr(chunk[j]))
        j += 1
    
    if len(string_chars) >= 5:  # Strings de al menos 5 caracteres
        string = ''.join(string_chars)
        rel_offset = abs_offset - offset_puntos
        print(f"  Offset 0x{abs_offset:08x} (puntos{rel_offset:+d}): '{string}'")

print(f"\n\nHex dump completo (200 bytes antes y después):\n")

for i in range(start, end, 16):
    hex_str = ' '.join(f'{b:02x}' for b in data[i:i+16])
    ascii_str = ''.join(chr(b) if 32 <= b < 127 else '.' for b in data[i:i+16])
    
    marker = ""
    if i <= offset_puntos < i + 16:
        marker = " >>> PUNTOS AQUÍ"
        # Marcar el byte exacto
        byte_pos = offset_puntos - i
        hex_parts = hex_str.split()
        if byte_pos < len(hex_parts):
            hex_parts[byte_pos] = f"[{hex_parts[byte_pos]}]"
            hex_str = ' '.join(hex_parts)
    
    print(f"  0x{i:08x}  {hex_str:<48}  {ascii_str}{marker}")

# Buscar patrones repetitivos
print(f"\n\nBuscando patrones conocidos de Unreal Engine...")

patterns = {
    b'IntProperty': 'IntProperty (tipo de datos)',
    b'StructProperty': 'StructProperty (tipo de datos)',
    b'ArrayProperty': 'ArrayProperty (tipo de datos)',
    b'FloatProperty': 'FloatProperty (tipo de datos)',
    b'None\x00': 'None (terminador de propiedades)',
}

for pattern, desc in patterns.items():
    pos = chunk.find(pattern)
    while pos != -1:
        abs_pos = start + pos
        rel_pos = abs_pos - offset_puntos
        print(f"  {desc} en offset 0x{abs_pos:08x} (puntos{rel_pos:+d})")
        pos = chunk.find(pattern, pos + 1)

