#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Restaurador de Backups de VotV
Restaura backups de saves con menu interactivo

Funciona con cualquier usuario de Windows
"""

import os
import glob
import shutil
from datetime import datetime

def obtener_directorio_saves():
    """Obtiene el directorio de saves de VotV del usuario actual"""
    localappdata = os.environ.get('LOCALAPPDATA')
    if not localappdata:
        print("ERROR: No se pudo detectar la carpeta LOCALAPPDATA")
        return None
    
    saves_dir = os.path.join(localappdata, "VotV", "Saved", "SaveGames")
    return saves_dir

def listar_backups_disponibles():
    """Lista los backups y retorna diccionario organizado"""
    saves_dir = obtener_directorio_saves()
    if not saves_dir:
        return None, None
    
    backup_dir = os.path.join(saves_dir, "backups")
    
    if not os.path.exists(backup_dir):
        return saves_dir, {}
    
    patron = os.path.join(backup_dir, "*.backup_*")
    backups = glob.glob(patron)
    
    if not backups:
        return saves_dir, {}
    
    # Organizar por archivo original
    backups_por_archivo = {}
    for backup in backups:
        nombre_completo = os.path.basename(backup)
        if ".backup_" in nombre_completo:
            partes = nombre_completo.split(".backup_")
            archivo_original = partes[0]
            timestamp_str = partes[1] if len(partes) > 1 else "unknown"
            
            if archivo_original not in backups_por_archivo:
                backups_por_archivo[archivo_original] = []
            
            stat = os.stat(backup)
            fecha_modificacion = datetime.fromtimestamp(stat.st_mtime)
            
            backups_por_archivo[archivo_original].append({
                'ruta': backup,
                'timestamp': timestamp_str,
                'fecha': fecha_modificacion,
                'nombre': nombre_completo
            })
    
    # Ordenar por fecha (mas reciente primero)
    for archivo in backups_por_archivo:
        backups_por_archivo[archivo].sort(key=lambda x: x['fecha'], reverse=True)
    
    return saves_dir, backups_por_archivo

def mostrar_menu_archivos(backups_por_archivo):
    """Muestra menu de archivos originales"""
    archivos = sorted(backups_por_archivo.keys())
    
    print("\n" + "="*70)
    print("  SELECCIONA EL ARCHIVO A RESTAURAR")
    print("="*70)
    
    for i, archivo in enumerate(archivos, 1):
        count = len(backups_por_archivo[archivo])
        mas_reciente = backups_por_archivo[archivo][0]['fecha']
        print(f"  {i}. {archivo}")
        print(f"     Backups: {count} | Ultimo: {mas_reciente.strftime('%Y-%m-%d %H:%M:%S')}")
    
    print(f"\n  0. Salir")
    print("="*70)
    
    return archivos

def mostrar_menu_backups(archivo_original, lista_backups):
    """Muestra menu de backups de un archivo"""
    print("\n" + "="*70)
    print(f"  BACKUPS DE: {archivo_original}")
    print("="*70)
    
    for i, backup in enumerate(lista_backups, 1):
        marca = "  <-- MAS RECIENTE" if i == 1 else ""
        print(f"\n  {i}. {backup['timestamp']}")
        print(f"     Fecha: {backup['fecha'].strftime('%Y-%m-%d %H:%M:%S')}{marca}")
        print(f"     Archivo: {backup['nombre']}")
    
    print(f"\n  0. Volver al menu anterior")
    print("="*70)

def restaurar_backup(backup_info, archivo_destino):
    """Restaura un backup al archivo original"""
    try:
        # Crear backup del archivo actual antes de restaurar
        if os.path.exists(archivo_destino):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_actual = archivo_destino + f".before_restore_{timestamp}"
            shutil.copy2(archivo_destino, backup_actual)
            print(f"\n[SEGURIDAD] Backup del archivo actual creado:")
            print(f"  {os.path.basename(backup_actual)}")
        
        # Restaurar
        shutil.copy2(backup_info['ruta'], archivo_destino)
        
        print(f"\n[EXITO] Backup restaurado correctamente!")
        print(f"  Desde: {backup_info['nombre']}")
        print(f"  Hacia: {os.path.basename(archivo_destino)}")
        print(f"  Fecha del backup: {backup_info['fecha'].strftime('%Y-%m-%d %H:%M:%S')}")
        
        return True
        
    except Exception as e:
        print(f"\n[ERROR] No se pudo restaurar el backup: {e}")
        return False

def main():
    print("="*70)
    print("  RESTAURADOR DE BACKUPS - VotV Points Editor")
    print("="*70)
    
    saves_dir, backups_por_archivo = listar_backups_disponibles()
    
    if not saves_dir:
        return
    
    if not backups_por_archivo:
        print("\n[INFO] No hay backups disponibles")
        print(f"\nDirectorio de backups: {os.path.join(saves_dir, 'backups')}")
        print("\nLos backups se crean automaticamente al usar set_puntos.py")
        return
    
    while True:
        archivos = mostrar_menu_archivos(backups_por_archivo)
        
        try:
            opcion = input("\nSelecciona un archivo (numero): ").strip()
            
            if opcion == '0':
                print("\nSaliendo...")
                break
            
            indice = int(opcion) - 1
            if indice < 0 or indice >= len(archivos):
                print("\n[ERROR] Opcion invalida")
                continue
            
            archivo_seleccionado = archivos[indice]
            lista_backups = backups_por_archivo[archivo_seleccionado]
            
            # Menu de backups
            while True:
                mostrar_menu_backups(archivo_seleccionado, lista_backups)
                
                opcion_backup = input("\nSelecciona un backup (numero): ").strip()
                
                if opcion_backup == '0':
                    break
                
                indice_backup = int(opcion_backup) - 1
                if indice_backup < 0 or indice_backup >= len(lista_backups):
                    print("\n[ERROR] Opcion invalida")
                    continue
                
                backup_info = lista_backups[indice_backup]
                
                # Confirmar
                print("\n" + "="*70)
                print("  CONFIRMACION")
                print("="*70)
                print(f"\nVas a restaurar:")
                print(f"  {backup_info['nombre']}")
                print(f"  Fecha: {backup_info['fecha'].strftime('%Y-%m-%d %H:%M:%S')}")
                print(f"\nEsto reemplazara el archivo actual:")
                print(f"  {archivo_seleccionado}")
                print(f"\n(Se creara un backup del archivo actual antes de restaurar)")
                
                confirmar = input("\nContinuar? (s/n): ").strip().lower()
                
                if confirmar == 's':
                    archivo_destino = os.path.join(saves_dir, archivo_seleccionado)
                    if restaurar_backup(backup_info, archivo_destino):
                        print("\n[INFO] Puedes verificar cargando el juego")
                        input("\nPresiona ENTER para continuar...")
                        break
                else:
                    print("\n[CANCELADO] No se restauro el backup")
                    input("\nPresiona ENTER para continuar...")
                
        except ValueError:
            print("\n[ERROR] Ingresa un numero valido")
        except KeyboardInterrupt:
            print("\n\nSaliendo...")
            break
        except Exception as e:
            print(f"\n[ERROR] {e}")

if __name__ == "__main__":
    main()

