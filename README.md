# Gestión de Proyectos - Arquitectura Modular

## 📋 Descripción

Sistema de gestión de proyectos y tareas estilo **Odoo** con arquitectura moderna y escalable:

- **Frontend**: SPA estático en GitHub Pages  
- **Backend**: API serverless en Cloudflare Workers  
- **Base de Datos**: PostgreSQL en Supabase  

---

## 🏗️ Estructura del Proyecto

```
proyecto/
│
├── backend/                    # API Serverless (Cloudflare Workers)
│   ├── app.py                 # API Flask compatible con Workers
│   ├── wrangler.toml          # Configuración de Cloudflare
│   ├── requirements.txt       # Dependencias Python
│   ├── Procfile               # Para despliegue alternativo
│   └── package.json           # Dependencias Node.js
│
├── frontend/                   # SPA estático (GitHub Pages)
│   ├── public/
│   │   ├── index.html         # HTML principal
│   │   ├── app.js             # Lógica JavaScript
│   │   └── styles.css         # Estilos (tema oscuro Odoo)
│   ├── firebase.json          # Config Firebase Hosting
│   └── package.json
│
├── ARQUITECTURA_FRONTEND.md   # Documentación técnica completa
└── README.md                  # Este archivo
```

---

## 🚀 Despliegue

### 1️⃣ Backend - Cloudflare Workers + Supabase

#### Requisitos:
- Cuenta en [Cloudflare](https://dash.cloudflare.com)
- Cuenta en [Supabase](https://supabase.com)
- CLI instalado: `npm install -g wrangler`

#### Pasos:

1. **Crear base de datos en Supabase:**
   - Ir a https://supabase.com → Nuevo proyecto
   - Copiar `Connection String` (PostgreSQL URL)

2. **Configurar variables de entorno:**
   ```bash
   cd backend
   
   # Crear archivo .env
   echo "DATABASE_URL=postgresql://user:password@db.supabase.co:5432/postgres" > .env
   echo "SECRET_KEY=tu-clave-secreta-super-segura" >> .env
   ```

3. **Actualizar `wrangler.toml`:**
   ```toml
   [env.production]
   route = "https://api.tudominio.com/*"
   zone_id = "tu_cloudflare_zone_id"
   
   vars = { DATABASE_URL = "tu_database_url" }
   ```

4. **Desplegar en Cloudflare:**
   ```bash
   cd backend
   wrangler deploy --env production
   ```

   **Alternativa (Heroku):**
   ```bash
   heroku create nombre-app
   heroku config:set DATABASE_URL="postgresql://..."
   git push heroku main
   ```

---

### 2️⃣ Frontend - GitHub Pages

#### Requisitos:
- Cuenta en [GitHub](https://github.com)
- Git instalado

#### Pasos:

1. **Crear repositorio GitHub:**
   ```bash
   cd frontend/public
   git init
   git add .
   git commit -m "Primer commit"
   git remote add origin https://github.com/tu-usuario/gestion-proyectos.git
   git branch -M main
   git push -u origin main
   ```

2. **Configurar GitHub Pages:**
   - Ir a Settings → Pages
   - Source: Deploy from a branch
   - Branch: `main`, folder: `/(root)` o `/docs`
   - Guardar

3. **Configurar API URL (en `frontend/public/app.js`):**
   ```javascript
   const API_URL = 'https://api.tudominio.com'; // Cambiar a tu URL de Cloudflare
   ```

4. **Actualizar CORS en backend:**
   ```python
   CORS(app, resources={
       r"/api/*": {
           "origins": [
               "https://tu-usuario.github.io",
               "https://tudominio.com"
           ],
           ...
       }
   })
   ```

5. **Hacer push a GitHub:**
   ```bash
   git add frontend/public/app.js
   git commit -m "Actualizar API URL"
   git push
   ```

   El sitio estará disponible en: `https://tu-usuario.github.io/gestion-proyectos`

---

### 3️⃣ Base de Datos - Supabase

#### Configuración:

1. **Crear proyecto en Supabase:** https://supabase.com

2. **Copiar credenciales:**
   - Project URL
   - anon/public key
   - service_role key (para backend)

3. **Ejecutar script de inicialización:**
   ```bash
   psql postgresql://user:pass@db.supabase.co:5432/postgres < init_db.sql
   ```

   O desde la consola SQL de Supabase:
   ```sql
   -- Backend ejecutará automáticamente con init_db()
   ```

---

## 🔐 Variables de Entorno

### Backend (`backend/.env`)
```
DATABASE_URL=postgresql://user:pass@host/db
SECRET_KEY=tu-clave-super-secura
FLASK_ENV=production
CORS_ORIGINS=https://tu-usuario.github.io,https://tudominio.com
```

### Frontend (`frontend/public/app.js`)
```javascript
const API_URL = 'https://api.tudominio.com';
```

---

## 📱 Credenciales de Prueba

```
Email: admin@example.com
Password: admin

Email: demo@example.com
Password: demo
```

---

## 🔄 Flujo de Trabajo

### Desarrollo Local

```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
export DATABASE_URL="postgresql://local:pass@localhost/db"
python app.py  # http://localhost:5000

# Frontend (otra terminal)
cd frontend/public
python -m http.server 3000  # http://localhost:3000
```

### Testing

1. Login con credenciales de prueba
2. Ver proyectos
3. Crear nuevo proyecto
4. Crear tareas
5. Cambiar stage de tareas

---

## 🌐 Dominios Personalizados

### Cloudflare Workers + Custom Domain

1. En Cloudflare Dashboard:
   - Workers & Pages → Tu Worker → Settings
   - Routes → Agregar ruta: `api.tudominio.com/*`
   - Zone: `tudominio.com`

2. En DNS:
   - CNAME: `api` → `tu-account.workers.dev`

### GitHub Pages + Custom Domain

1. En GitHub:
   - Settings → Pages
   - Custom domain: `tudominio.com`
   - Agregar CNAME en DNS

2. En DNS (registrador):
   ```
   A: tudominio.com → 185.199.108.153
   A: tudominio.com → 185.199.109.153
   A: tudominio.com → 185.199.110.153
   A: tudominio.com → 185.199.111.153
   ```

---

## 📊 Monitoreo y Logs

### Cloudflare Workers
```bash
wrangler tail --env production
```

### Supabase
- Dashboard → Logs
- Analytics → Performance

### GitHub Pages
- Settings → Pages → Visit site
- GitHub Actions para CI/CD

---

## 🔧 Troubleshooting

### CORS errors en frontend
```javascript
// En backend/app.py
CORS(app, origins=["*"])  # Para desarrollo
```

### Base de datos no conecta
```bash
# Verificar conexión
psql $DATABASE_URL -c "SELECT 1"
```

### GitHub Pages no actualiza
```bash
# Limpiar cache
git add .
git commit -m "Update" --allow-empty
git push
```

---

## 📚 Documentación Completa

Ver [ARQUITECTURA_FRONTEND.md](./ARQUITECTURA_FRONTEND.md) para:
- Estructura de base de datos
- Flujos de autenticación
- Rutas API
- Mejoras de UX/Frontend sugeridas

---

## 🚀 Próximos Pasos

- [ ] Implementar drag & drop en tareas
- [ ] Añadir gráficos de progreso
- [ ] Notificaciones en tiempo real (WebSockets)
- [ ] Exportar reportes (PDF/Excel)
- [ ] Integración con servicios (Slack, Teams)
- [ ] Mobile app nativa
- [ ] Dark/Light mode switcher
- [ ] Búsqueda avanzada con filtros

---

## 📝 Licencia

MIT License - Libre para usar y modificar

---

## 👥 Soporte

Para reportar problemas o sugerencias, crear un issue en el repositorio GitHub.
