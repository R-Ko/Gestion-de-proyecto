# 🔐 Configuración de Secrets en GitHub

Para que los GitHub Actions funcionen correctamente, necesitas configurar los secrets siguientes:

## 📝 Pasos para Agregar Secrets

1. Ir a tu repositorio en GitHub
2. Settings → Secrets and variables → Actions
3. Click en "New repository secret"
4. Agregar cada secret con el nombre y valor

---

## 🔑 Secrets Requeridos

### Para Backend (Cloudflare Workers)

#### 1. CLOUDFLARE_API_TOKEN
- Ir a Cloudflare Dashboard → Account → API Tokens
- Click en "Create Token"
- Usar template: "Edit Cloudflare Workers"
- Copiar el token generado
- Pegar en GitHub como `CLOUDFLARE_API_TOKEN`

```bash
# Ejemplo:
CLOUDFLARE_API_TOKEN=v1.0d3b3f2c1a9e8d7c6b5a4f3e2d1c0b...
```

#### 2. CLOUDFLARE_ACCOUNT_ID
- En Cloudflare Dashboard → Workers → Inicio
- Copiar "Account ID" (parte derecha)

```bash
# Ejemplo:
CLOUDFLARE_ACCOUNT_ID=a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6
```

#### 3. DATABASE_URL (en backend/.env)
- De Supabase → Settings → Database → Connection string
- IMPORTANTE: No es un GitHub secret, va en el archivo `.env`

---

### Para Frontend (GitHub Pages)

✅ **GitHub Pages funciona automáticamente** con la rama `main`

No requiere secrets adicionales, pero asegúrate de:
1. Settings → Pages → Source = Deploy from a branch
2. Branch: `main`, folder: `/(root)` o `/frontend/public`

---

## 🚀 Variables de Entorno en Backend

Archivo: `backend/.env` (no se sube a GitHub)

```env
# Base de Datos
DATABASE_URL=postgresql://[USER]:[PASSWORD]@[HOST]:5432/postgres

# Seguridad
SECRET_KEY=tu-clave-muy-secura-aqui

# Entorno
FLASK_ENV=production
PORT=5000

# CORS
CORS_ALLOWED_ORIGINS=https://tu-usuario.github.io,https://api.tudominio.com
```

---

## 🔗 Variables en Frontend

Archivo: `frontend/public/app.js`

```javascript
// Cambiar en desarrollo vs producción
const API_URL = process.env.API_URL || 'https://api.tudominio.com';
const isDevelopment = window.location.hostname === 'localhost';
```

---

## ✅ Verificar que los Secrets Están Configurados

Ir a Settings → Secrets → Actions
Deberías ver:
- ✓ CLOUDFLARE_API_TOKEN
- ✓ CLOUDFLARE_ACCOUNT_ID

---

## 🔄 Flujo de Despliegue Automático

Cuando haces `git push` a `main`:

1. **Backend** (`backend/**` cambia):
   - ✅ GitHub Action detecta cambios
   - ✅ Instala dependencias
   - ✅ Usa secrets para autenticarse en Cloudflare
   - ✅ Despliega en Cloudflare Workers
   - ✅ API disponible en https://api.tudominio.com

2. **Frontend** (`frontend/public/**` cambia):
   - ✅ GitHub Action detecta cambios
   - ✅ Copia archivos a GitHub Pages
   - ✅ Publica en https://tu-usuario.github.io

---

## 🛠️ Troubleshooting

### Error: "Invalid token"
- Verificar que el CLOUDFLARE_API_TOKEN sea válido
- Regenerar en Cloudflare si es necesario

### Error: "Unauthorized"
- Verificar que el ACCOUNT_ID sea correcto
- Copiar solo el ID, sin espacios

### No se actualiza GitHub Pages
- Esperar 1-2 minutos
- Limpiar cache del navegador (Ctrl+Shift+Del)
- Verificar que los archivos están en `frontend/public/`

### Backend no responde después de deploy
- Verificar logs: `wrangler tail --env production`
- Verificar DATABASE_URL es válida
- Intentar despliegue manual: `wrangler deploy`

---

## 📚 Documentación Adicional

- [Cloudflare API Tokens](https://developers.cloudflare.com/fundamentals/api/get-started/create-token/)
- [GitHub Secrets](https://docs.github.com/en/actions/security-guides/encrypted-secrets)
- [GitHub Pages Deployment](https://github.blog/changelog/2022-07-27-github-pages-now-uses-actions-by-default/)

---

## 🎯 Resumen Rápido

1. **Cloudflare**: Crear API Token y Account ID
2. **GitHub**: Agregar secrets en Settings
3. **Backend**: Variables en `.env`
4. **Frontend**: URL de API en `app.js`
5. **Push**: Git push y se despliega automáticamente ✅
