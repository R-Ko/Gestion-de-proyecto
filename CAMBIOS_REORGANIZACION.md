# ⚠️ REORGANIZACIÓN DEL PROYECTO - 18/05/2026

## Cambios Realizados

### 1. Carpeta `templates/` Movida
- **Antes**: `templates/` (raíz del proyecto)
- **Ahora**: `backend/legacy_templates/` (backup histórico)
- **Razón**: Nueva arquitectura usa SPA estático, no templating en servidor

### 2. Nueva Estructura Implementada

```
proyecto/
├── backend/
│   ├── app.py                    # API REST (Cloudflare Workers)
│   ├── requirements.txt
│   ├── wrangler.toml
│   ├── legacy_templates/         # ← Archivos antiguos (NO se usan)
│   └── ...
│
├── frontend/
│   ├── public/
│   │   ├── index.html            # ← Nuevo SPA único
│   │   ├── app.js
│   │   └── styles.css
│   └── ...
│
└── (otros archivos de configuración)
```

### 3. Stack Actualizado

| Aspecto | Antes | Ahora |
|--------|-------|-------|
| Frontend | Renderizado en servidor (templates Jinja2) | SPA estático (vanilla JS) |
| Backend | Flask + templates | API REST pura |
| Host Frontend | Servidor mismo | GitHub Pages |
| Host Backend | Mismo servidor | Cloudflare Workers |
| Base Datos | SQLite local | Supabase PostgreSQL |
| CORS | N/A | Habilitado para GitHub Pages |

### 4. Ventajas de la Nueva Arquitectura

✅ **Escalable**: Servicios independientes  
✅ **Moderno**: SPA en JavaScript puro  
✅ **Gratis**: GitHub Pages + Cloudflare gratis  
✅ **Rápido**: CDN global + base de datos administrada  
✅ **Seguro**: API separada, mejor control de acceso  

### 5. Archivos Nuevos/Modificados

#### Nuevos:
- ✅ `backend/app.py` (actualizado para API pura)
- ✅ `backend/wrangler.toml`
- ✅ `backend/package.json`
- ✅ `frontend/public/index.html`
- ✅ `frontend/public/app.js`
- ✅ `frontend/public/styles.css`
- ✅ `ARQUITECTURA_FRONTEND.md`
- ✅ `INSTALACION.md`
- ✅ `GITHUB_SECRETS.md`
- ✅ `.github/workflows/deploy-*.yml`

#### Reorganizados:
- 📦 `templates/` → `backend/legacy_templates/`
- 📦 `static/` → (opcional mover a `frontend/public/`)

### 6. Qué Pasó con los Templates

Los archivos de templates antiguos se preservaron en `backend/legacy_templates/`:
- `apps.html`
- `app_page.html`
- `login.html`
- `project_*.html`
- `task_*.html`
- `user*.html`

**Para recuperarlos**: Si necesitas volver a renderización en servidor, están disponibles como referencia.

### 7. Próximos Pasos

1. ✅ Hacer commit de todos los cambios
2. ⏳ Actualizar `.env` con credenciales de Supabase
3. ⏳ Configurar secrets en GitHub
4. ⏳ Desplegar en Cloudflare Workers
5. ⏳ Desplegar en GitHub Pages

---

## 📝 Notas

- Los templates antiguos NO se borran, solo se organizan
- La carpeta raíz `templates/` puedes eliminarla después del commit
- El frontend nuevo es más moderno y mantenible
- No hay dependencia de templating engine (Jinja2) en servidor

---

## 🔄 Rollback (si es necesario)

Si quieres volver a la arquitectura anterior:

```bash
# Copiar templates de vuelta
cp backend/legacy_templates/* templates/

# Cambiar backend/app.py para servir templates
# (está documentado en legacy_templates/README.md)
```

---

**Commit**: "feat: Reorganizar estructura - SPA frontend + API backend"
