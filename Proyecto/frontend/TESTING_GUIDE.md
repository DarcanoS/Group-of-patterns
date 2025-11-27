# 🧪 Guía Paso a Paso - Pruebas de Integración Frontend

**Fecha:** 27 de Noviembre, 2025  
**Objetivo:** Probar sistemáticamente cada vista del frontend y verificar qué servicios del backend se consumen

---

## 📋 Requisitos Previos

### ✅ Antes de Empezar

1. **Backend corriendo:**
   ```bash
   # Verificar que el backend responda
   curl http://localhost:8000/api/v1/admin/health
   ```
   ✅ Debe responder: `{"status":"healthy","database":"connected",...}`

2. **Frontend corriendo:**
   ```bash
   cd /Users/sebasmancera/Group-of-patterns/Proyecto/frontend
   npm run dev
   ```
   ✅ Debe estar en: `http://localhost:5173`

3. **Base de datos con datos de prueba:**
   - Usuarios creados (citizen, researcher, admin)
   - Estaciones con datos
   - Lecturas de calidad del aire

4. **Herramientas de debugging:**
   - Navegador con DevTools abierto (F12)
   - Pestaña **Network** para ver peticiones HTTP
   - Pestaña **Console** para ver logs

---

## 🎯 Flujo de Pruebas Completo

```
1. Landing Page (Pública)
   ↓
2. Login (Autenticación)
   ↓
3. Citizen Dashboard (Usuario autenticado)
   ↓
4. Researcher Dashboard (Investigador)
   ↓
5. Admin Dashboard (Administrador)
```

---

## 📍 PRUEBA 1: Landing Page

### 🌐 URL
```
http://localhost:5173/
```

### 🎯 Objetivo
Verificar que la página de inicio carga correctamente (NO requiere backend)

### 🔍 Qué Servicios se Consumen
**NINGUNO** - La landing page es completamente estática

### ✅ Pasos de Prueba

1. **Abrir la URL en el navegador**
   ```
   http://localhost:5173/
   ```

2. **Verificar que se muestre:**
   - ✅ Hero section con título y descripción
   - ✅ Sección de roles (Citizen, Researcher, Admin)
   - ✅ Sección "How it Works"
   - ✅ Sección de insights/estadísticas

3. **Verificar en DevTools (F12):**
   - Pestaña **Network**: No debe haber llamadas al backend
   - Pestaña **Console**: No debe haber errores en rojo

### ❌ Errores Comunes
- Si no carga: Verificar que `npm run dev` esté corriendo
- Si hay errores CSS: Los archivos de estilos deben estar en `/src/styles/`

### 📸 Resultado Esperado
```
✅ Página carga sin errores
✅ Sin llamadas HTTP al backend
✅ Navegación funcional a /login
```

---

## 📍 PRUEBA 2: Login

### 🌐 URL
```
http://localhost:5173/login
```

### 🎯 Objetivo
Autenticar al usuario y obtener el token JWT

### 🔍 Qué Servicios se Consumen

#### **Servicio:** `authService.login()`
#### **Endpoint Backend:** `POST /api/v1/auth/login`

**Petición que se envía:**
```http
POST http://localhost:8000/api/v1/auth/login
Content-Type: application/x-www-form-urlencoded

username=citizen@example.com
password=citizen123
```

**Respuesta esperada:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "email": "citizen@example.com",
    "full_name": "John Citizen",
    "role": {
      "id": 1,
      "name": "Citizen",
      "description": "Regular citizen user"
    },
    "is_active": true
  }
}
```

### ✅ Pasos de Prueba

1. **Abrir DevTools (F12)** antes de hacer login
   - Ir a pestaña **Network**
   - Marcar "Preserve log" para no perder las peticiones

2. **Ingresar credenciales:**
   ```
   Email: citizen@example.com
   Password: citizen123
   ```

3. **Click en botón "Login"**

4. **Verificar en Network:**
   - ✅ Debe aparecer una petición `POST` a `/api/v1/auth/login`
   - ✅ Status Code: `200 OK`
   - ✅ Response contiene `access_token`

5. **Verificar en Application/Storage:**
   - Ir a pestaña **Application** → **Local Storage** → `http://localhost:5173`
   - ✅ Debe existir: `access_token` con valor del JWT
   - ✅ Debe existir: `user` con JSON del usuario

6. **Verificar redirección:**
   - Actualmente redirige a `/dashboard` (simulado)
   - Debe cambiar a `/dashboard/citizen` para ciudadanos

### 📊 Monitoreo en DevTools

**Network Tab:**
```
Request URL: http://localhost:8000/api/v1/auth/login
Request Method: POST
Status Code: 200 OK

Request Headers:
  Content-Type: application/x-www-form-urlencoded

Form Data:
  username: citizen@example.com
  password: citizen123

Response:
  {
    "access_token": "...",
    "user": {...}
  }
```

**Console Tab:**
```javascript
// Debería aparecer:
Login: citizen@example.com citizen123
```

### 🧪 Pruebas con Diferentes Roles

Repite el login con estos usuarios:

| Rol | Email | Password | Dashboard esperado |
|-----|-------|----------|-------------------|
| **Citizen** | citizen@example.com | citizen123 | /dashboard/citizen |
| **Researcher** | researcher@example.com | researcher123 | /dashboard/researcher |
| **Admin** | admin@example.com | admin123 | /dashboard/admin |

### ❌ Errores Comunes

**Error 401 Unauthorized:**
```json
{"detail": "Incorrect email or password"}
```
→ Las credenciales son incorrectas o el usuario no existe en la BD

**Error 500 Internal Server Error:**
```json
{"detail": "Database connection error"}
```
→ El backend no puede conectarse a PostgreSQL

**Error CORS:**
```
Access to fetch at 'http://localhost:8000/...' from origin 'http://localhost:5173' 
has been blocked by CORS policy
```
→ El backend necesita configurar CORS para permitir localhost:5173

### 📸 Resultado Esperado
```
✅ Login exitoso
✅ Token guardado en localStorage
✅ Usuario redirigido al dashboard
✅ Petición POST visible en Network tab
```

---

## 📍 PRUEBA 3: Citizen Dashboard

### 🌐 URL
```
http://localhost:5173/dashboard/citizen
```

### 🎯 Objetivo
Mostrar la calidad del aire actual y recomendaciones para el ciudadano

### 🔍 Qué Servicios se Consumen

#### **Servicio 1:** `getAirQuality(city)`
#### **Endpoint:** `GET /api/v1/air-quality/current?city={city}`

**Petición que se envía:**
```http
GET http://localhost:8000/api/v1/air-quality/current?city=Bogotá
```

**Respuesta esperada:**
```json
{
  "city": "Bogotá",
  "aqi": 102,
  "primary_pollutant": "PM2.5",
  "risk_category": {
    "level": "Unhealthy for Sensitive Groups",
    "color": "#FF9800",
    "health_implications": "Members of sensitive groups may experience health effects",
    "cautionary_statement": "Active children and adults should limit prolonged outdoor exertion"
  },
  "timestamp": "2025-11-27T14:30:00",
  "station": {
    "id": 1,
    "name": "Downtown Station"
  }
}
```

#### **Servicio 2:** `getStations(city)`
#### **Endpoint:** `GET /api/v1/stations?city={city}&limit=10`

**Petición que se envía:**
```http
GET http://localhost:8000/api/v1/stations?city=Bogotá&limit=10
```

**Respuesta esperada:**
```json
[
  {
    "id": 1,
    "name": "Estación Centro",
    "latitude": 4.6097,
    "longitude": -74.0817,
    "city": "Bogotá",
    "country": "Colombia",
    "is_active": true
  },
  {
    "id": 2,
    "name": "Estación Norte",
    "latitude": 4.6097,
    "longitude": -74.0817,
    "city": "Bogotá",
    "country": "Colombia",
    "is_active": true
  }
]
```

#### **Servicio 3:** `getStationCurrentReadings(stationId)`
#### **Endpoint:** `GET /api/v1/stations/{id}/readings/current`

**Petición que se envía (para cada estación):**
```http
GET http://localhost:8000/api/v1/stations/1/readings/current
GET http://localhost:8000/api/v1/stations/2/readings/current
GET http://localhost:8000/api/v1/stations/3/readings/current
```

**Respuesta esperada:**
```json
{
  "station": {
    "id": 1,
    "name": "Estación Centro",
    "city": "Bogotá"
  },
  "readings": [
    {
      "pollutant": {
        "id": 1,
        "name": "PM2.5",
        "unit": "µg/m³"
      },
      "value": 35.5,
      "aqi": 102,
      "timestamp": "2025-11-27T14:30:00"
    }
  ],
  "last_updated": "2025-11-27T14:30:00"
}
```

### ✅ Pasos de Prueba

1. **Asegurarse de estar autenticado:**
   - Debe haber hecho login primero
   - Verificar en Application → Local Storage que existe `access_token`

2. **Navegar a:**
   ```
   http://localhost:5173/dashboard/citizen
   ```

3. **Verificar que aparece "cargando datos..."**
   - Esto indica que está haciendo las peticiones

4. **Verificar en Network Tab:**
   - ✅ Petición 1: `GET /api/v1/air-quality/current?city=Bogotá`
   - ✅ Petición 2: `GET /api/v1/stations?city=Bogotá&limit=10`
   - ✅ Peticiones 3-5: `GET /api/v1/stations/{id}/readings/current` (para las primeras 3 estaciones)

5. **Verificar que se muestra:**
   - ✅ **Card AQI** con el valor numérico (ej: 102)
   - ✅ **Card Status** con nivel de riesgo
   - ✅ **Card Estaciones Cercanas** con lista de estaciones y sus AQI
   - ✅ **Card Sugerencias** (puede estar vacío por ahora)
   - ✅ **Gráfico histórico** con Chart.js

6. **Verificar colores del AQI:**
   - AQI 0-50: Verde (Good)
   - AQI 51-100: Amarillo (Moderate)
   - AQI 101-150: Naranja (Unhealthy for Sensitive Groups)
   - AQI 151-200: Rojo (Unhealthy)
   - AQI 201+: Morado (Very Unhealthy)

### 📊 Monitoreo en DevTools

**Network Tab - Secuencia de peticiones:**
```
1. GET /air-quality/current?city=Bogotá
   Status: 200 OK
   Response: { "city": "Bogotá", "aqi": 102, ... }

2. GET /stations?city=Bogotá&limit=10
   Status: 200 OK
   Response: [ { "id": 1, "name": "Estación Centro", ... }, ... ]

3. GET /stations/1/readings/current
   Status: 200 OK
   Response: { "station": {...}, "readings": [...], ... }

4. GET /stations/2/readings/current
   Status: 200 OK
   ...

5. GET /stations/3/readings/current
   Status: 200 OK
   ...
```

**Console Tab:**
```javascript
// No debe haber errores rojos
// Puede haber logs informativos como:
"Air quality data loaded for Bogotá"
```

### 🎨 Elementos Visuales a Verificar

1. **Card AQI (grande, centrado):**
   ```
   Air Quality
   102          ← Número grande con color según nivel
   Unhealthy for Sensitive Groups  ← Descripción del nivel
   ultima actualizacion: 27/11/2025 14:30  ← Timestamp
   ```

2. **Card Status:**
   ```
   Status
   Unhealthy for Sensitive Groups
   Limit prolonged outdoor exertion  ← Recomendación
   ```

3. **Card Estaciones Cercanas:**
   ```
   Estaciones cercanas
   • Estación Centro — AQI 102
   • Estación Norte — AQI 95
   • Estación Sur — AQI 88
   ```

4. **Gráfico Chart.js:**
   - Línea con los últimos 7 días de AQI
   - Eje X: Días de la semana
   - Eje Y: Valores de AQI

### ❌ Errores Comunes

**Error: "Unable to connect to air quality service"**
→ El backend no responde o la ciudad no tiene datos

**Error 401 en las peticiones:**
→ El token expiró o no existe. Hacer login nuevamente.

**Error: "Cannot read property 'history' of null"**
→ La petición falló y `data.value` es null. Revisar respuesta del backend.

**Gráfico no aparece:**
→ Chart.js no está inicializado o el canvas no se encuentra

### 📸 Resultado Esperado
```
✅ Dashboard carga sin "cargando datos..."
✅ AQI visible con color correcto
✅ 3-4 peticiones HTTP exitosas (200 OK)
✅ Estaciones listadas con sus AQI
✅ Gráfico renderizado
✅ Sin errores en Console
```

---

## 📍 PRUEBA 4: Researcher Dashboard

### 🌐 URL
```
http://localhost:5173/dashboard/researcher
```

### 🎯 Objetivo
Mostrar estadísticas históricas y permitir filtros avanzados para análisis

### 🔍 Qué Servicios se Consumen

#### **Servicio:** `fetchDailyStats({ city, station, pollutant, startDate, endDate })`
#### **Endpoint:** `GET /api/v1/air-quality/daily-stats`

**Petición inicial (sin filtros):**
```http
GET http://localhost:8000/api/v1/air-quality/daily-stats?limit=365
```

**Petición con filtros aplicados:**
```http
GET http://localhost:8000/api/v1/air-quality/daily-stats?limit=365&station_id=1&pollutant_id=1&start_date=2025-11-13&end_date=2025-11-27
```

**Respuesta esperada:**
```json
[
  {
    "id": 1,
    "date": "2025-11-27",
    "station_id": 1,
    "pollutant_id": 1,
    "avg_value": 35.5,
    "max_value": 45.2,
    "min_value": 28.1,
    "avg_aqi": 102,
    "readings_count": 24
  },
  {
    "id": 2,
    "date": "2025-11-26",
    "station_id": 1,
    "pollutant_id": 1,
    "avg_value": 32.1,
    "max_value": 41.5,
    "min_value": 25.8,
    "avg_aqi": 95,
    "readings_count": 24
  }
  // ... más registros
]
```

#### **Servicio auxiliar:** `getStations(city)` si se filtra por ciudad
#### **Endpoint:** `GET /api/v1/stations?city={city}&limit=1`

### ✅ Pasos de Prueba

#### PASO 1: Carga Inicial

1. **Login como researcher:**
   ```
   Email: researcher@example.com
   Password: researcher123
   ```

2. **Navegar a:**
   ```
   http://localhost:5173/dashboard/researcher
   ```

3. **Verificar en Network Tab:**
   - ✅ Petición: `GET /api/v1/air-quality/daily-stats?limit=365`
   - ✅ Status: 200 OK
   - ✅ Response: Array de objetos con estadísticas diarias

4. **Verificar que se muestra:**
   - ✅ Card de filtros en la parte superior
   - ✅ "Loading data..." brevemente
   - ✅ Gráfico de línea con tendencia de AQI
   - ✅ Tabla con datos día por día

#### PASO 2: Aplicar Filtros

1. **Seleccionar filtros:**
   ```
   City: Bogotá
   Station: Estación Centro
   Pollutant: PM2.5
   Start Date: 2025-11-13
   End Date: 2025-11-27
   ```

2. **Click en "Apply"**

3. **Verificar en Network Tab:**
   - ✅ Nueva petición con parámetros de filtro
   - ✅ URL debe incluir: `station_id=1&pollutant_id=1&start_date=2025-11-13&end_date=2025-11-27`

4. **Verificar que los datos se actualizan:**
   - ✅ El gráfico se redibuja con los nuevos datos
   - ✅ La tabla muestra solo los registros filtrados
   - ✅ Las fechas corresponden al rango seleccionado

#### PASO 3: Resetear Filtros

1. **Click en "Reset"**

2. **Verificar:**
   - ✅ Todos los filtros vuelven a valores por defecto
   - ✅ Nueva petición sin parámetros de filtro
   - ✅ Datos originales restaurados

#### PASO 4: Exportar Datos

1. **Click en "Export CSV"**

2. **Verificar:**
   - ✅ Se descarga un archivo CSV
   - ✅ Contiene las columnas: date, city, station, pollutant, avg_aqi
   - ✅ Datos corresponden a lo mostrado en la tabla

3. **Click en "Download JSON"**

4. **Verificar:**
   - ✅ Se descarga un archivo JSON
   - ✅ Contiene los mismos datos en formato JSON

### 📊 Monitoreo en DevTools

**Network Tab - Carga inicial:**
```
GET /api/v1/air-quality/daily-stats?limit=365
Status: 200 OK
Response: [
  { "date": "2025-11-27", "avg_aqi": 102, ... },
  { "date": "2025-11-26", "avg_aqi": 95, ... },
  ...
]
```

**Network Tab - Con filtros aplicados:**
```
1. GET /api/v1/stations?city=Bogotá&limit=1
   Status: 200 OK
   Response: [ { "id": 1, "name": "Estación Centro", ... } ]

2. GET /api/v1/air-quality/daily-stats?limit=365&station_id=1&pollutant_id=1&start_date=2025-11-13&end_date=2025-11-27
   Status: 200 OK
   Response: [ ... datos filtrados ... ]
```

### 🎨 Elementos Visuales a Verificar

1. **Card de Filtros:**
   ```
   ┌─────────────────────────────────────┐
   │ City: [Bogotá ▼]  Station: [All ▼] │
   │ Pollutant: [PM2.5 ▼]                │
   │ Start: [2025-11-13]  End: [2025-11-27] │
   │ [Apply] [Reset]                     │
   └─────────────────────────────────────┘
   ```

2. **Card de Gráfico:**
   ```
   Daily AQI Trend              [Export CSV] [Download JSON]
   ┌─────────────────────────────────────┐
   │        Chart.js Line Chart          │
   │  150 │              ╱╲              │
   │  100 │         ╱──╲/  ╲   ╱╲        │
   │   50 │    ╱──╲      ╲/  ╲/  ╲       │
   │    0 └────────────────────────────  │
   │      Mon Tue Wed Thu Fri Sat Sun    │
   └─────────────────────────────────────┘
   ```

3. **Tabla de Datos:**
   ```
   ┌──────────────┬─────────┬─────────────┬──────────┬─────────┐
   │ Fecha        │ Ciudad  │ Estación    │ Polutión │ Avg AQI │
   ├──────────────┼─────────┼─────────────┼──────────┼─────────┤
   │ 2025-11-27   │ Bogotá  │ Est. Centro │ PM2.5    │ 102     │
   │ 2025-11-26   │ Bogotá  │ Est. Centro │ PM2.5    │ 95      │
   │ 2025-11-25   │ Bogotá  │ Est. Centro │ PM2.5    │ 88      │
   └──────────────┴─────────┴─────────────┴──────────┴─────────┘
   ```

### ❌ Errores Comunes

**"No records to display":**
→ La combinación de filtros no tiene datos en la BD

**Gráfico no se actualiza:**
→ El componente no está detectando el cambio en los datos. Verificar que Chart.js se reinicializa.

**Error 404 en /stations:**
→ La ciudad no existe o no tiene estaciones registradas

**Fechas no funcionan:**
→ El formato debe ser YYYY-MM-DD (ISO 8601)

### 📸 Resultado Esperado
```
✅ Dashboard carga con datos iniciales
✅ Gráfico muestra tendencia de AQI
✅ Tabla poblada con registros
✅ Filtros actualizan los datos
✅ Exportación funciona (CSV y JSON)
✅ 1-2 peticiones HTTP por acción
```

---

## 📍 PRUEBA 5: Admin Dashboard

### 🌐 URL
```
http://localhost:5173/dashboard/admin
```

### 🎯 Objetivo
Panel de administración (funcionalidad básica por implementar)

### 🔍 Qué Servicios se Consumen
**POR DEFINIR** - El admin dashboard puede requerir endpoints específicos como:
- Gestión de usuarios
- Gestión de estaciones
- Configuración del sistema
- Métricas de uso

### ✅ Pasos de Prueba

1. **Login como admin:**
   ```
   Email: admin@example.com
   Password: admin123
   ```

2. **Navegar a:**
   ```
   http://localhost:5173/dashboard/admin
   ```

3. **Verificar:**
   - ✅ La vista carga sin errores
   - ⏸️ Funcionalidad por implementar según requerimientos

---

## 🛠️ Herramientas de Debugging

### 1. Network Tab (Chrome DevTools)

**Cómo usar:**
1. Presionar F12 → pestaña **Network**
2. Marcar **Preserve log** para no perder peticiones en navegación
3. Filtrar por **XHR** o **Fetch** para ver solo peticiones AJAX
4. Click en cualquier petición para ver:
   - **Headers**: URL, método, headers enviados
   - **Payload**: Datos enviados (POST/PUT)
   - **Response**: Datos recibidos del backend
   - **Timing**: Cuánto tardó la petición

**Verificar en cada petición:**
```
✅ Status Code: 200 OK (verde)
✅ Response Tab: JSON válido
✅ Size: KB transferidos
✅ Time: Milisegundos de respuesta
```

### 2. Console Tab

**Cómo usar:**
1. F12 → pestaña **Console**
2. Buscar errores en rojo
3. Ver logs de información (console.log)

**Comandos útiles:**
```javascript
// Ver token guardado
localStorage.getItem('access_token')

// Ver usuario guardado
JSON.parse(localStorage.getItem('user'))

// Hacer petición manual
fetch('http://localhost:8000/api/v1/air-quality/current?city=Bogotá')
  .then(r => r.json())
  .then(console.log)

// Ver si hay token
console.log('Authenticated:', !!localStorage.getItem('access_token'))
```

### 3. Application Tab

**Cómo usar:**
1. F12 → pestaña **Application**
2. Expandir **Local Storage** → `http://localhost:5173`
3. Ver/editar/borrar keys:
   - `access_token`: JWT token
   - `user`: Datos del usuario en JSON

**Para resetear sesión:**
```javascript
// En Console:
localStorage.clear()
location.reload()
```

### 4. Vue DevTools (Extensión recomendada)

**Instalar:**
- Chrome: https://chrome.google.com/webstore → "Vue.js devtools"
- Firefox: https://addons.mozilla.org → "Vue.js devtools"

**Usar:**
1. F12 → pestaña **Vue**
2. Ver componentes en el árbol
3. Inspeccionar data, props, computed
4. Ver eventos emitidos

---

## 📊 Checklist de Pruebas Completa

### Landing Page
- [ ] Página carga sin errores
- [ ] No hay peticiones HTTP al backend
- [ ] Botones de navegación funcionan
- [ ] Responsive en móvil

### Login
- [ ] Formulario funciona
- [ ] POST a `/auth/login` retorna 200
- [ ] Token se guarda en localStorage
- [ ] Usuario se guarda en localStorage
- [ ] Redirección al dashboard correcto según rol
- [ ] Error mostrado si credenciales incorrectas

### Citizen Dashboard
- [ ] GET `/air-quality/current` retorna 200
- [ ] GET `/stations` retorna 200
- [ ] GET `/stations/{id}/readings/current` retorna 200 (x3)
- [ ] Card AQI muestra valor correcto
- [ ] Color del AQI corresponde al nivel
- [ ] Estaciones listadas con sus AQI
- [ ] Gráfico Chart.js renderizado
- [ ] Sin errores en console

### Researcher Dashboard
- [ ] GET `/daily-stats` retorna 200
- [ ] Gráfico muestra tendencia inicial
- [ ] Tabla poblada con datos
- [ ] Filtros de ciudad funcionan
- [ ] Filtros de fecha funcionan
- [ ] Botón "Apply" actualiza datos
- [ ] Botón "Reset" limpia filtros
- [ ] Export CSV descarga archivo
- [ ] Download JSON descarga archivo

### Admin Dashboard
- [ ] Vista carga sin errores
- [ ] (Funcionalidad por implementar)

---

## 🎓 Tips para Debugging

### Si el backend no responde:
```bash
# Verificar que esté corriendo
curl http://localhost:8000/api/v1/admin/health

# Ver procesos Python
ps aux | grep python

# Reiniciar backend
cd /ruta/al/backend
uvicorn main:app --reload
```

### Si hay errores CORS:
```python
# En el backend (FastAPI):
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Si el token expira:
```javascript
// Limpiar localStorage y hacer login nuevamente
localStorage.clear()
// Navegar a /login
```

### Si los datos no se actualizan:
```javascript
// En Console, forzar recarga sin caché:
location.reload(true)
// O Ctrl+Shift+R (Windows) / Cmd+Shift+R (Mac)
```

---

## 📈 Métricas de Éxito

### Performance
- ⏱️ Carga inicial < 2 segundos
- ⏱️ Peticiones API < 500ms
- ⏱️ Renderizado gráficos < 1 segundo

### Funcionalidad
- ✅ 100% de peticiones con status 200
- ✅ 0 errores en console
- ✅ Datos correctos en todas las vistas

### UX
- ✅ Mensajes de loading visibles
- ✅ Errores manejados con mensajes claros
- ✅ Navegación intuitiva

---

## 📞 Soporte

Si encuentras problemas, revisa:
1. **TEST_RESULTS.md** - Resultados de pruebas previas
2. **INTEGRATION_COMPLETE.md** - Documentación de integración
3. **API_CONTRACT.md** - Contrato de API del backend
4. **DevTools Console** - Errores específicos

---

**¡Listo para probar!** 🚀

Sigue estos pasos en orden y documenta cualquier error que encuentres para debug posterior.

