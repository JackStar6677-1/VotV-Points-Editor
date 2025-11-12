#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de investigacion para archivos .sav de VotV 0.9.0 alpha
Intenta descubrir donde estan almacenados los puntos
"""

import struct
import os
import sys

def hexdump(data, offset=0, length=512):
    """Muestra un hexdump de los datos"""
    for i in range(0, min(length, len(data) - offset), 16):
        pos = offset + i
        hex_str = ' '.join(f'{b:02x}' for b in data[pos:pos+16])
        ascii_str = ''.join(chr(b) if 32 <= b < 127 else '.' for b in data[pos:pos+16])
        print(f'{pos:08x}  {hex_str:<48}  {ascii_str}')

def buscar_strings(data, min_length=4):
    """Busca strings ASCII en los datos"""
    strings = []
    current_string = bytearray()
    start_pos = 0
    
    for i, byte in enumerate(data):
        if 32 <= byte < 127:  # ASCII printable
            if not current_string:
                start_pos = i
            current_string.append(byte)
        else:
            if len(current_string) >= min_length:
                strings.append((start_pos, current_string.decode('ascii', errors='ignore')))
            current_string = bytearray()
    
    return strings

def buscar_valores_enteros(data, valor_minimo=0, valor_maximo=1000000):
    """Busca valores enteros en el rango especificado"""
    resultados = []
    for i in range(len(data) - 4):
        try:
            # Little endian (int32)
            val = struct.unpack('<i', data[i:i+4])[0]
            if valor_minimo <= val <= valor_maximo:
                resultados.append((i, val, 'int32_le'))
            
            # Big endian (int32)
            val_be = struct.unpack('>i', data[i:i+4])[0]
            if valor_minimo <= val_be <= valor_maximo:
                resultados.append((i, val_be, 'int32_be'))
        except:
            pass
    
    return resultados

def analizar_unreal_savegame(data):
    """Intenta analizar estructura de Unreal Engine SaveGame"""
    print("\n=== Analisis de estructura Unreal SaveGame ===")
    
    # Buscar magic number de UE4
    if len(data) > 4:
        magic = struct.unpack('<I', data[0:4])[0]
        print(f"Magic number: 0x{magic:08x}")
    
    # Buscar strings comunes de UE4
    ue_strings = [
        b'SaveGame',
        b'GameInstance',
        b'PlayerState',
        b'IntProperty',
        b'FloatProperty',
        b'StructProperty',
        b'ArrayProperty',
        b'Points',
        b'points',
        b'Money',
        b'money',
        b'Currency',
        b'currency'
    ]
    
    print("\nStrings relevantes encontrados:")
    for search_str in ue_strings:
        pos = data.find(search_str)
        if pos != -1:
            print(f"  {search_str.decode()}: offset 0x{pos:08x} ({pos})")
            # Mostrar contexto
            start = max(0, pos - 32)
            end = min(len(data), pos + 64)
            print(f"    Contexto:")
            hexdump(data, start, end - start)

def analizar_archivo_v09(archivo_path):
    """Analiza un archivo .sav de v0.9"""
    print("="*70)
    print(f"Analizando: {os.path.basename(archivo_path)}")
    print("="*70)
    
    if not os.path.exists(archivo_path):
        print(f"[ERROR] Archivo no encontrado")
        return
    
    with open(archivo_path, 'rb') as f:
        data = f.read()
    
    print(f"\nTamano del archivo: {len(data):,} bytes ({len(data)/1024/1024:.2f} MB)")
    
    # Mostrar primeros bytes
    print("\nPrimeros 256 bytes:")
    hexdump(data, 0, 256)
    
    # Buscar strings
    print("\n=== Strings ASCII (minimo 8 caracteres) ===")
    strings = buscar_strings(data, min_length=8)
    print(f"Encontrados {len(strings)} strings")
    
    # Mostrar strings relevantes (relacionados con puntos/dinero)
    palabras_clave = ['point', 'Point', 'money', 'Money', 'currency', 'Currency', 
                      'cash', 'Cash', 'credit', 'Credit', 'score', 'Score',
                      'save', 'Save', 'player', 'Player', 'game', 'Game']
    
    strings_relevantes = [(pos, s) for pos, s in strings 
                          if any(palabra in s for palabra in palabras_clave)]
    
    if strings_relevantes:
        print("\nStrings potencialmente relevantes:")
        for pos, string in strings_relevantes[:50]:  # Limitar a 50
            print(f"  0x{pos:08x}: {string}")
    
    # Analizar estructura UE4
    analizar_unreal_savegame(data)
    
    # Buscar valores enteros comunes (posibles puntos)
    print("\n=== Buscando valores enteros en rango 0-100000 ===")
    valores = buscar_valores_enteros(data, 0, 100000)
    
    # Agrupar valores repetidos
    conteo = {}
    for pos, val, tipo in valores:
        if val not in conteo:
            conteo[val] = []
        conteo[val].append((pos, tipo))
    
    # Mostrar valores que aparecen multiple veces (mas probable que sean datos del juego)
    valores_frecuentes = {k: v for k, v in conteo.items() if len(v) >= 2}
    
    if valores_frecuentes:
        print(f"\nValores que aparecen multiples veces:")
        for val in sorted(valores_frecuentes.keys())[:20]:  # Top 20
            posiciones = valores_frecuentes[val]
            print(f"  Valor {val:,}: aparece {len(posiciones)} veces")
            for pos, tipo in posiciones[:3]:  # Mostrar primeras 3 ocurrencias
                print(f"    - Offset 0x{pos:08x} ({tipo})")

def comparar_dos_saves():
    """Compara dos archivos de save para encontrar diferencias"""
    saves_dir = r"C:\Users\JackStar\AppData\Local\VotV\Saved\SaveGames"
    
    print("="*70)
    print("COMPARACION DE ARCHIVOS DE SAVE")
    print("="*70)
    print("\nEsta herramienta te ayuda a encontrar donde estan los puntos")
    print("comparando el mismo save antes y despues de ganar puntos en el juego")
    print("\nInstrucciones:")
    print("1. Haz una copia de tu save actual (antes de ganar puntos)")
    print("2. Juega y gana exactamente X puntos (ej: 100)")
    print("3. Guarda el juego")
    print("4. Ejecuta este script con ambos archivos")
    print("\nPor ahora, solo analiza un archivo individual")
    print("="*70)

def main():
    saves_dir = r"C:\Users\JackStar\AppData\Local\VotV\Saved\SaveGames"
    
    if len(sys.argv) > 1:
        archivo = sys.argv[1]
    else:
        # Archivo por defecto: s_09colege.sav (el unico archivo de v0.9)
        archivo = os.path.join(saves_dir, "s_09colege.sav")
        print(f"Uso: python investigar_v09.py <archivo.sav>")
        print(f"\nAnalizando archivo por defecto: s_09colege.sav\n")
    
    analizar_archivo_v09(archivo)
    
    print("\n" + "="*70)
    print("PROXIMOS PASOS:")
    print("="*70)
    print("1. Revisa los strings y valores encontrados arriba")
    print("2. Compara con un archivo de v0.8 que SI tiene Points")
    print("3. Busca patrones de serializacion de Unreal Engine")
    print("4. Intenta modificar valores sospechosos y probar en el juego")
    print("="*70)

if __name__ == "__main__":
    main()

