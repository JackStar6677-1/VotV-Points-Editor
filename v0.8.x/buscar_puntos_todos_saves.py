#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para buscar propiedades de puntos en TODOS los archivos .sav
Esto nos ayudará a entender dónde están realmente almacenados los puntos
"""

import struct
import os
import glob

def buscar_propiedad_int(data, nombre_propiedad):
    """Busca una propiedad IntProperty por nombre y retorna su posición y valor"""
    nombre_bytes = nombre_propiedad.encode('ascii')
    pos_nombre = data.find(nombre_bytes)
    
    if pos_nombre == -1:
        return None, None
    
    search_start = pos_nombre
    search_end = min(pos_nombre + 200, len(data))
    chunk = data[search_start:search_end]
    
    int_prop_pos = chunk.find(b'IntProperty')
    if int_prop_pos == -1:
        return None, None
    
    abs_int_prop_pos = search_start + int_prop_pos
    
    for offset in range(12, 25):
        try:
            pos_valor = abs_int_prop_pos + offset
            if pos_valor + 4 <= len(data):
                valor = struct.unpack('<i', data[pos_valor:pos_valor + 4])[0]
                if -10000000 <= valor < 10000000:
                    return pos_valor, valor
        except:
            pass
    
    return None, None

def buscar_propiedades_en_archivo(archivo):
    """Busca propiedades de puntos en un archivo específico"""
    try:
        with open(archivo, 'rb') as f:
            data = f.read()
        
        # Buscar diferentes variantes de propiedades de puntos
        propiedades_buscar = [
            'total_points_42',
            'points_spent_43',
            'total_points',
            'points_spent',
            'TotalPoints',
            'PointsSpent',
            'Points',
            'points'
        ]
        
        resultados = {}
        for prop in propiedades_buscar:
            pos, valor = buscar_propiedad_int(data, prop)
            if pos is not None:
                resultados[prop] = {'posicion': pos, 'valor': valor}
        
        return resultados
    except Exception as e:
        return {'error': str(e)}

def main():
    saves_dir = os.path.join(os.path.expanduser("~"), "AppData", "Local", "VotV", "Saved", "SaveGames")
    
    print("="*70)
    print("  ANALIZADOR DE PUNTOS EN TODOS LOS ARCHIVOS .SAV")
    print("="*70)
    print(f"\nBuscando archivos .sav en: {saves_dir}\n")
    
    # Buscar todos los archivos .sav (excluyendo backups)
    patron = os.path.join(saves_dir, "*.sav")
    archivos = [f for f in glob.glob(patron) if not '.backup_' in f]
    
    if not archivos:
        print("[ERROR] No se encontraron archivos .sav")
        return
    
    print(f"Se encontraron {len(archivos)} archivos .sav\n")
    print("="*70)
    
    for archivo in sorted(archivos):
        nombre_archivo = os.path.basename(archivo)
        print(f"\n[{nombre_archivo}]")
        print("-" * 70)
        
        resultados = buscar_propiedades_en_archivo(archivo)
        
        if 'error' in resultados:
            print(f"   ERROR: {resultados['error']}")
        elif not resultados:
            print(f"   No se encontraron propiedades de puntos")
        else:
            for prop, datos in resultados.items():
                print(f"   {prop:25s} = {datos['valor']:>10,}")
    
    print("\n" + "="*70)
    print("Analisis completado")
    print("="*70)

if __name__ == "__main__":
    main()

