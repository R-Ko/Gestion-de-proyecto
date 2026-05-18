@echo off
REM Script de despliegue para Windows

echo.
echo Iniciando despliegue...
echo.

REM Desplegar backend en Cloudflare Workers
echo Desplegando backend...
cd backend
call npm install
call wrangler deploy --env production
cd ..

REM Desplegar frontend en GitHub Pages
echo Desplegando frontend...
cd frontend\public
git add .
git commit -m "Auto deploy: %date%"
git push origin main
cd ..\..

echo.
echo ✓ ¡Despliegue completado!
echo Frontend: https://tu-usuario.github.io/gestion-proyectos
echo Backend: https://api.tudominio.com
echo.
pause
