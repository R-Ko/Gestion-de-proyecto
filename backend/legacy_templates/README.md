# Legacy Templates - Archivos Antiguos (No se usan)

Esta carpeta contiene los templates HTML del desarrollo inicial cuando la aplicación usaba Flask para renderizar HTML en el servidor.

**Estado Actual:**
- ❌ **NO se usan** en la nueva arquitectura
- ✅ Los reemplazó el frontend estático en `frontend/public/`

**Por qué están aquí:**
- Se guardan como referencia histórica
- Podrían servir si se vuelve a un modelo de renderización en servidor
- Documentan la evolución del proyecto

**Nueva Arquitectura:**
- Frontend: `frontend/public/index.html` (SPA estático)
- Backend: API REST pura (sin templates)
- Base de datos: Supabase PostgreSQL

**Para recuperar la vieja arquitectura:**
Si alguna vez necesitas volver a renderizar templates en Flask:

```python
from flask import render_template

@app.route('/login')
def login():
    return render_template('login.html')
```

Pero **NO ES RECOMENDADO** para la arquitectura actual.
