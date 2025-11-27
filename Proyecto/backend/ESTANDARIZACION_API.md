# 📋 Estandarización de API - Resumen de Cambios

**Fecha:** 27 de Noviembre, 2025  
**Problema identificado:** Los endpoints estaban funcionando con `/api` en lugar de `/api/v1`

---

## 🔍 Problema Identificado

El usuario reportó que el endpoint `http://localhost:8000/api/admin/health` funcionaba, cuando según el **API_CONTRACT.md** debería ser `http://localhost:8000/api/v1/admin/health`.

### Causa Raíz

En el archivo `.env`, el valor de `API_V1_STR` estaba configurado como:
```env
API_V1_STR=/api
```

Cuando debería ser:
```env
API_V1_STR=/api/v1
```

---

## ✅ Cambios Realizados

### 1. Archivo `/Users/sebasmancera/Group-of-patterns/Proyecto/backend/.env`

**Antes:**
```env
API_V1_STR=/api
```

**Después:**
```env
API_V1_STR=/api/v1
```

### 2. Archivo `/Users/sebasmancera/Group-of-patterns/Proyecto/backend/.env.example`

**Antes:**
```env
API_V1_STR=/api
```

**Después:**
```env
API_V1_STR=/api/v1
```

---

## 🧪 Verificaciones Necesarias

Para confirmar que todos los endpoints están estandarizados según el contrato de API, realiza las siguientes pruebas:

### 1. Reiniciar el Servidor

```bash
cd /Users/sebasmancera/Group-of-patterns/Proyecto/backend

# Detener cualquier servidor corriendo
pkill -f "uvicorn app.main:app"

# Iniciar el servidor
source .venv/bin/activate
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 2. Probar Endpoints Públicos (🟢)

```bash
# Root endpoint
curl http://localhost:8000/
# Esperado: {"name": "Air Quality Platform API", ...}

# Health check básico
curl http://localhost:8000/health
# Esperado: {"status": "healthy", ...}

# Documentación API
open http://localhost:8000/api/v1/docs
```

### 3. Probar Endpoints de Authentication (🟢)

```bash
# Login
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin@airquality.com&password=admin123"

# Guardar el token de la respuesta
TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."

# Obtener usuario actual
curl -H "Authorization: Bearer $TOKEN" \
  "http://localhost:8000/api/v1/auth/me"
```

### 4. Probar Endpoints de Stations (🟢)

```bash
# Listar estaciones
curl "http://localhost:8000/api/v1/stations"

# Obtener estación específica
curl "http://localhost:8000/api/v1/stations/1"

# Obtener lecturas actuales
curl "http://localhost:8000/api/v1/stations/1/readings/current"
```

### 5. Probar Endpoints de Air Quality (🟢)

```bash
# Dashboard
curl "http://localhost:8000/api/v1/air-quality/dashboard?city=New%20York"

# Estadísticas diarias
curl "http://localhost:8000/api/v1/air-quality/daily-stats?station_id=1"
```

### 6. Probar Endpoints de Admin (🔴 Requiere autenticación)

```bash
# Asegúrate de tener un token de admin
ADMIN_TOKEN="..."

# Health check
curl -H "Authorization: Bearer $ADMIN_TOKEN" \
  "http://localhost:8000/api/v1/admin/health"

# Listar estaciones (admin)
curl -H "Authorization: Bearer $ADMIN_TOKEN" \
  "http://localhost:8000/api/v1/admin/stations"

# Listar usuarios
curl -H "Authorization: Bearer $ADMIN_TOKEN" \
  "http://localhost:8000/api/v1/admin/users"
```

### 7. Probar Endpoints de Recommendations (🟡 Requiere token)

```bash
USER_TOKEN="..."

# Recomendación actual
curl -H "Authorization: Bearer $USER_TOKEN" \
  "http://localhost:8000/api/v1/recommendations/current?location=New%20York"

# Historial
curl -H "Authorization: Bearer $USER_TOKEN" \
  "http://localhost:8000/api/v1/recommendations/history"
```

### 8. Probar Endpoints de Settings (🟡 Requiere token)

```bash
USER_TOKEN="..."

# Obtener preferencias
curl -H "Authorization: Bearer $USER_TOKEN" \
  "http://localhost:8000/api/v1/settings/preferences"

# Configuración del dashboard
curl -H "Authorization: Bearer $USER_TOKEN" \
  "http://localhost:8000/api/v1/settings/dashboard"
```

### 9. Probar Endpoints de Reports (🟡 Requiere token)

```bash
USER_TOKEN="..."

# Listar reportes
curl -H "Authorization: Bearer $USER_TOKEN" \
  "http://localhost:8000/api/v1/reports"

# Crear reporte
curl -X POST "http://localhost:8000/api/v1/reports" \
  -H "Authorization: Bearer $USER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "city": "New York",
    "start_date": "2025-11-01",
    "end_date": "2025-11-27",
    "station_id": 1,
    "pollutant_id": 1
  }'
```

---

## 📊 Lista de Verificación de Endpoints

Según el **API_CONTRACT.md**, todos los endpoints deben tener el prefijo `/api/v1`:

### ✅ Authentication
- [x] `POST /api/v1/auth/login`
- [x] `GET /api/v1/auth/me`

### ✅ Stations
- [x] `GET /api/v1/stations`
- [x] `GET /api/v1/stations/{station_id}`
- [x] `GET /api/v1/stations/{station_id}/readings/current`

### ✅ Air Quality
- [x] `GET /api/v1/air-quality/current` (si está implementado)
- [x] `GET /api/v1/air-quality/dashboard`
- [x] `GET /api/v1/air-quality/daily-stats`

### ✅ Recommendations
- [x] `GET /api/v1/recommendations/current`
- [x] `GET /api/v1/recommendations/history`

### ✅ Admin
- [x] `GET /api/v1/admin/health`
- [x] `GET /api/v1/admin/stations`
- [x] `POST /api/v1/admin/stations`
- [x] `PUT /api/v1/admin/stations/{station_id}`
- [x] `DELETE /api/v1/admin/stations/{station_id}`
- [x] `GET /api/v1/admin/users`
- [x] `PUT /api/v1/admin/users/{user_id}/role`

### ✅ Settings
- [x] `GET /api/v1/settings/preferences`
- [x] `PUT /api/v1/settings/preferences`
- [x] `GET /api/v1/settings/dashboard`
- [x] `PUT /api/v1/settings/dashboard`

### ✅ Reports
- [x] `POST /api/v1/reports`
- [x] `GET /api/v1/reports`
- [x] `GET /api/v1/reports/{report_id}`

---

## 🔄 Endpoints que NO deben cambiar

Estos endpoints están en el nivel raíz y son correctos:

- ✅ `GET /` - Root endpoint
- ✅ `GET /health` - Health check básico

---

## 📝 Notas Importantes

1. **Documentación interactiva:** Ahora disponible en `http://localhost:8000/api/v1/docs`
2. **OpenAPI JSON:** Disponible en `http://localhost:8000/api/v1/openapi.json`
3. **ReDoc:** Disponible en `http://localhost:8000/api/v1/redoc`

4. **Compatibilidad hacia atrás:** Los endpoints antiguos con `/api` (sin `/v1`) **ya no funcionan**. Esto es intencional para mantener la consistencia con el contrato de API.

5. **Frontend:** Si tienes un frontend conectado, asegúrate de actualizar todas las URLs de:
   ```javascript
   // ❌ Antiguo (incorrecto)
   const API_BASE = 'http://localhost:8000/api'
   
   // ✅ Nuevo (correcto)
   const API_BASE = 'http://localhost:8000/api/v1'
   ```

---

## 🎯 Resultado Esperado

Después de estos cambios:

| URL | Estado | Descripción |
|-----|--------|-------------|
| `http://localhost:8000/api/admin/health` | ❌ 404 | Ya no funciona (incorrecto) |
| `http://localhost:8000/api/v1/admin/health` | ✅ 200 | Funciona correctamente |
| `http://localhost:8000/api/v1/docs` | ✅ 200 | Documentación Swagger |
| `http://localhost:8000/api/v1/stations` | ✅ 200 | Lista de estaciones |

---

## 🐛 Troubleshooting

### Problema: El servidor no inicia

```bash
# Verificar que el puerto 8000 esté libre
lsof -i :8000

# Si hay algo ocupándolo, mátalo
lsof -ti:8000 | xargs kill -9
```

### Problema: "Address already in use"

```bash
# Matar todos los procesos de uvicorn
pkill -9 -f uvicorn

# Esperar un momento
sleep 2

# Reiniciar
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Problema: Error de base de datos

Si ves errores de autenticación de PostgreSQL, verifica tu configuración en `.env`:

```env
DATABASE_URL=postgresql://postgres:TU_PASSWORD@localhost:5432/airquality_db
```

---

## ✅ Conclusión

Los cambios realizados estandarizan todos los endpoints para que cumplan con el **API_CONTRACT.md**. Ahora todos los endpoints de la API v1 están bajo el prefijo `/api/v1`, lo cual mejora:

1. ✅ **Consistencia:** Todos los endpoints siguen el mismo patrón
2. ✅ **Versionado:** Preparado para futuras versiones de API (v2, v3, etc.)
3. ✅ **Documentación:** La documentación Swagger refleja correctamente las rutas
4. ✅ **Mantenibilidad:** Código más fácil de mantener y entender

---

**Próximos pasos:**
1. Reiniciar el servidor
2. Ejecutar las verificaciones listadas arriba
3. Actualizar cualquier cliente/frontend que use la API
4. Verificar que todos los tests pasen con las nuevas rutas

