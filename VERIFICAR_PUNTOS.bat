@echo off
REM Script para verificar los puntos en todos los archivos de save

echo ====================================
echo VotV Points Editor - Verificacion
echo ====================================
echo.
echo Analizando todos los archivos .sav...
echo.

python buscar_puntos_todos_saves.py

echo.
echo ====================================
echo Presiona cualquier tecla para salir
pause > nul

