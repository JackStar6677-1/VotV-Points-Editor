#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script EXPERIMENTAL para VotV 0.9.0 alpha (UNSTABLE)

ADVERTENCIA: La versión 0.9.0 alpha tiene una estructura de guardado diferente.
Este script solo modifica data.sav. Los archivos de partida individuales
de v0.9 tienen estructura desconocida.

Uso: python set_puntos_v09.py <puntos_deseados>
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
    
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    nombre_archivo = os.path.basename(archivo)
    backup = os.path.join(backup_dir, f"{nombre_archivo}.backup_{timestamp}")
    
    shutil.copy2(archivo, backup)
    print(f"[OK] Backup creado: {nombre_archivo}.backup_{timestamp}")
    return backup

def buscar_propiedad_int(data, nombre_propiedad):
    """Busca una propiedad IntProperty por nombre"""
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

def leer_puntos(archivo):
    """Lee los puntos actuales de data.sav"""
    if not os.path.exists(archivo):
        return None
    
    with open(archivo, 'rb') as f:
        data = f.read()
    
    pos_total, valor_total = buscar_propiedad_int(data, 'total_points_42')
    pos_spent, valor_spent = buscar_propiedad_int(data, 'points_spent_43')
    
    return {
        'total_points': {'posicion': pos_total, 'valor': valor_total},
        'points_spent': {'posicion': pos_spent, 'valor': valor_spent}
    }

def establecer_puntos_data_sav(archivo, puntos_disponibles):
    """Modifica SOLO data.sav (archivos de partida v0.9 no soportados aún)"""
    
    print("\n[1/2] Leyendo data.sav...")
    valores = leer_puntos(archivo)
    
    if valores is None or valores['total_points']['valor'] is None:
        print("[ERROR] No se pudieron leer los valores")
        return False
    
    print(f"\n      Total Points: {valores['total_points']['valor']}")
    print(f"      Points Spent: {valores['points_spent']['valor']}")
    print(f"      Disponibles: {valores['total_points']['valor'] - valores['points_spent']['valor']}")
    
    nuevo_total = valores['points_spent']['valor'] + puntos_disponibles
    
    print(f"\n      Nuevo valor: {puntos_disponibles} puntos disponibles")
    
    print(f"\n[2/2] Modificando data.sav...")
    hacer_backup(archivo)
    
    with open(archivo, 'rb') as f:
        data = bytearray(f.read())
    
    pos = valores['total_points']['posicion']
    nuevo_bytes = struct.pack('<i', nuevo_total)
    data[pos:pos+4] = nuevo_bytes
    
    with open(archivo, 'wb') as f:
        f.write(data)
    
    print(f"      OK: Total Points establecido en {nuevo_total}")
    
    print(f"\n{'='*70}")
    print(f"[EXITO] data.sav modificado!")
    print(f"{'='*70}")
    print(f"\nPuntos establecidos en data.sav: {puntos_disponibles}")
    print(f"\n⚠️  ADVERTENCIA: Los archivos de partida de v0.9.0 alpha")
    print(f"    tienen estructura desconocida y NO fueron modificados.")
    print(f"    Los puntos pueden NO reflejarse en el juego.")
    
    return True

if __name__ == "__main__":
    archivo = r"C:\Users\JackStar\AppData\Local\VotV\Saved\SaveGames\data.sav"
    
    print("="*70)
    print("  VotV Points Editor - VERSION 0.9.0 ALPHA (EXPERIMENTAL)")
    print("="*70)
    
    if not os.path.exists(archivo):
        print(f"\n[ERROR] No se encontro data.sav")
        print(f"Ruta esperada: {archivo}")
        sys.exit(1)
    
    valores = leer_puntos(archivo)
    if valores:
        print(f"\n[INFO] Valores actuales:")
        print(f"       Total Points: {valores['total_points']['valor']}")
        print(f"       Points Spent: {valores['points_spent']['valor']}")
        print(f"       Disponibles: {valores['total_points']['valor'] - valores['points_spent']['valor']}")
    
    if len(sys.argv) < 2:
        print(f"\n[INFO] Uso: python set_puntos_v09.py <puntos_deseados>")
        print(f"\nEjemplos:")
        print(f"  python set_puntos_v09.py 50000")
        print(f"  python set_puntos_v09.py 999999")
        sys.exit(0)
    
    try:
        puntos = int(sys.argv[1])
        
        if puntos < 0:
            print(f"\n[ERROR] Los puntos no pueden ser negativos")
            sys.exit(1)
        
        establecer_puntos_data_sav(archivo, puntos)
        
    except ValueError:
        print(f"\n[ERROR] '{sys.argv[1]}' no es un numero valido")
        sys.exit(1)
    except Exception as e:
        print(f"\n[ERROR] {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

