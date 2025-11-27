# 📋 Resumen Ejecutivo - Documentación de API para Frontend

## 🎯 Archivos Generados

Se han creado **4 documentos completos** para facilitar la integración del frontend con el backend:

| Archivo | Descripción | Uso Principal |
|---------|-------------|---------------|
| **API_CONTRACT.md** | Contrato completo de la API con todos los endpoints, request/response, ejemplos | Referencia principal para desarrolladores |
| **api-types.ts** | Definiciones TypeScript de todos los tipos de datos | Copiar al proyecto frontend para type safety |
| **api-client-example.ts** | Cliente JavaScript/TypeScript listo para usar | Integrar directamente en el frontend |
| **FRONTEND_INTEGRATION_GUIDE.md** | Guía paso a paso de integración con ejemplos de React | Seguir para implementar en frontend |
| **TESTING_GUIDE.md** | Ejemplos de cURL y Postman para testing | Testing manual y automatizado |

---

## 🚀 Quick Start para Frontend

### 1. Copiar Archivos
```bash
cp api-types.ts /path/to/frontend/src/types/
cp api-client-example.ts /path/to/frontend/src/api/
```

### 2. Configurar API
```typescript
// src/api/index.ts
import { AirQualityAPI } from './api-client-example';

export const api = new AirQualityAPI('http://localhost:8000/api/v1');
```

### 3. Usar en Componente
```typescript
// Login
const response = await api.auth.login(email, password);
api.setToken(response.access_token);

// Dashboard
const dashboard = await api.airQuality.getDashboard({ city: 'New York' });
```

---

## 📊 Endpoints Disponibles

### Resumen por Categoría

| Categoría | Endpoints | Autenticación | Principales Funciones |
|-----------|-----------|---------------|----------------------|
| **Authentication** | 2 | 🟢 Mixto | Login, obtener usuario actual |
| **Stations** | 3 | 🟢 Público | Listar estaciones, ver lecturas |
| **Air Quality** | 3 | 🟢 Público | AQI actual, dashboard, estadísticas |
| **Recommendations** | 2 | 🟡 Requiere auth | Recomendaciones personalizadas |
| **Admin** | 7 | 🔴 Solo admin | Gestión de estaciones y usuarios |
| **Settings** | 4 | 🟡 Requiere auth | Preferencias y configuración |
| **Reports** | 3 | 🟡 Requiere auth | Generar y consultar reportes |

**Total: 24 endpoints**

### Endpoints Más Importantes

```typescript
// 🔐 Autenticación
POST   /auth/login              // Login y obtener token
GET    /auth/me                 // Info del usuario actual

// 🏭 Estaciones
GET    /stations                // Listar todas las estaciones
GET    /stations/{id}/readings/current  // Lecturas actuales

// 🌫️ Calidad del Aire
GET    /air-quality/current     // AQI actual de una ciudad
GET    /air-quality/dashboard   // Dashboard completo (Builder Pattern)

// 💡 Recomendaciones
GET    /recommendations/current // Recomendación personalizada (Factory Pattern)

// ⚙️ Configuración
GET    /settings/preferences    // Preferencias del usuario
GET    /settings/dashboard      // Configuración de dashboard (Prototype Pattern)
```

---

## 🎨 Patrones de Diseño Implementados

| Patrón | Endpoint | Descripción | Beneficio |
|--------|----------|-------------|-----------|
| **Strategy** | `/air-quality/current` | Categorización de riesgo según AQI | Fácil agregar nuevas categorías |
| **Builder** | `/air-quality/dashboard` | Construcción de respuesta compleja | Datos estructurados y completos |
| **Factory** | `/recommendations/current` | Generación por tipo de usuario | Recomendaciones personalizadas |
| **Prototype** | `/settings/dashboard` | Clonación de configuraciones | Configuración rápida para nuevos usuarios |

---

## 🔐 Autenticación

### Flujo de Autenticación

```
1. Login → Obtener token
2. Guardar token (localStorage)
3. Incluir en headers: Authorization: Bearer {token}
4. Token válido por tiempo configurable
5. Renovar o logout cuando expire
```

### Niveles de Acceso

| Nivel | Descripción | Endpoints Disponibles |
|-------|-------------|----------------------|
| **Público** | Sin autenticación | Stations, Air Quality (lectura) |
| **Citizen** | Usuario regular | + Recommendations, Settings, Reports |
| **Researcher** | Investigador | + Datos adicionales, análisis |
| **Admin** | Administrador | + Gestión de estaciones y usuarios |

---

## 📦 Modelos de Datos Principales

### User (Usuario)
```typescript
{
  id: number
  email: string
  full_name: string
  role: { id, name, description }
  created_at: string
  is_active: boolean
}
```

### Station (Estación)
```typescript
{
  id: number
  name: string
  latitude: number
  longitude: number
  city: string
  country: string
  region: { id, name }
  is_active: boolean
}
```

### Dashboard Response
```typescript
{
  station: { id, name, city, ... }
  current_readings: [{ pollutant, value, aqi, ... }]
  daily_stats: { avg_aqi, max_aqi, min_aqi, ... }
  risk_assessment: { level, color, health_implications, ... }
}
```

### Recommendation
```typescript
{
  id: number
  location: string
  aqi: number
  risk_level: string
  health_advice: string[]
  actions: string[]
  products: [{ type, name, priority, ... }]
}
```

---

## 🌐 Configuración del Frontend

### Variables de Entorno

```bash
# .env
REACT_APP_API_URL=http://localhost:8000/api/v1
VITE_API_URL=http://localhost:8000/api/v1

# Producción
# REACT_APP_API_URL=https://api.airquality.com/api/v1
```

### CORS

El backend está configurado para aceptar requests de:
- `http://localhost:3000` (React)
- `http://localhost:5173` (Vite)
- Otros orígenes configurados en producción

---

## 🧪 Testing

### Testing Manual con cURL

```bash
# 1. Login
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=user@example.com&password=password123"

# 2. Obtener dashboard
curl "http://localhost:8000/api/v1/air-quality/dashboard?city=New%20York"

# 3. Recomendación (con auth)
curl -H "Authorization: Bearer {token}" \
  "http://localhost:8000/api/v1/recommendations/current?location=New%20York"
```

Ver **TESTING_GUIDE.md** para ejemplos completos.

---

## 💡 Ejemplos de Uso

### Ejemplo 1: Login y Dashboard

```typescript
import { api } from './api';

async function loadDashboard() {
  // 1. Login
  const { access_token, user } = await api.auth.login(
    'user@example.com', 
    'password123'
  );
  
  // 2. Configurar token
  api.setToken(access_token);
  localStorage.setItem('token', access_token);
  
  // 3. Obtener dashboard
  const dashboard = await api.airQuality.getDashboard({ 
    city: 'New York' 
  });
  
  console.log('AQI:', dashboard.daily_stats.avg_aqi);
  console.log('Nivel de riesgo:', dashboard.risk_assessment.level);
}
```

### Ejemplo 2: Listar Estaciones con Mapa

```typescript
async function loadStations() {
  const stations = await api.stations.list({
    city: 'New York',
    limit: 50
  });
  
  // Mostrar en mapa
  stations.forEach(station => {
    addMarkerToMap({
      lat: station.latitude,
      lng: station.longitude,
      title: station.name,
      city: station.city
    });
  });
}
```

### Ejemplo 3: Recomendaciones Personalizadas

```typescript
async function getRecommendations() {
  // Requiere autenticación
  const token = localStorage.getItem('token');
  api.setToken(token);
  
  const recommendation = await api.recommendations.getCurrent({
    location: 'New York'
  });
  
  // Mostrar consejos de salud
  recommendation.health_advice.forEach(advice => {
    console.log('✓', advice);
  });
  
  // Mostrar productos recomendados
  const highPriority = recommendation.products.filter(
    p => p.priority === 'high'
  );
  console.log('Productos recomendados:', highPriority);
}
```

### Ejemplo 4: Admin - Crear Estación

```typescript
async function createStation(adminToken: string) {
  api.setToken(adminToken);
  
  const newStation = await api.admin.createStation({
    name: 'Central Park Station',
    latitude: 40.7829,
    longitude: -73.9654,
    city: 'New York',
    country: 'USA',
    region_id: 1
  });
  
  console.log('Estación creada:', newStation.id);
}
```

---

## ⚠️ Manejo de Errores

### Códigos HTTP

| Código | Significado | Acción Frontend |
|--------|-------------|-----------------|
| 200 | OK | Procesar respuesta |
| 201 | Created | Recurso creado exitosamente |
| 400 | Bad Request | Validar entrada del usuario |
| 401 | Unauthorized | Redirigir a login |
| 403 | Forbidden | Mostrar "Sin permisos" |
| 404 | Not Found | Mostrar "No encontrado" |
| 422 | Validation Error | Mostrar errores de validación |
| 500 | Server Error | Mostrar error general |

### Ejemplo de Manejo

```typescript
import { APIError } from './api/api-client-example';

try {
  const data = await api.airQuality.getCurrentAQI('New York');
  setData(data);
} catch (error) {
  if (error instanceof APIError) {
    switch (error.statusCode) {
      case 401:
        // Token expirado
        AuthManager.logout();
        break;
      case 404:
        setError('Ciudad no encontrada');
        break;
      default:
        setError(error.message);
    }
  } else {
    setError('Error de conexión');
  }
}
```

---

## 📱 Integración con React Query (Opcional)

```typescript
import { useQuery } from '@tanstack/react-query';
import { api } from './api';

function useDashboard(city: string) {
  return useQuery({
    queryKey: ['dashboard', city],
    queryFn: () => api.airQuality.getDashboard({ city }),
    refetchInterval: 300000, // Refetch cada 5 minutos
  });
}

// Uso en componente
function Dashboard() {
  const { data, isLoading, error } = useDashboard('New York');
  
  if (isLoading) return <Spinner />;
  if (error) return <Error message={error.message} />;
  
  return <DashboardUI data={data} />;
}
```

---

## 📈 Métricas y Performance

### Recomendaciones

- **Caché**: Implementar cache para datos que no cambian frecuentemente
- **Polling**: Actualizar datos críticos cada 5 minutos
- **Debounce**: En búsquedas y filtros (300-500ms)
- **Paginación**: Usar skip/limit para grandes datasets
- **Lazy Loading**: Cargar datos bajo demanda

### Ejemplo de Polling

```typescript
useEffect(() => {
  const interval = setInterval(async () => {
    const data = await api.airQuality.getCurrentAQI(city);
    setAQI(data.aqi);
  }, 300000); // 5 minutos

  return () => clearInterval(interval);
}, [city]);
```

---

## ✅ Checklist de Integración

### Setup Inicial
- [ ] Copiar `api-types.ts` al proyecto
- [ ] Copiar `api-client-example.ts` al proyecto
- [ ] Configurar variable de entorno `API_URL`
- [ ] Instalar dependencias (si usa React Query, Axios, etc.)

### Autenticación
- [ ] Implementar página de Login
- [ ] Crear `AuthManager` o similar
- [ ] Guardar token en localStorage
- [ ] Configurar token en API client
- [ ] Implementar logout
- [ ] Proteger rutas privadas

### Funcionalidades
- [ ] Dashboard principal con AQI
- [ ] Lista de estaciones
- [ ] Mapa con estaciones (opcional)
- [ ] Recomendaciones personalizadas
- [ ] Configuración de usuario
- [ ] Generación de reportes
- [ ] Panel de administración (si aplica)

### Testing
- [ ] Probar endpoints públicos
- [ ] Probar autenticación
- [ ] Probar endpoints protegidos
- [ ] Probar manejo de errores
- [ ] Probar en diferentes roles (Citizen, Admin)

### Optimización
- [ ] Implementar loading states
- [ ] Implementar error boundaries
- [ ] Agregar cache (React Query o similar)
- [ ] Optimizar renders
- [ ] Implementar lazy loading

---

## 🆘 Solución de Problemas

### Problema: CORS Error

**Solución:**
```typescript
// Verificar que el backend tiene configurado CORS
// En FastAPI (ya configurado):
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Problema: 401 Unauthorized

**Solución:**
```typescript
// Verificar que el token está siendo enviado
console.log('Token:', localStorage.getItem('token'));

// Verificar formato del header
// Debe ser: Authorization: Bearer {token}
```

### Problema: Datos no se actualizan

**Solución:**
```typescript
// Implementar polling o usar React Query
const { data, refetch } = useQuery(...);

// Forzar actualización
useEffect(() => {
  const interval = setInterval(() => refetch(), 300000);
  return () => clearInterval(interval);
}, []);
```

---

## 📚 Recursos Adicionales

### Documentación
- **Contrato completo**: `API_CONTRACT.md` - Todos los endpoints detallados
- **Guía de integración**: `FRONTEND_INTEGRATION_GUIDE.md` - Paso a paso
- **Testing**: `TESTING_GUIDE.md` - Ejemplos de cURL y Postman
- **Tipos TypeScript**: `api-types.ts` - Type definitions

### Links Útiles
- FastAPI Docs: http://localhost:8000/docs (Swagger UI)
- ReDoc: http://localhost:8000/redoc (Documentación alternativa)

---

## 🎯 Próximos Pasos

1. **Leer** `API_CONTRACT.md` para entender todos los endpoints
2. **Copiar** archivos TypeScript al proyecto frontend
3. **Seguir** `FRONTEND_INTEGRATION_GUIDE.md` para implementación
4. **Probar** con `TESTING_GUIDE.md` para validar integración
5. **Implementar** funcionalidades según prioridad
6. **Optimizar** con cache y manejo de errores

---

## 📞 Contacto y Soporte

Para dudas o problemas:
1. Revisar la documentación completa en `API_CONTRACT.md`
2. Verificar ejemplos en `FRONTEND_INTEGRATION_GUIDE.md`
3. Probar endpoints con ejemplos de `TESTING_GUIDE.md`
4. Contactar al equipo de backend

---

**¡Buena suerte con la integración! 🚀**

*Última actualización: 27 de Noviembre, 2025*

