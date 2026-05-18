#!/bin/bash
# Script de despliegue automático

echo "🚀 Iniciando despliegue..."

# Desplegar backend en Cloudflare Workers
echo "📤 Desplegando backend..."
cd backend
npm install
wrangler deploy --env production
cd ..

# Desplegar frontend en GitHub Pages
echo "📤 Desplegando frontend..."
cd frontend/public
git add .
git commit -m "Auto deploy: $(date)"
git push origin main
cd ../..

echo "✅ ¡Despliegue completado!"
echo "Frontend: https://tu-usuario.github.io/gestion-proyectos"
echo "Backend: https://api.tudominio.com"
