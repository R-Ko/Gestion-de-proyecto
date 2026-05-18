# Gestión de Proyectos - Arquitectura Modular

## 📋 Descripción

Sistema de gestión de proyectos y tareas estilo **Odoo** con arquitectura moderna y escalable:

- **Frontend**: SPA estático en Vercel  
- **Backend**: API en Render (Python/Flask)  
- **Base de Datos**: PostgreSQL/MySQL en Aiven  

---

## 🏗️ Estructura del Proyecto

```
proyecto/
│
├── backend/                    # API Backend en Render / Flask
│   ├── app.py                 # API Flask compatible con Render
│   ├── requirements.txt       # Dependencias Python
│   ├── Procfile               # Para despliegue alternativo
│   └── .env.example           # Ejemplo de variables de entorno
│
├── frontend/                   # SPA estático en Vercel
│   ├── public/
│   │   ├── index.html         # HTML principal
│   │   ├── app.js             # Lógica JavaScript
│   │   └── styles.css         # Estilos (tema oscuro Odoo)
│   └── package.json
│
├── ARQUITECTURA_FRONTEND.md   # Documentación técnica completa
└── README.md                  # Este archivo
```

---

## 🚀 Despliegue

### 1️⃣ Base de Datos - Aiven

#### Requisitos:
- Cuenta en [Aiven](https://console.aiven.io)
- Servicio PostgreSQL o MySQL creado

#### Pasos:

1. **Crear un servicio en Aiven:**
   - Ir a https://console.aiven.io → Create Service
   - Elegir `PostgreSQL` o `MySQL`
   - Definir plan y región
   - Esperar a que el servicio esté activo

2. **Obtener credenciales de conexión:**
   - Ir a la página del servicio
   - Copiar la `Connection string` o `URI` completo
   - Si usas MySQL, asegúrate de incluir `ssl-mode=REQUIRED`

3. **Configurar variables de entorno en backend:**
   ```bash
   cd backend
   echo "DATABASE_URL=postgresql://user:password@host:port/dbname" > .env
   echo "SECRET_KEY=tu-clave-secreta-super-segura" >> .env
   echo "FLASK_ENV=production" >> .env
   ```

4. **Inicializar la base de datos:**
   ```bash
   cd backend
   .venv\Scripts\python.exe app.py
   ```
   El primer arranque creará las tablas necesarias.

---

### 2️⃣ Backend - Render

#### Requisitos:
- Cuenta en [Render](https://render.com)
- Repositorio Git con la rama `main`

#### Pasos:

1. **Crear un nuevo Web Service en Render:**
   - Importar el repositorio desde GitHub
   - Seleccionar `Python` como Runtime
   - Usar el comando de Build: `pip install -r backend/requirements.txt`
   - Usar el comando de Start: `python backend/app.py`
   - Definir `Root Directory` o `Start Directory` según el proyecto

2. **Configurar variables de entorno en Render:**
   - `DATABASE_URL` = URI de Aiven
   - `SECRET_KEY` = clave segura
   - `FLASK_ENV` = `production`
   - `CORS_ORIGINS` = `https://<tu-sitio-vercel>.vercel.app`

3. **Desplegar:**
   - Guardar y desplegar el servicio
   - Render construirá y publicará la API

---

### 3️⃣ Frontend - Vercel

#### Requisitos:
- Cuenta en [Vercel](https://vercel.com)
- Repo Git con la carpeta `frontend`

#### Pasos:

1. **Crear un nuevo proyecto en Vercel:**
   - Importar el repositorio desde GitHub
   - Seleccionar `frontend` como directorio de despliegue
   - Configurar `Build Command` como `echo "Static site"`
   - Configurar `Output Directory` como `public`

2. **Configurar la URL del backend:**
   - Editar `frontend/public/app.js`
   - Ajustar `window.API_URL` en el HTML o usar una constante directa:
     ```javascript
     const API_URL = 'https://tu-backend.onrender.com';
     ```

3. **Desplegar:**
   - Guardar la configuración
   - Desplegar el sitio en Vercel
   - El dominio de Vercel quedará activo automáticamente

---

### 4️⃣ Flujo de despliegue completo

1. El frontend se despliega en Vercel como sitio estático.
2. El backend se despliega en Render como servicio Python/Flask.
3. Aiven provee la base de datos PostgreSQL/MySQL y ofrece SSL en producción.
4. El frontend consume la API de Render mediante `API_URL`.

---

## 🔐 Variables de Entorno

### Backend (`backend/.env`)
```
DATABASE_URL=postgresql://user:pass@host/db
SECRET_KEY=tu-clave-super-secura
FLASK_ENV=production
CORS_ORIGINS=https://<tu-proyecto>.vercel.app
```

### Frontend (`frontend/public/app.js`)
```javascript
const API_URL = 'https://tu-backend.onrender.com';
```

---

##  Credenciales de Prueba

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

### Render + Dominio personalizado

1. En Render, ve al servicio del backend.
2. Agrega un dominio personalizado.
3. Sigue las instrucciones de DNS para CNAME o A records.

### Vercel + Dominio personalizado

1. En Vercel, ve al proyecto del frontend.
2. Agrega el dominio personalizado.
3. Configura el DNS según las instrucciones de Vercel.

---

## 📊 Monitoreo y Logs

### Render
- Dashboard → Service → Logs
- Health checks y despliegues

### Vercel
- Dashboard → Deployments
- Logs de ejecución y errores

### Aiven
- Console → Service → Logs
- Metrics → Database

---

## 🔧 Troubleshooting

### CORS errores en el frontend
```python
# En backend/app.py
CORS(app, resources={
    r"/api/*": {
        "origins": ["https://<tu-sitio-vercel>.vercel.app"],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})
```

### Base de datos no conecta
```bash
# Verificar conexión con Aiven
psql "$DATABASE_URL" -c "SELECT 1"
```

### Despliegue en Vercel no actualiza
```bash
# Revisar Deployment en Vercel y redeploy
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
