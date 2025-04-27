@echo off
title Iniciando Proyecto Inventario
color 0A

echo ================================
echo    INICIANDO PROYECTO...
echo ================================

cd /d C:\Users\Jos\Downloads\FinalProject\ProyectoInventario\WEBSITE
echo Levantando servidor Django...
start /b python manage.py runserver

cd client
echo Levantando servidor React...
start /b npm run dev

echo Esperando que los servidores arranquen...
timeout /t 5 >nul

echo Abriendo navegador...
start http://localhost:5173/Inicio

echo ================================
echo       ¡Todo listo! 🚀
echo ================================
pause
