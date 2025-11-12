@echo off
REM Script de prueba rápida para VotV Points Editor
REM Establece 50,000 puntos en todas las partidas

echo ====================================
echo VotV Points Editor - Prueba Rapida
echo ====================================
echo.
echo Este script establecera 50,000 puntos en todas tus partidas
echo.
pause

python set_puntos.py 50000

echo.
echo ====================================
echo Presiona cualquier tecla para salir
pause > nul

