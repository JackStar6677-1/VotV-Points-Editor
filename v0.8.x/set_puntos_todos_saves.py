#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script mejorado para modificar los puntos en Voice of the Void
Modifica tanto data.sav como TODOS los archivos de partida individuales

Uso: python set_puntos_todos_saves.py <puntos_deseados>
Ejemplo: python set_puntos_todos_saves.py 50000
"""

import struct
import os
import shutil
import sys
import glob
from datetime import datetime

def hacer_backup(archivo):
    """Crea una copia de seguridad del archivo en carpeta separada"""
    saves_dir = os.path.dirname(archivo)
    backup_dir = os.path.join(saves_dir, "backups")
    
    # Crear carpeta de backups si no existe
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    nombre_archivo = os.path.basename(archivo)
    backup = os.path.join(backup_dir, f"{nombre_archivo}.backup_{timestamp}")
    
    shutil.copy2(archivo, backup)
    return backup

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

def modificar_propiedad_int(data, nombre_propiedad, nuevo_valor):
    """Modifica una propiedad IntProperty en los datos"""
    pos, valor_actual = buscar_propiedad_int(data, nombre_propiedad)
    if pos is None:
        return data, False, None
    
    nuevo_bytes = struct.pack('<i', nuevo_valor)
    data[pos:pos+4] = nuevo_bytes
    return data, True, valor_actual

def modificar_data_sav(archivo, puntos_disponibles):
    """Modifica data.sav (total_points_42 y points_spent_43)"""
    if not os.path.exists(archivo):
        return False, "Archivo no encontrado"
    
    with open(archivo, 'rb') as f:
        data = bytearray(f.read())
    
    # Buscar valores actuales
    pos_spent, valor_spent = buscar_propiedad_int(data, 'points_spent_43')
    
    if pos_spent is None:
        return False, "No se encontró points_spent_43"
    
    # Calcular nuevo total
    nuevo_total = valor_spent + puntos_disponibles
    
    # Modificar total_points_42
    data, modificado, valor_anterior = modificar_propiedad_int(data, 'total_points_42', nuevo_total)
    
    if not modificado:
        return False, "No se pudo modificar total_points_42"
    
    # Crear backup y guardar
    backup = hacer_backup(archivo)
    with open(archivo, 'wb') as f:
        f.write(data)
    
    return True, f"Modificado: {valor_anterior} -> {nuevo_total}"

def modificar_save_individual(archivo, puntos):
    """Modifica un archivo de save individual (propiedad Points)"""
    if not os.path.exists(archivo):
        return False, "Archivo no encontrado"
    
    with open(archivo, 'rb') as f:
        data = bytearray(f.read())
    
    # Buscar y modificar la propiedad 'Points'
    data, modificado, valor_anterior = modificar_propiedad_int(data, 'Points', puntos)
    
    if not modificado:
        return False, "No se encontró propiedad Points"
    
    # Crear backup y guardar
    backup = hacer_backup(archivo)
    with open(archivo, 'wb') as f:
        f.write(data)
    
    return True, f"{valor_anterior} -> {puntos}"

def main():
    saves_dir = os.path.join(os.path.expanduser("~"), "AppData", "Local", "VotV", "Saved", "SaveGames")
    data_sav = os.path.join(saves_dir, "data.sav")
    
    print("="*70)
    print("  MODIFICADOR DE PUNTOS - VOICE OF THE VOID (MEJORADO)")
    print("="*70)
    
    # Verificar argumentos
    if len(sys.argv) < 2:
        print("\n[INFO] Uso: python set_puntos_todos_saves.py <puntos_deseados>")
        print("\nEjemplos:")
        print("  python set_puntos_todos_saves.py 50000   - Establecer 50,000 puntos")
        print("  python set_puntos_todos_saves.py 999999  - Establecer 999,999 puntos")
        sys.exit(0)
    
    try:
        puntos = int(sys.argv[1])
        
        if puntos < 0:
            print("\n[ERROR] Los puntos no pueden ser negativos")
            sys.exit(1)
        
        if puntos > 10000000:
            print("\n[AVISO] Valor muy alto, puede causar problemas")
        
        print(f"\n[OBJETIVO] Establecer {puntos:,} puntos en todas las partidas")
        print("="*70)
        
        # 1. Modificar data.sav
        print("\n[1/2] Modificando data.sav...")
        exito, mensaje = modificar_data_sav(data_sav, puntos)
        if exito:
            print(f"      OK: {mensaje}")
        else:
            print(f"      ERROR: {mensaje}")
        
        # 2. Modificar todos los archivos de save individuales
        print("\n[2/2] Modificando archivos de partida individuales...")
        patron = os.path.join(saves_dir, "s_*.sav")
        archivos_save = [f for f in glob.glob(patron) if not '.backup_' in f]
        
        if not archivos_save:
            print("      No se encontraron archivos de partida")
        else:
            print(f"      Se encontraron {len(archivos_save)} partidas")
            modificados = 0
            omitidos = 0
            
            for archivo in sorted(archivos_save):
                nombre = os.path.basename(archivo)
                exito, mensaje = modificar_save_individual(archivo, puntos)
                
                if exito:
                    print(f"      OK: {nombre:30s} {mensaje}")
                    modificados += 1
                else:
                    omitidos += 1
            
            print(f"\n      Total modificados: {modificados}/{len(archivos_save)}")
            if omitidos > 0:
                print(f"      NOTA: {omitidos} archivos omitidos (incompatibles con v0.9.0 alpha)")
        
        print("\n" + "="*70)
        print("[EXITO] Modificacion completada!")
        print("="*70)
        print(f"\nAhora todas tus partidas tienen {puntos:,} puntos disponibles")
        print("\nNOTA: Los backups se crearon automaticamente")
        print(f"      Ubicacion: {saves_dir}")
        
    except ValueError:
        print(f"\n[ERROR] '{sys.argv[1]}' no es un numero valido")
        sys.exit(1)
    except Exception as e:
        print(f"\n[ERROR] {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()

