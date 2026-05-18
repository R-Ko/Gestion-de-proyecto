# 🚀 Guía Rápida de Instalación y Despliegue

## 1️⃣ Requisitos Previos

- Python 3.8+
- Node.js 18+
- Git
- Cuentas en: Supabase, Cloudflare, GitHub

---

## 2️⃣ Instalación Local

### Backend

```bash
# Crear entorno virtual
cd backend
python -m venv venv

# Activar (Windows)
venv\Scripts\activate
# O en macOS/Linux
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Copiar variables de entorno
cp .env.example .env

# Editar .env con tus credenciales de Supabase
# DATABASE_URL=postgresql://...
```

### Frontend

```bash
cd frontend

# Instalar dependencias (si uses Node.js)
npm install

# O simplemente servir archivos estáticos
cd public
python -m http.server 3000
```

---

## 3️⃣ Prueba Local

### Terminal 1 - Backend

```bash
cd backend
export DATABASE_URL="postgresql://user:pass@localhost/db"
python app.py
# API disponible en http://localhost:5000
```

### Terminal 2 - Frontend

```bash
cd frontend/public
python -m http.server 3000
# Frontend disponible en http://localhost:3000
```

---

## 4️⃣ Configuración de Supabase

1. **Crear proyecto:**
   - Ir a https://supabase.com → New Project
   - Llenar datos
   - Copiar "Connection String"

2. **Obtener credenciales:**
   - Ir a Settings → Database
   - Copiar URL PostgreSQL

3. **Crear .env en backend:**
   ```
   DATABASE_URL=postgresql://postgres:[PASSWORD]@[HOST]:5432/postgres
   ```

---

## 5️⃣ Despliegue en Producción

### Opción A: Cloudflare Workers (Recomendado)

```bash
# Instalar Wrangler
npm install -g wrangler

# Loguear en Cloudflare
wrangler login

# Desplegar
cd backend
wrangler deploy --env production
```

### Opción B: Heroku (Alternativa)

```bash
# Instalar Heroku CLI
npm install -g heroku

# Loguear
heroku login

# Crear app
heroku create nombre-app

# Configurar base de datos
heroku config:set DATABASE_URL="postgresql://..."

# Desplegar
git push heroku main
```

### Frontend - GitHub Pages

```bash
cd frontend/public

# Inicializar repo si no existe
git init
git remote add origin https://github.com/usuario/repo.git

# Agregar y pushear
git add .
git commit -m "Despliegue inicial"
git push -u origin main

# Habilitar GitHub Pages
# Settings → Pages → Source: main branch
```

---

## 6️⃣ Variables de Entorno en Producción

### Backend (Cloudflare)

En `wrangler.toml`:
```toml
[env.production]
vars = { 
    ENVIRONMENT = "production",
    DATABASE_URL = "postgresql://..."
}
```

### Backend (Heroku)

```bash
heroku config:set SECRET_KEY="super-secret"
heroku config:set DATABASE_URL="postgresql://..."
```

### Frontend (GitHub Pages)

En `frontend/public/app.js`:
```javascript
const API_URL = 'https://api.tudominio.com';
```

---

## 7️⃣ Estructura Final

```
proyecto/
├── backend/
│   ├── app.py               ✓
│   ├── requirements.txt     ✓
│   ├── wrangler.toml        ✓
│   ├── package.json         ✓
│   ├── .env.example         ✓
│   └── .env                 (no commitar)
│
├── frontend/
│   ├── public/
│   │   ├── index.html       ✓
│   │   ├── app.js           ✓
│   │   └── styles.css       ✓
│   ├── firebase.json        ✓
│   ├── package.json         ✓
│   └── .env.example         ✓
│
├── ARQUITECTURA_FRONTEND.md ✓
├── README.md                ✓
├── .gitignore              ✓
├── deploy.sh               ✓
└── deploy.bat              ✓
```

---

## 🔗 URLs de Referencia

- **Supabase:** https://supabase.com/docs
- **Cloudflare Workers:** https://developers.cloudflare.com/workers/
- **GitHub Pages:** https://pages.github.com/
- **Flask:** https://flask.palletsprojects.com/
- **Wrangler CLI:** https://developers.cloudflare.com/workers/wrangler/

---

## ✅ Checklist de Despliegue

- [ ] Supabase proyecto creado y credenciales copiadas
- [ ] Variables de entorno configuradas (.env)
- [ ] Backend probado localmente
- [ ] Frontend probado localmente
- [ ] GitHub repo creado
- [ ] Cloudflare account y dominio configurado
- [ ] wrangler.toml actualizado con credenciales
- [ ] Backend desplegado en Cloudflare
- [ ] Frontend desplegado en GitHub Pages
- [ ] CORS configurado correctamente
- [ ] API URL actualizada en frontend
- [ ] URLs customizadas configuradas (opcional)

---

## 🆘 Troubleshooting

### Error: "psycopg2-binary is required"
```bash
pip install psycopg2-binary
```

### Error: "CORS error"
- Verificar que tu origin esté en CORS_ALLOWED_ORIGINS
- En desarrollo: `http://localhost:3000`

### Error: "Database connection failed"
- Verificar DATABASE_URL válida
- Probar conexión: `psql $DATABASE_URL -c "SELECT 1"`

### Frontend no ve cambios
- Limpiar cache de GitHub Pages
- Esperar 5-10 minutos de propagación

---

## 📞 Soporte

Documentación completa en [ARQUITECTURA_FRONTEND.md](../ARQUITECTURA_FRONTEND.md)
