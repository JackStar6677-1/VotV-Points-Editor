#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Compara dos archivos de save para encontrar diferencias
"""

import struct
import os

def comparar_archivos(archivo1, archivo2):
    """Compara dos archivos byte a byte"""
    
    print(f"\nComparando archivos:")
    print(f"  Archivo 1: {os.path.basename(archivo1)}")
    print(f"  Archivo 2: {os.path.basename(archivo2)}")
    
    with open(archivo1, 'rb') as f1:
        data1 = f1.read()
    
    with open(archivo2, 'rb') as f2:
        data2 = f2.read()
    
    if len(data1) != len(data2):
        print(f"\nTamanos diferentes:")
        print(f"  Archivo 1: {len(data1):,} bytes")
        print(f"  Archivo 2: {len(data2):,} bytes")
    else:
        print(f"\nTamano identico: {len(data1):,} bytes")
    
    # Buscar diferencias
    diferencias = []
    tamano_min = min(len(data1), len(data2))
    
    for i in range(tamano_min):
        if data1[i] != data2[i]:
            diferencias.append(i)
    
    print(f"\nTotal de bytes diferentes: {len(diferencias)}")
    
    if len(diferencias) == 0:
        print("\nLos archivos son identicos")
        return
    
    print(f"\nMostrando primeras 50 diferencias:\n")
    
    # Agrupar diferencias cercanas
    grupos = []
    if diferencias:
        grupo_actual = [diferencias[0]]
        for i in range(1, len(diferencias)):
            if diferencias[i] - diferencias[i-1] <= 20:  # Si están a menos de 20 bytes
                grupo_actual.append(diferencias[i])
            else:
                grupos.append(grupo_actual)
                grupo_actual = [diferencias[i]]
        grupos.append(grupo_actual)
    
    for idx, grupo in enumerate(grupos[:50]):
        offset_inicio = grupo[0]
        offset_fin = grupo[-1]
        
        print(f"Grupo {idx + 1}: Offset 0x{offset_inicio:08x} - 0x{offset_fin:08x}")
        
        # Mostrar contexto
        contexto_inicio = max(0, offset_inicio - 32)
        contexto_fin = min(tamano_min, offset_fin + 32)
        
        # Intentar interpretar como int32
        if len(grupo) >= 4 and offset_fin - offset_inicio <= 10:
            # Puede ser un int32
            try:
                for off in grupo[:5]:  # Solo primeros 5 offsets del grupo
                    if off + 4 <= tamano_min:
                        val1_le = struct.unpack('<i', data1[off:off+4])[0]
                        val2_le = struct.unpack('<i', data2[off:off+4])[0]
                        val1_be = struct.unpack('>i', data1[off:off+4])[0]
                        val2_be = struct.unpack('>i', data2[off:off+4])[0]
                        
                        print(f"  Offset 0x{off:08x}:")
                        print(f"    Bytes: {data1[off:off+4].hex()} -> {data2[off:off+4].hex()}")
                        print(f"    int32_le: {val1_le} -> {val2_le}")
                        if val1_le == 107 and val2_le == 109:
                            print(f"    *** ENCONTRADO! 107 -> 109 ***")
                        if val1_be == 107 and val2_be == 109:
                            print(f"    int32_be: {val1_be} -> {val2_be}")
                            print(f"    *** ENCONTRADO! 107 -> 109 (big endian) ***")
            except:
                pass
        
        # Mostrar hex dump
        print(f"  Contexto archivo 1:")
        for i in range(contexto_inicio, contexto_fin, 16):
            hex_str = ' '.join(f'{b:02x}' for b in data1[i:i+16])
            ascii_str = ''.join(chr(b) if 32 <= b < 127 else '.' for b in data1[i:i+16])
            print(f"    0x{i:08x}  {hex_str:<48}  {ascii_str}")
        
        print(f"  Contexto archivo 2:")
        for i in range(contexto_inicio, contexto_fin, 16):
            hex_str = ' '.join(f'{b:02x}' for b in data2[i:i+16])
            ascii_str = ''.join(chr(b) if 32 <= b < 127 else '.' for b in data2[i:i+16])
            marker = "  >>>" if any(i <= d < i+16 for d in grupo) else "     "
            print(f"{marker}0x{i:08x}  {hex_str:<48}  {ascii_str}")
        
        print()

if __name__ == "__main__":
    saves_dir = r"C:\Users\JackStar\AppData\Local\VotV\Saved\SaveGames"
    
    # El save actual con 109 puntos
    archivo_actual = os.path.join(saves_dir, "s_testpoints.sav")
    
    # Buscar el backup más reciente (antes de que el juego guardara)
    backup_dir = os.path.join(saves_dir, "backups")
    backups = [f for f in os.listdir(backup_dir) if f.startswith("s_testpoints.sav.backup_")]
    
    if not backups:
        print("ERROR: No hay backups")
        exit(1)
    
    # Ordenar por fecha
    backups.sort()
    
    print("Backups disponibles:")
    for i, b in enumerate(backups):
        print(f"  {i+1}. {b}")
    
    # Usar el penúltimo backup (antes de nuestra modificación experimental)
    if len(backups) >= 2:
        backup_usar = backups[-2]
        print(f"\nUsando backup: {backup_usar}")
    else:
        backup_usar = backups[-1]
        print(f"\nUsando unico backup: {backup_usar}")
    
    archivo_backup = os.path.join(backup_dir, backup_usar)
    
    comparar_archivos(archivo_backup, archivo_actual)

