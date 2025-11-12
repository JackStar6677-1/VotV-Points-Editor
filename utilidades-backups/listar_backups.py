#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Listador de Backups de VotV
Lista todos los backups disponibles con informacion detallada

Funciona con cualquier usuario de Windows
"""

import os
import glob
from datetime import datetime

def obtener_directorio_saves():
    """Obtiene el directorio de saves de VotV del usuario actual"""
    # Usar variable de entorno LOCALAPPDATA
    localappdata = os.environ.get('LOCALAPPDATA')
    if not localappdata:
        print("ERROR: No se pudo detectar la carpeta LOCALAPPDATA")
        return None
    
    saves_dir = os.path.join(localappdata, "VotV", "Saved", "SaveGames")
    return saves_dir

def listar_backups():
    """Lista todos los backups disponibles"""
    saves_dir = obtener_directorio_saves()
    if not saves_dir:
        return
    
    backup_dir = os.path.join(saves_dir, "backups")
    
    if not os.path.exists(backup_dir):
        print("="*70)
        print("  NO HAY BACKUPS")
        print("="*70)
        print(f"\nEl directorio de backups no existe:")
        print(f"  {backup_dir}")
        print("\nLos backups se crean automaticamente al usar set_puntos.py")
        return
    
    # Buscar todos los archivos .backup_*
    patron = os.path.join(backup_dir, "*.backup_*")
    backups = glob.glob(patron)
    
    if not backups:
        print("="*70)
        print("  NO HAY BACKUPS")
        print("="*70)
        print(f"\nDirectorio: {backup_dir}")
        print("\nLos backups se crean automaticamente al usar set_puntos.py")
        return
    
    # Organizar por archivo original
    backups_por_archivo = {}
    for backup in backups:
        nombre_completo = os.path.basename(backup)
        # Separar nombre original y timestamp
        if ".backup_" in nombre_completo:
            partes = nombre_completo.split(".backup_")
            archivo_original = partes[0]
            timestamp_str = partes[1] if len(partes) > 1 else "unknown"
            
            if archivo_original not in backups_por_archivo:
                backups_por_archivo[archivo_original] = []
            
            # Obtener info del archivo
            stat = os.stat(backup)
            fecha_modificacion = datetime.fromtimestamp(stat.st_mtime)
            tamano_kb = stat.st_size / 1024
            
            backups_por_archivo[archivo_original].append({
                'ruta': backup,
                'timestamp': timestamp_str,
                'fecha': fecha_modificacion,
                'tamano': tamano_kb
            })
    
    # Mostrar resultados
    print("="*70)
    print("  BACKUPS DISPONIBLES")
    print("="*70)
    print(f"\nDirectorio: {backup_dir}")
    print(f"Total de archivos originales: {len(backups_por_archivo)}")
    print(f"Total de backups: {len(backups)}")
    print("\n" + "="*70)
    
    for archivo_original in sorted(backups_por_archivo.keys()):
        lista_backups = sorted(backups_por_archivo[archivo_original], 
                              key=lambda x: x['fecha'], 
                              reverse=True)
        
        print(f"\n[{archivo_original}] - {len(lista_backups)} backup(s)")
        print("-" * 70)
        
        for i, backup in enumerate(lista_backups, 1):
            # Marcar el mas reciente
            marca = "  [MAS RECIENTE]" if i == 1 else ""
            print(f"  {i}. {backup['timestamp']}")
            print(f"     Fecha: {backup['fecha'].strftime('%Y-%m-%d %H:%M:%S')}{marca}")
            print(f"     Tamano: {backup['tamano']:.1f} KB")
            print(f"     Ruta: {os.path.basename(backup['ruta'])}")
            if i < len(lista_backups):
                print()
    
    print("\n" + "="*70)
    print("  COMANDOS UTILES")
    print("="*70)
    print("\nPara restaurar un backup:")
    print("  python restaurar_backup.py")
    print("\nPara limpiar backups antiguos:")
    print("  python limpiar_backups_antiguos.py")
    print("="*70)

def main():
    print("="*70)
    print("  LISTADOR DE BACKUPS - VotV Points Editor")
    print("="*70)
    
    saves_dir = obtener_directorio_saves()
    if saves_dir:
        print(f"\nDirectorio de saves detectado:")
        print(f"  {saves_dir}")
        print()
    
    listar_backups()

if __name__ == "__main__":
    main()

