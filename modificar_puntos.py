#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script interactivo mejorado para modificar los puntos en Voice of the Void
Ahora modifica tanto data.sav como TODOS los archivos de partida individuales

NOTA: Este script corrige el problema donde los puntos no se guardaban.
Ahora modifica:
  1. data.sav (total_points_42 y points_spent_43)
  2. Todos los archivos de partida s_*.sav (propiedad Points)
"""

import struct
import os
import shutil
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
    print(f"[OK] Backup creado: {nombre_archivo}.backup_{timestamp}")
    return backup

def buscar_propiedad_int(data, nombre_propiedad):
    """Busca una propiedad IntProperty por nombre y retorna su posición y valor"""
    # Buscar el nombre de la propiedad
    nombre_bytes = nombre_propiedad.encode('ascii')
    pos_nombre = data.find(nombre_bytes)
    
    if pos_nombre == -1:
        return None, None
    
    # Buscar IntProperty después del nombre
    search_start = pos_nombre
    search_end = min(pos_nombre + 200, len(data))
    chunk = data[search_start:search_end]
    
    int_prop_pos = chunk.find(b'IntProperty')
    if int_prop_pos == -1:
        return None, None
    
    # El valor int típicamente está 12-20 bytes después de IntProperty
    abs_int_prop_pos = search_start + int_prop_pos
    
    for offset in range(12, 25):
        try:
            pos_valor = abs_int_prop_pos + offset
            if pos_valor + 4 <= len(data):
                valor = struct.unpack('<i', data[pos_valor:pos_valor + 4])[0]
                # Verificar si es un valor razonable
                if -10000000 <= valor < 10000000:
                    return pos_valor, valor
        except:
            pass
    
    return None, None

def leer_puntos(archivo):
    """Lee los puntos actuales del archivo data.sav"""
    if not os.path.exists(archivo):
        print(f"[ERROR] No se encontro el archivo {archivo}")
        return None, None
    
    with open(archivo, 'rb') as f:
        data = f.read()
    
    # Buscar total_points
    pos_total, valor_total = buscar_propiedad_int(data, 'total_points_42')
    
    # Buscar points_spent
    pos_spent, valor_spent = buscar_propiedad_int(data, 'points_spent_43')
    
    return {
        'total_points': {
            'posicion': pos_total,
            'valor': valor_total
        },
        'points_spent': {
            'posicion': pos_spent,
            'valor': valor_spent
        }
    }

def modificar_propiedad_int(data, nombre_propiedad, nuevo_valor):
    """Modifica una propiedad IntProperty en los datos"""
    pos, valor_actual = buscar_propiedad_int(data, nombre_propiedad)
    if pos is None:
        return data, False, None
    
    nuevo_bytes = struct.pack('<i', nuevo_valor)
    data[pos:pos+4] = nuevo_bytes
    return data, True, valor_actual

def modificar_save_individual(archivo, puntos):
    """Modifica un archivo de save individual (propiedad Points)"""
    if not os.path.exists(archivo):
        return False, "Archivo no encontrado"
    
    with open(archivo, 'rb') as f:
        data = bytearray(f.read())
    
    data, modificado, valor_anterior = modificar_propiedad_int(data, 'Points', puntos)
    
    if not modificado:
        return False, "No se encontró propiedad Points"
    
    hacer_backup(archivo)
    with open(archivo, 'wb') as f:
        f.write(data)
    
    return True, f"{valor_anterior} -> {puntos}"

def modificar_archivos_partida(saves_dir, puntos):
    """Modifica todos los archivos de partida individuales"""
    patron = os.path.join(saves_dir, "s_*.sav")
    archivos_save = [f for f in glob.glob(patron) if not '.backup_' in f]
    
    if not archivos_save:
        return 0
    
    modificados = 0
    for archivo_save in sorted(archivos_save):
        exito, _ = modificar_save_individual(archivo_save, puntos)
        if exito:
            modificados += 1
    
    return modificados

def modificar_puntos(archivo, nuevo_total=None, nuevo_spent=None):
    """Modifica los puntos en data.sav y en todos los archivos de partida"""
    if not os.path.exists(archivo):
        print(f"[ERROR] No se encontro el archivo {archivo}")
        return False
    
    saves_dir = os.path.dirname(archivo)
    
    # Leer valores actuales
    print("\nLeyendo valores actuales...")
    valores = leer_puntos(archivo)
    
    if valores is None:
        print("[ERROR] Error al leer los valores")
        return False
    
    print(f"\nValores actuales:")
    print(f"  Total Points: {valores['total_points']['valor']}")
    print(f"  Points Spent: {valores['points_spent']['valor']}")
    print(f"  Disponibles: {valores['total_points']['valor'] - valores['points_spent']['valor']}")
    
    if nuevo_total is None and nuevo_spent is None:
        print("\n[INFO] No se especificaron nuevos valores para modificar")
        return True
    
    # Crear backup de data.sav
    print("\nCreando backup de data.sav...")
    backup = hacer_backup(archivo)
    
    # Leer archivo
    with open(archivo, 'rb') as f:
        data = bytearray(f.read())
    
    modificaciones = 0
    
    # Modificar total_points si se especificó
    if nuevo_total is not None and valores['total_points']['posicion'] is not None:
        pos = valores['total_points']['posicion']
        nuevo_bytes = struct.pack('<i', nuevo_total)
        data[pos:pos+4] = nuevo_bytes
        print(f"[OK] Total Points: {valores['total_points']['valor']} -> {nuevo_total}")
        modificaciones += 1
    
    # Modificar points_spent si se especificó
    if nuevo_spent is not None and valores['points_spent']['posicion'] is not None:
        pos = valores['points_spent']['posicion']
        nuevo_bytes = struct.pack('<i', nuevo_spent)
        data[pos:pos+4] = nuevo_bytes
        print(f"[OK] Points Spent: {valores['points_spent']['valor']} -> {nuevo_spent}")
        modificaciones += 1
    
    if modificaciones > 0:
        # Guardar data.sav modificado
        with open(archivo, 'wb') as f:
            f.write(data)
        
        print(f"\n[OK] data.sav modificado exitosamente")
        
        # Modificar archivos de partida individuales
        if nuevo_total is not None:
            print(f"\nModificando archivos de partida...")
            puntos_disponibles = nuevo_total - valores['points_spent']['valor']
            modificados = modificar_archivos_partida(saves_dir, puntos_disponibles)
            if modificados > 0:
                print(f"[OK] {modificados} partidas modificadas con {puntos_disponibles} puntos")
        
        print(f"\nSi algo sale mal, restaura desde: {backup}")
        return True
    else:
        print("\n[AVISO] No se realizaron modificaciones")
        return False

def mostrar_menu():
    """Muestra el menú interactivo"""
    archivo = r"C:\Users\JackStar\AppData\Local\VotV\Saved\SaveGames\data.sav"
    
    print("="*60)
    print("  MODIFICADOR DE PUNTOS - VOICE OF THE VOID")
    print("="*60)
    
    if not os.path.exists(archivo):
        print(f"\n[ERROR] No se encontro data.sav en:")
        print(f"   {archivo}")
        return
    
    # Leer valores actuales
    valores = leer_puntos(archivo)
    
    if valores is None:
        print("[ERROR] Error al leer los valores del archivo")
        return
    
    print(f"\n[VALORES ACTUALES]")
    print(f"   Total Points: {valores['total_points']['valor']}")
    print(f"   Points Spent: {valores['points_spent']['valor']}")
    print(f"   Points Disponibles: {valores['total_points']['valor'] - valores['points_spent']['valor']}")
    
    print("\n" + "="*60)
    print("OPCIONES:")
    print("  1. Modificar Total Points")
    print("  2. Modificar Points Spent")
    print("  3. Establecer puntos disponibles específicos")
    print("  4. Salir")
    print("="*60)
    
    try:
        opcion = input("\nSelecciona una opción (1-4): ").strip()
        
        if opcion == "1":
            nuevo_valor = int(input("\nIngresa el nuevo valor para Total Points: "))
            modificar_puntos(archivo, nuevo_total=nuevo_valor)
        
        elif opcion == "2":
            nuevo_valor = int(input("\nIngresa el nuevo valor para Points Spent: "))
            modificar_puntos(archivo, nuevo_spent=nuevo_valor)
        
        elif opcion == "3":
            puntos_deseados = int(input("\n¿Cuántos puntos disponibles quieres tener?: "))
            # Mantener points_spent igual y ajustar total_points
            nuevo_total = valores['points_spent']['valor'] + puntos_deseados
            print(f"\nSe establecerá Total Points en {nuevo_total}")
            print(f"(Points Spent: {valores['points_spent']['valor']} + Disponibles: {puntos_deseados})")
            confirmar = input("\n¿Confirmar? (s/n): ").strip().lower()
            if confirmar == 's':
                modificar_puntos(archivo, nuevo_total=nuevo_total)
        
        elif opcion == "4":
            print("\nSaliendo...")
        
        else:
            print("\n[AVISO] Opcion no valida")
    
    except ValueError:
        print("\n[ERROR] Debes ingresar un numero entero")
    except KeyboardInterrupt:
        print("\n\nOperacion cancelada")
    except Exception as e:
        print(f"\n[ERROR] {e}")

if __name__ == "__main__":
    mostrar_menu()

