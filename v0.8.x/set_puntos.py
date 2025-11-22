#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script mejorado para modificar los puntos en Voice of the Void
Modifica tanto data.sav como TODOS los archivos de partida individuales

Uso: python set_puntos.py <puntos_deseados>
Ejemplo: python set_puntos.py 50000

NOTA: Este script ahora modifica:
  1. data.sav (total_points_42 y points_spent_43)
  2. Todos los archivos de partida s_*.sav (propiedad Points)
  
MEJORAS:
  - Identifica y prioriza el save activo (mas reciente)
  - Crea backups solo una vez al inicio
  - Corrige calculo de puntos para evitar valores negativos incorrectos
"""

import struct
import os
import shutil
import sys
import glob
from datetime import datetime

# Variable global para rastrear si ya se creo un backup en esta sesion
_backups_creados = set()

def hacer_backup(archivo, mostrar_mensaje=True):
    """Crea una copia de seguridad del archivo solo si no se ha hecho backup en esta sesion"""
    # Evitar crear backups duplicados en la misma sesion
    if archivo in _backups_creados:
        return None
    
    saves_dir = os.path.dirname(archivo)
    backup_dir = os.path.join(saves_dir, "backups")
    
    # Crear carpeta de backups si no existe
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    nombre_archivo = os.path.basename(archivo)
    backup = os.path.join(backup_dir, f"{nombre_archivo}.backup_{timestamp}")
    
    shutil.copy2(archivo, backup)
    _backups_creados.add(archivo)
    
    if mostrar_mensaje:
        print(f"[OK] Backup creado: {nombre_archivo}.backup_{timestamp}")
    return backup

def identificar_save_activo(saves_dir):
    """Identifica el save mas reciente (activo) basado en fecha de modificacion"""
    patron = os.path.join(saves_dir, "s_*.sav")
    archivos_save = [f for f in glob.glob(patron) if not '.backup_' in f]
    
    if not archivos_save:
        return None
    
    # Ordenar por fecha de modificacion (mas reciente primero)
    archivos_save.sort(key=lambda x: os.path.getmtime(x), reverse=True)
    
    return archivos_save[0]

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
                # Permitir valores negativos grandes (hasta -2,147,483,648) y positivos razonables
                if -2147483648 <= valor <= 2147483647:
                    return pos_valor, valor
        except:
            pass
    
    return None, None

def leer_puntos(archivo):
    """Lee los puntos actuales del archivo data.sav"""
    if not os.path.exists(archivo):
        print(f"[ERROR] No se encontro el archivo {archivo}")
        return None
    
    with open(archivo, 'rb') as f:
        data = f.read()
    
    pos_total, valor_total = buscar_propiedad_int(data, 'total_points_42')
    pos_spent, valor_spent = buscar_propiedad_int(data, 'points_spent_43')
    
    return {
        'total_points': {'posicion': pos_total, 'valor': valor_total},
        'points_spent': {'posicion': pos_spent, 'valor': valor_spent}
    }

def modificar_propiedad_int(data, nombre_propiedad, nuevo_valor):
    """Modifica una propiedad IntProperty en los datos"""
    pos, valor_actual = buscar_propiedad_int(data, nombre_propiedad)
    if pos is None:
        return data, False, None
    
    nuevo_bytes = struct.pack('<i', nuevo_valor)
    data[pos:pos+4] = nuevo_bytes
    return data, True, valor_actual

def modificar_save_individual(archivo, puntos, crear_backup=True):
    """Modifica un archivo de save individual (propiedad Points)"""
    if not os.path.exists(archivo):
        return False, "Archivo no encontrado"
    
    with open(archivo, 'rb') as f:
        data = bytearray(f.read())
    
    # Buscar y modificar la propiedad 'Points'
    data, modificado, valor_anterior = modificar_propiedad_int(data, 'Points', puntos)
    
    if not modificado:
        return False, "No se encontró propiedad Points"
    
    # Crear backup solo si se solicita (evitar duplicados)
    if crear_backup:
        hacer_backup(archivo, mostrar_mensaje=False)
    
    with open(archivo, 'wb') as f:
        f.write(data)
    
    return True, f"{valor_anterior} -> {puntos}"

def establecer_puntos_disponibles(archivo, puntos_disponibles):
    """Establece los puntos disponibles del jugador en TODOS los saves"""
    
    saves_dir = os.path.dirname(archivo)
    
    # Limpiar lista de backups creados para esta sesion
    _backups_creados.clear()
    
    print("\n[1/4] Leyendo data.sav...")
    valores = leer_puntos(archivo)
    
    if valores is None or valores['total_points']['valor'] is None:
        print("[ERROR] No se pudieron leer los valores")
        return False
    
    total_actual = valores['total_points']['valor']
    spent_actual = valores['points_spent']['valor']
    disponibles_actuales = total_actual - spent_actual
    
    print(f"\n      Total Points: {total_actual:,}")
    print(f"      Points Spent: {spent_actual:,}")
    print(f"      Disponibles: {disponibles_actuales:,}")
    
    # Calcular nuevo total - asegurar que no sea negativo
    nuevo_total = spent_actual + puntos_disponibles
    
    # Validar que el nuevo total no cause overflow
    if nuevo_total > 2147483647:  # Maximo valor int32
        # Ajustar automaticamente al maximo posible
        puntos_disponibles_ajustados = 2147483647 - spent_actual
        if puntos_disponibles_ajustados < 0:
            print(f"\n[ERROR] No es posible establecer puntos disponibles con el valor actual de Points Spent ({spent_actual:,})")
            print(f"        Points Spent es demasiado alto")
            return False
        print(f"\n[AVISO] El valor solicitado excede el maximo permitido")
        print(f"        Ajustando automaticamente a: {puntos_disponibles_ajustados:,} puntos disponibles")
        puntos_disponibles = puntos_disponibles_ajustados
        nuevo_total = 2147483647
    
    print(f"\n      Nuevo valor: {puntos_disponibles:,} puntos disponibles")
    print(f"      Nuevo Total Points: {nuevo_total:,}")
    
    # Identificar save activo
    print(f"\n[2/4] Identificando save activo...")
    save_activo = identificar_save_activo(saves_dir)
    if save_activo:
        nombre_activo = os.path.basename(save_activo)
        fecha_activo = datetime.fromtimestamp(os.path.getmtime(save_activo))
        print(f"      Save activo: {nombre_activo}")
        print(f"      Ultima modificacion: {fecha_activo.strftime('%Y-%m-%d %H:%M:%S')}")
    else:
        print(f"      No se encontro save activo")
    
    # Crear backups una sola vez al inicio
    print(f"\n[3/4] Creando backups...")
    hacer_backup(archivo)  # Backup de data.sav
    
    # Crear backups de saves individuales (solo una vez)
    patron = os.path.join(saves_dir, "s_*.sav")
    archivos_save = [f for f in glob.glob(patron) if not '.backup_' in f]
    
    if archivos_save:
        print(f"      Creando backups de {len(archivos_save)} saves individuales...")
        for archivo_save in archivos_save:
            hacer_backup(archivo_save, mostrar_mensaje=False)
        print(f"      OK: Backups creados")
    
    # Modificar data.sav
    with open(archivo, 'rb') as f:
        data = bytearray(f.read())
    
    pos = valores['total_points']['posicion']
    nuevo_bytes = struct.pack('<i', nuevo_total)
    data[pos:pos+4] = nuevo_bytes
    
    with open(archivo, 'wb') as f:
        f.write(data)
    
    print(f"      OK: data.sav modificado (Total Points: {total_actual:,} -> {nuevo_total:,})")
    
    # Modificar archivos de partida individuales
    print(f"\n[4/4] Modificando archivos de partida...")
    
    if archivos_save:
        # Ordenar: save activo primero, luego los demas
        if save_activo and save_activo in archivos_save:
            archivos_save.remove(save_activo)
            archivos_save.insert(0, save_activo)
        
        modificados = 0
        omitidos = 0
        
        for archivo_save in archivos_save:
            nombre = os.path.basename(archivo_save)
            es_activo = (archivo_save == save_activo)
            
            # No crear backup individual (ya se crearon al inicio)
            exito, mensaje = modificar_save_individual(archivo_save, puntos_disponibles, crear_backup=False)
            
            if exito:
                modificados += 1
                if es_activo:
                    print(f"      [PRIORIDAD] {nombre:30s} {mensaje}")
                else:
                    print(f"      OK: {nombre:30s} {mensaje}")
            else:
                omitidos += 1
                print(f"      ERROR: {nombre:30s} {mensaje}")
        
        print(f"\n      Total: {modificados} partidas modificadas")
        if omitidos > 0:
            print(f"      NOTA: {omitidos} partidas omitidas (incompatibles)")
    else:
        print(f"      No se encontraron partidas individuales")
    
    print(f"\n{'='*60}")
    print(f"[EXITO] Puntos modificados en todos los saves!")
    print(f"{'='*60}")
    print(f"\nAhora tienes {puntos_disponibles:,} puntos en todas tus partidas")
    if save_activo:
        print(f"\nSave activo ({os.path.basename(save_activo)}) modificado con prioridad")
    print(f"\nBackups creados en: {os.path.join(saves_dir, 'backups')}")
    
    return True

if __name__ == "__main__":
    saves_dir = os.path.join(os.path.expanduser("~"), "AppData", "Local", "VotV", "Saved", "SaveGames")
    archivo = os.path.join(saves_dir, "data.sav")
    
    print("="*60)
    print("  MODIFICADOR DE PUNTOS - VOICE OF THE VOID")
    print("="*60)
    
    if not os.path.exists(archivo):
        print(f"\n[ERROR] No se encontro data.sav")
        print(f"Ruta esperada: {archivo}")
        sys.exit(1)
    
    # Leer valores actuales primero
    valores = leer_puntos(archivo)
    if valores:
        print(f"\n[INFO] Valores actuales:")
        print(f"       Total Points: {valores['total_points']['valor']}")
        print(f"       Points Spent: {valores['points_spent']['valor']}")
        print(f"       Disponibles: {valores['total_points']['valor'] - valores['points_spent']['valor']}")
    
    # Verificar si se pasó un argumento
    if len(sys.argv) < 2:
        print(f"\n[INFO] Uso: python set_puntos.py <puntos_deseados>")
        print(f"\nEjemplos:")
        print(f"  python set_puntos.py 50000   - Establecer 50,000 puntos")
        print(f"  python set_puntos.py 999999  - Establecer 999,999 puntos")
        print(f"  python set_puntos.py 0       - Establecer 0 puntos")
        sys.exit(0)
    
    try:
        puntos = int(sys.argv[1])
        
        if puntos < 0:
            print(f"\n[ERROR] Los puntos no pueden ser negativos")
            sys.exit(1)
        
        if puntos > 10000000:
            print(f"\n[AVISO] {puntos} puntos es un valor muy alto")
            print(f"         Esto podria causar problemas en el juego")
        
        establecer_puntos_disponibles(archivo, puntos)
        
    except ValueError:
        print(f"\n[ERROR] '{sys.argv[1]}' no es un numero valido")
        print(f"[INFO] Uso: python set_puntos.py <numero>")
        sys.exit(1)
    except Exception as e:
        print(f"\n[ERROR] {e}")
        sys.exit(1)

