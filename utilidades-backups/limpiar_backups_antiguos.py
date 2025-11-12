#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Limpiador de Backups Antiguos de VotV
Permite eliminar backups viejos para liberar espacio

Funciona con cualquier usuario de Windows
"""

import os
import glob
from datetime import datetime, timedelta

def obtener_directorio_saves():
    """Obtiene el directorio de saves de VotV del usuario actual"""
    localappdata = os.environ.get('LOCALAPPDATA')
    if not localappdata:
        print("ERROR: No se pudo detectar la carpeta LOCALAPPDATA")
        return None
    
    saves_dir = os.path.join(localappdata, "VotV", "Saved", "SaveGames")
    return saves_dir

def obtener_backups_con_info():
    """Obtiene todos los backups con su informacion"""
    saves_dir = obtener_directorio_saves()
    if not saves_dir:
        return None, []
    
    backup_dir = os.path.join(saves_dir, "backups")
    
    if not os.path.exists(backup_dir):
        return backup_dir, []
    
    patron = os.path.join(backup_dir, "*.backup_*")
    backups = glob.glob(patron)
    
    info_backups = []
    for backup in backups:
        stat = os.stat(backup)
        fecha = datetime.fromtimestamp(stat.st_mtime)
        tamano_mb = stat.st_size / (1024 * 1024)
        
        info_backups.append({
            'ruta': backup,
            'nombre': os.path.basename(backup),
            'fecha': fecha,
            'tamano_mb': tamano_mb
        })
    
    # Ordenar por fecha (mas antiguos primero)
    info_backups.sort(key=lambda x: x['fecha'])
    
    return backup_dir, info_backups

def mostrar_estadisticas(backups):
    """Muestra estadisticas generales"""
    if not backups:
        return
    
    total_tamano = sum(b['tamano_mb'] for b in backups)
    fecha_mas_antigua = backups[0]['fecha']
    fecha_mas_reciente = backups[-1]['fecha']
    
    print("\n" + "="*70)
    print("  ESTADISTICAS")
    print("="*70)
    print(f"\nTotal de backups: {len(backups)}")
    print(f"Espacio total: {total_tamano:.2f} MB")
    print(f"Backup mas antiguo: {fecha_mas_antigua.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Backup mas reciente: {fecha_mas_reciente.strftime('%Y-%m-%d %H:%M:%S')}")

def filtrar_por_antiguedad(backups, dias):
    """Filtra backups mas antiguos que X dias"""
    fecha_limite = datetime.now() - timedelta(days=dias)
    return [b for b in backups if b['fecha'] < fecha_limite]

def menu_principal(backups):
    """Menu principal de opciones"""
    print("\n" + "="*70)
    print("  OPCIONES DE LIMPIEZA")
    print("="*70)
    print("\n  1. Eliminar backups mas antiguos que X dias")
    print("  2. Mantener solo los N backups mas recientes (por archivo)")
    print("  3. Eliminar TODOS los backups (peligroso)")
    print("  4. Ver lista detallada de backups")
    print("\n  0. Salir")
    print("="*70)

def eliminar_por_antiguedad(backups):
    """Elimina backups mas antiguos que X dias"""
    print("\n" + "="*70)
    print("  ELIMINAR POR ANTIGUEDAD")
    print("="*70)
    
    try:
        dias = int(input("\nDias de antiguedad (ej: 7, 14, 30): ").strip())
        
        if dias <= 0:
            print("\n[ERROR] El numero debe ser positivo")
            return
        
        antiguos = filtrar_por_antiguedad(backups, dias)
        
        if not antiguos:
            print(f"\n[INFO] No hay backups mas antiguos que {dias} dias")
            return
        
        espacio_total = sum(b['tamano_mb'] for b in antiguos)
        
        print(f"\n[INFO] Se encontraron {len(antiguos)} backups mas antiguos que {dias} dias")
        print(f"[INFO] Espacio a liberar: {espacio_total:.2f} MB")
        
        print("\nBackups que seran eliminados:")
        for i, backup in enumerate(antiguos[:10], 1):
            print(f"  {i}. {backup['nombre']}")
            print(f"     Fecha: {backup['fecha'].strftime('%Y-%m-%d %H:%M:%S')}")
        
        if len(antiguos) > 10:
            print(f"  ... y {len(antiguos) - 10} mas")
        
        confirmar = input(f"\nEliminar {len(antiguos)} backup(s)? (s/n): ").strip().lower()
        
        if confirmar == 's':
            eliminados = 0
            for backup in antiguos:
                try:
                    os.remove(backup['ruta'])
                    eliminados += 1
                except Exception as e:
                    print(f"[ERROR] No se pudo eliminar {backup['nombre']}: {e}")
            
            print(f"\n[EXITO] {eliminados} backup(s) eliminados")
            print(f"[INFO] Espacio liberado: {espacio_total:.2f} MB")
        else:
            print("\n[CANCELADO] No se eliminaron backups")
    
    except ValueError:
        print("\n[ERROR] Ingresa un numero valido")

def mantener_n_recientes(backups):
    """Mantiene solo los N backups mas recientes por archivo"""
    print("\n" + "="*70)
    print("  MANTENER N MAS RECIENTES POR ARCHIVO")
    print("="*70)
    
    try:
        n = int(input("\nCuantos backups mantener por archivo? (ej: 3, 5, 10): ").strip())
        
        if n <= 0:
            print("\n[ERROR] El numero debe ser positivo")
            return
        
        # Organizar por archivo original
        por_archivo = {}
        for backup in backups:
            nombre = backup['nombre']
            if ".backup_" in nombre:
                archivo_original = nombre.split(".backup_")[0]
                if archivo_original not in por_archivo:
                    por_archivo[archivo_original] = []
                por_archivo[archivo_original].append(backup)
        
        # Para cada archivo, ordenar por fecha y marcar los que sobran
        a_eliminar = []
        for archivo, lista in por_archivo.items():
            lista_ordenada = sorted(lista, key=lambda x: x['fecha'], reverse=True)
            if len(lista_ordenada) > n:
                a_eliminar.extend(lista_ordenada[n:])
        
        if not a_eliminar:
            print(f"\n[INFO] Todos los archivos tienen {n} o menos backups")
            return
        
        espacio_total = sum(b['tamano_mb'] for b in a_eliminar)
        
        print(f"\n[INFO] Se eliminaran {len(a_eliminar)} backups")
        print(f"[INFO] Espacio a liberar: {espacio_total:.2f} MB")
        print(f"[INFO] Se mantendran los {n} backups mas recientes de cada archivo")
        
        confirmar = input(f"\nEliminar {len(a_eliminar)} backup(s)? (s/n): ").strip().lower()
        
        if confirmar == 's':
            eliminados = 0
            for backup in a_eliminar:
                try:
                    os.remove(backup['ruta'])
                    eliminados += 1
                except Exception as e:
                    print(f"[ERROR] No se pudo eliminar {backup['nombre']}: {e}")
            
            print(f"\n[EXITO] {eliminados} backup(s) eliminados")
            print(f"[INFO] Espacio liberado: {espacio_total:.2f} MB")
        else:
            print("\n[CANCELADO] No se eliminaron backups")
    
    except ValueError:
        print("\n[ERROR] Ingresa un numero valido")

def eliminar_todos(backups):
    """Elimina TODOS los backups (con confirmacion multiple)"""
    print("\n" + "="*70)
    print("  ELIMINAR TODOS LOS BACKUPS - PELIGROSO")
    print("="*70)
    
    espacio_total = sum(b['tamano_mb'] for b in backups)
    
    print(f"\n[ADVERTENCIA] Vas a eliminar TODOS los backups ({len(backups)} archivos)")
    print(f"[ADVERTENCIA] Espacio a liberar: {espacio_total:.2f} MB")
    print(f"[ADVERTENCIA] Esta accion NO se puede deshacer")
    
    confirmar1 = input("\nEstas seguro? (s/n): ").strip().lower()
    if confirmar1 != 's':
        print("\n[CANCELADO]")
        return
    
    confirmar2 = input("Estas REALMENTE seguro? Escribe 'ELIMINAR TODO': ").strip()
    if confirmar2 != "ELIMINAR TODO":
        print("\n[CANCELADO]")
        return
    
    eliminados = 0
    for backup in backups:
        try:
            os.remove(backup['ruta'])
            eliminados += 1
        except Exception as e:
            print(f"[ERROR] No se pudo eliminar {backup['nombre']}: {e}")
    
    print(f"\n[EXITO] {eliminados} backup(s) eliminados")
    print(f"[INFO] Espacio liberado: {espacio_total:.2f} MB")

def ver_lista_detallada(backups):
    """Muestra lista detallada de todos los backups"""
    print("\n" + "="*70)
    print("  LISTA DETALLADA DE BACKUPS")
    print("="*70)
    
    for i, backup in enumerate(backups, 1):
        print(f"\n{i}. {backup['nombre']}")
        print(f"   Fecha: {backup['fecha'].strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"   Tamano: {backup['tamano_mb']:.2f} MB")
    
    input("\nPresiona ENTER para continuar...")

def main():
    print("="*70)
    print("  LIMPIADOR DE BACKUPS - VotV Points Editor")
    print("="*70)
    
    backup_dir, backups = obtener_backups_con_info()
    
    if backup_dir is None:
        return
    
    if not backups:
        print("\n[INFO] No hay backups para limpiar")
        print(f"\nDirectorio de backups: {backup_dir}")
        return
    
    print(f"\nDirectorio de backups: {backup_dir}")
    mostrar_estadisticas(backups)
    
    while True:
        menu_principal(backups)
        
        try:
            opcion = input("\nSelecciona una opcion: ").strip()
            
            if opcion == '0':
                print("\nSaliendo...")
                break
            elif opcion == '1':
                eliminar_por_antiguedad(backups)
                # Recargar backups
                backup_dir, backups = obtener_backups_con_info()
                if backups:
                    mostrar_estadisticas(backups)
            elif opcion == '2':
                mantener_n_recientes(backups)
                # Recargar backups
                backup_dir, backups = obtener_backups_con_info()
                if backups:
                    mostrar_estadisticas(backups)
            elif opcion == '3':
                eliminar_todos(backups)
                # Recargar backups
                backup_dir, backups = obtener_backups_con_info()
                if backups:
                    mostrar_estadisticas(backups)
                else:
                    print("\n[INFO] No quedan backups")
                    break
            elif opcion == '4':
                ver_lista_detallada(backups)
            else:
                print("\n[ERROR] Opcion invalida")
        
        except KeyboardInterrupt:
            print("\n\nSaliendo...")
            break
        except Exception as e:
            print(f"\n[ERROR] {e}")

if __name__ == "__main__":
    main()

