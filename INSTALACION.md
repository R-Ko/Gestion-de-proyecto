# 🚀 Guía Rápida de Instalación y Despliegue

## 1️⃣ Requisitos Previos

- Python 3.8+
- Node.js 18+
- Git
- Cuentas en: Aiven, Render, Vercel, GitHub

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

# Editar .env con tus credenciales de Aiven
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

### Opción 1 - Ejecutar la aplicación monolítica local

```bash
cd "c:\Users\IamMiyuki\Desktop\Gestion de proyecto"
.venv\Scripts\python.exe app.py
```

Abre `http://localhost:5000` en el navegador. Esta opción usa la base de datos local SQLite `users.db`.

### Opción 2 - Backend y frontend por separado

```bash
cd backend
.venv\Scripts\python.exe app.py
```

En otra terminal:

```bash
cd frontend/public
python -m http.server 3000
```

Abre `http://localhost:3000` para acceder al frontend conectado al backend local.

---

## 4️⃣ Configuración de Aiven

1. **Crear servicio**
   - Ir a https://console.aiven.io → Create Service
   - Seleccionar `PostgreSQL` o `MySQL`
   - Configurar plan, usuario y región
   - Esperar a que el servicio esté activo

2. **Obtener credenciales de conexión**
   - Copiar la URI de conexión completa
   - Si usas MySQL, incluye `ssl-mode=REQUIRED`

3. **Crear .env en backend:**
   ```bash
   cd backend
   echo "DATABASE_URL=postgresql://user:password@host:port/dbname" > .env
   echo "SECRET_KEY=tu-clave-secreta" >> .env
   echo "FLASK_ENV=production" >> .env
   ```

---

## 5️⃣ Despliegue en Producción

### Backend - Render

```bash
# En Render, crea un nuevo Web Service y selecciona Python.
# Configura los comandos:
# Build: pip install -r backend/requirements.txt
# Start: python backend/app.py
```

Configura variables de entorno en Render:
- `DATABASE_URL` = URI de Aiven
- `SECRET_KEY` = clave segura
- `FLASK_ENV` = production
- `CORS_ORIGINS` = https://<tu-sitio-vercel>.vercel.app

### Frontend - Vercel

```bash
# Importa el repositorio en Vercel
# Selecciona `frontend` como directorio de despliegue
# Output Directory: public
# Build Command: echo "Static site"
```

Configura la URL del backend editando `frontend/public/app.js`:
```javascript
const API_URL = 'https://tu-backend.onrender.com';
```

---

## 6️⃣ Variables de Entorno en Producción

### Backend (Render)

Configura estas variables desde el panel de Render:
```
DATABASE_URL=postgresql://user:password@host:port/dbname
SECRET_KEY=tu-clave-super-segura
FLASK_ENV=production
CORS_ORIGINS=https://<tu-sitio-vercel>.vercel.app
```

### Frontend (Vercel)

Actualiza la URL del backend en `frontend/public/app.js`:
```javascript
const API_URL = 'https://tu-backend.onrender.com';
```

---

## 7️⃣ Estructura Final

```
proyecto/
├── backend/
│   ├── app.py               ✓
│   ├── requirements.txt     ✓
│   ├── .env.example         ✓
│   └── .env                 (no commitar)
│
├── frontend/
│   ├── public/
│   │   ├── index.html       ✓
│   │   ├── app.js           ✓
│   │   └── styles.css       ✓
│   ├── package.json         ✓
│   └── .env.example         ✓
│
├── ARQUITECTURA_FRONTEND.md ✓
├── README.md                ✓
├── .gitignore              ✓
```
---

## 🔗 URLs de Referencia

- **Aiven:** https://aiven.io/
- **Render:** https://render.com/
- **Vercel:** https://vercel.com/
- **Flask:** https://flask.palletsprojects.com/

---

## ✅ Checklist de Despliegue

- [ ] Servicio Aiven creado y credenciales copiadas
- [ ] Variables de entorno configuradas en Render
- [ ] Backend probado localmente
- [ ] Frontend probado localmente
- [ ] Repo Git configurado
- [ ] Proyecto de Render desplegado
- [ ] Sitio en Vercel desplegado
- [ ] CORS configurado correctamente
- [ ] API URL actualizada en frontend
- [ ] Dominio personalizado configurado (opcional)

---

## 🆘 Troubleshooting

### Error: "psycopg2-binary is required"
```bash
.venv\Scripts\python.exe -m pip install psycopg2-binary
```

### Error: "CORS error"
- Verificar que `CORS_ORIGINS` incluya el dominio de Vercel
- En desarrollo: `http://localhost:3000`

### Error: "Database connection failed"
- Verificar que `DATABASE_URL` sea válida
- Probar conexión: `psql "$DATABASE_URL" -c "SELECT 1"`

### Frontend no ve cambios
- Revisar Deployments en Vercel
- Forzar redeploy desde Vercel si es necesario

---

## 📞 Soporte

Documentación completa en [ARQUITECTURA_FRONTEND.md](./ARQUITECTURA_FRONTEND.md)
