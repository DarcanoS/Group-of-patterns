# 📚 Índice de Documentación - API Backend

## 🎯 Comienza Aquí

¿Eres del equipo de frontend y necesitas integrar con el backend? **Empieza por aquí:**

👉 **[README_INTEGRATION.md](./README_INTEGRATION.md)** - Resumen ejecutivo con todo lo que necesitas saber

---

## 📖 Documentación Completa

### Para Desarrolladores Frontend

| Documento | Descripción | Cuándo Usar |
|-----------|-------------|-------------|
| **[README_INTEGRATION.md](./README_INTEGRATION.md)** | 🎯 **EMPIEZA AQUÍ** - Resumen ejecutivo | Primer documento a leer |
| **[API_CONTRACT.md](./API_CONTRACT.md)** | 📘 Contrato completo de la API | Referencia de todos los endpoints |
| **[FRONTEND_INTEGRATION_GUIDE.md](./FRONTEND_INTEGRATION_GUIDE.md)** | 🚀 Guía de integración paso a paso | Durante la implementación |
| **[TESTING_GUIDE.md](./TESTING_GUIDE.md)** | 🧪 Ejemplos de testing (cURL/Postman) | Para probar endpoints |
| **[api-types.ts](./api-types.ts)** | 📦 Tipos TypeScript | Copiar a tu proyecto |
| **[api-client-example.ts](./api-client-example.ts)** | 💻 Cliente API listo para usar | Copiar a tu proyecto |

---

## 🗂️ Estructura de la Documentación

```
📁 backend/
│
├── 📄 README_INTEGRATION.md          ⭐ EMPIEZA AQUÍ
│   └── Resumen ejecutivo con quick start
│
├── 📄 API_CONTRACT.md                 📘 Referencia Principal
│   ├── Todos los endpoints (24 total)
│   ├── Request/Response schemas
│   ├── Códigos de error
│   ├── Modelos de datos
│   └── Ejemplos completos
│
├── 📄 FRONTEND_INTEGRATION_GUIDE.md   🚀 Guía de Implementación
│   ├── Setup inicial
│   ├── Configuración del cliente
│   ├── Ejemplos con React
│   ├── Manejo de autenticación
│   ├── React Query integration
│   └── Checklist de integración
│
├── 📄 TESTING_GUIDE.md                🧪 Testing & Validación
│   ├── Ejemplos cURL
│   ├── Colecciones Postman
│   ├── Scripts de testing
│   └── Validación de respuestas
│
├── 📄 api-types.ts                    📦 Tipos TypeScript
│   ├── Interfaces de todos los modelos
│   ├── Tipos de request/response
│   ├── Enums y constantes
│   └── Utilidades de tipos
│
└── 📄 api-client-example.ts           💻 Cliente API
    ├── Cliente completo y funcional
    ├── Manejo de autenticación
    ├── Todos los endpoints
    ├── Manejo de errores
    └── Ejemplos de uso
```

---

## 🚀 Quick Start (3 Pasos)

### 1️⃣ Lee el Resumen
```bash
# Abre y lee este archivo primero (10 minutos)
open README_INTEGRATION.md
```

### 2️⃣ Copia los Archivos al Frontend
```bash
# Copia los tipos TypeScript
cp api-types.ts /path/to/frontend/src/types/

# Copia el cliente API
cp api-client-example.ts /path/to/frontend/src/api/
```

### 3️⃣ Configura y Usa
```typescript
// src/api/index.ts
import { AirQualityAPI } from './api-client-example';

export const api = new AirQualityAPI('http://localhost:8000/api/v1');

// Úsalo en tus componentes
const response = await api.auth.login(email, password);
api.setToken(response.access_token);
const dashboard = await api.airQuality.getDashboard({ city: 'New York' });
```

---

## 📋 Endpoints Principales

### Resumen Rápido

| Categoría | Cantidad | Auth | Principales Endpoints |
|-----------|----------|------|----------------------|
| Authentication | 2 | Mixto | `/auth/login`, `/auth/me` |
| Stations | 3 | Público | `/stations`, `/stations/{id}/readings/current` |
| Air Quality | 3 | Público | `/air-quality/current`, `/air-quality/dashboard` |
| Recommendations | 2 | Requerido | `/recommendations/current`, `/recommendations/history` |
| Admin | 7 | Admin | `/admin/stations`, `/admin/users` |
| Settings | 4 | Requerido | `/settings/preferences`, `/settings/dashboard` |
| Reports | 3 | Requerido | `/reports` |

**Total: 24 endpoints**

Ver detalles completos en **[API_CONTRACT.md](./API_CONTRACT.md)**

---

## 🎨 Patrones de Diseño

| Patrón | Endpoint | Archivo Documentación |
|--------|----------|----------------------|
| **Strategy** | `/air-quality/current` | `docs/strategy/` |
| **Builder** | `/air-quality/dashboard` | `docs/builder/` |
| **Factory** | `/recommendations/current` | `docs/factory/` |
| **Prototype** | `/settings/dashboard` | `docs/prototype/` |

---

## 🔐 Autenticación

### Flujo Básico
```
1. POST /auth/login → Obtener token
2. Guardar token en localStorage
3. Incluir en headers: Authorization: Bearer {token}
4. GET /auth/me → Validar token
```

### Niveles de Acceso
- 🟢 **Público**: Sin auth (Stations, Air Quality básico)
- 🟡 **Usuario**: Token requerido (Recommendations, Settings, Reports)
- 🔴 **Admin**: Role Admin requerido (Admin endpoints)

Ver más en **[API_CONTRACT.md#autenticación](./API_CONTRACT.md#autenticación)**

---

## 📦 Archivos para Copiar al Frontend

### Archivos Esenciales

1. **api-types.ts** → `frontend/src/types/api-types.ts`
   - Todos los tipos TypeScript
   - Interfaces y enums
   - Constantes útiles

2. **api-client-example.ts** → `frontend/src/api/client.ts`
   - Cliente API completo
   - Manejo de auth
   - Todos los endpoints

### Cómo Copiarlos

```bash
# Opción 1: Copiar directamente
cp api-types.ts ../frontend/src/types/
cp api-client-example.ts ../frontend/src/api/

# Opción 2: Crear symlinks (desarrollo)
ln -s $(pwd)/api-types.ts ../frontend/src/types/
ln -s $(pwd)/api-client-example.ts ../frontend/src/api/
```

---

## 🧪 Testing

### Testing Rápido con cURL

```bash
# 1. Health check
curl http://localhost:8000/api/v1/admin/health

# 2. Login
curl -X POST http://localhost:8000/api/v1/auth/login \
  -d "username=user@example.com&password=password123"

# 3. Dashboard
curl http://localhost:8000/api/v1/air-quality/dashboard?city=New%20York
```

Ver todos los ejemplos en **[TESTING_GUIDE.md](./TESTING_GUIDE.md)**

---

## 💡 Casos de Uso Comunes

### 1. Login y Dashboard
```typescript
const { access_token } = await api.auth.login(email, password);
api.setToken(access_token);
const dashboard = await api.airQuality.getDashboard({ city: 'New York' });
```

### 2. Listar Estaciones
```typescript
const stations = await api.stations.list({ city: 'New York', limit: 20 });
```

### 3. Obtener Recomendaciones
```typescript
const recommendation = await api.recommendations.getCurrent({ location: 'New York' });
console.log(recommendation.health_advice);
```

### 4. Admin - Crear Estación
```typescript
const station = await api.admin.createStation({
  name: 'New Station',
  latitude: 40.7128,
  longitude: -74.0060,
  city: 'New York',
  country: 'USA',
  region_id: 1
});
```

Más ejemplos en **[FRONTEND_INTEGRATION_GUIDE.md](./FRONTEND_INTEGRATION_GUIDE.md)**

---

## 🗺️ Mapa de Navegación

### ¿Qué documento necesito?

```
┌─────────────────────────────────────────────────┐
│  ¿Qué necesitas hacer?                          │
└─────────────────────────────────────────────────┘
                      │
          ┌───────────┼───────────┐
          ▼           ▼           ▼
    
📖 Entender    💻 Implementar    🧪 Probar
   la API         en Frontend      Endpoints
      │               │              │
      ▼               ▼              ▼
      
API_CONTRACT   INTEGRATION_GUIDE  TESTING_GUIDE
      +               +               +
README_INTEGRATION  api-types.ts  Postman/cURL
                  api-client.ts
```

### Por Rol

**👨‍💻 Desarrollador Frontend - Primera vez**
1. `README_INTEGRATION.md` (resumen)
2. `FRONTEND_INTEGRATION_GUIDE.md` (implementación)
3. Copiar `api-types.ts` y `api-client-example.ts`
4. `API_CONTRACT.md` (referencia cuando necesites)

**🔍 Desarrollador Frontend - Buscando un endpoint**
→ `API_CONTRACT.md` (buscar el endpoint específico)

**🧪 QA / Testing**
→ `TESTING_GUIDE.md` (ejemplos de cURL y Postman)

**📚 Documentación / Referencia**
→ `API_CONTRACT.md` (documentación completa)

---

## ✅ Checklist de Integración

### Setup (10 minutos)
- [ ] Leer `README_INTEGRATION.md`
- [ ] Copiar `api-types.ts` a tu proyecto
- [ ] Copiar `api-client-example.ts` a tu proyecto
- [ ] Configurar variable de entorno `API_URL`

### Implementación Básica (1-2 horas)
- [ ] Crear página de Login
- [ ] Implementar AuthManager
- [ ] Crear Dashboard básico
- [ ] Listar estaciones

### Funcionalidades Avanzadas (2-4 horas)
- [ ] Recomendaciones personalizadas
- [ ] Configuración de usuario
- [ ] Generación de reportes
- [ ] Panel admin (si aplica)

### Testing y Optimización (1-2 horas)
- [ ] Probar todos los endpoints
- [ ] Implementar manejo de errores
- [ ] Agregar loading states
- [ ] Implementar cache/polling

---

## 🆘 Problemas Comunes

### ❌ Error: CORS
**Solución**: Verificar que el backend acepta tu origen. Ya configurado para `localhost:3000` y `localhost:5173`

### ❌ Error: 401 Unauthorized
**Solución**: 
1. Verificar que tienes el token
2. Verificar formato: `Authorization: Bearer {token}`
3. Token puede estar expirado - hacer login de nuevo

### ❌ Error: 404 Not Found
**Solución**: Verificar que el endpoint existe en `API_CONTRACT.md` y que la URL base es correcta

### ❌ Error: 422 Validation Error
**Solución**: Verificar que los datos enviados cumplen con el schema en `API_CONTRACT.md`

---

## 🌐 URLs Importantes

### Desarrollo
- **API Base**: `http://localhost:8000/api/v1`
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

### Testing
```bash
# Health check
curl http://localhost:8000/api/v1/admin/health

# Ver documentación interactiva
open http://localhost:8000/docs
```

---

## 📊 Estadísticas del Proyecto

- **Total Endpoints**: 24
- **Patrones de Diseño**: 4 (Strategy, Builder, Factory, Prototype)
- **Modelos de Datos**: 12+
- **Niveles de Auth**: 3 (Público, Usuario, Admin)
- **Líneas de Documentación**: 2000+
- **Ejemplos de Código**: 50+

---

## 🎯 Recomendaciones

### Para Máxima Productividad

1. **Lee primero** `README_INTEGRATION.md` (15 min)
2. **Implementa el cliente** copiando los archivos TypeScript (30 min)
3. **Sigue los ejemplos** de `FRONTEND_INTEGRATION_GUIDE.md` (1-2 horas)
4. **Usa** `API_CONTRACT.md` como referencia cuando necesites
5. **Prueba** con `TESTING_GUIDE.md` para validar

### Herramientas Recomendadas

- **VS Code** con extensión REST Client
- **Postman** para testing manual
- **React Query** para manejo de estado (opcional)
- **TypeScript** para type safety

---

## 📞 Soporte

### Orden de Resolución

1. ✅ Buscar en `API_CONTRACT.md`
2. ✅ Revisar ejemplos en `FRONTEND_INTEGRATION_GUIDE.md`
3. ✅ Probar con ejemplos de `TESTING_GUIDE.md`
4. ✅ Revisar `README_INTEGRATION.md` - Problemas Comunes
5. ✅ Contactar al equipo de backend

---

## 🎉 ¡Todo Listo!

Tienes toda la documentación necesaria para integrar el frontend con el backend.

**Próximo paso**: Abre **[README_INTEGRATION.md](./README_INTEGRATION.md)** y comienza la integración.

---

**Happy Coding! 🚀**

*Última actualización: 27 de Noviembre, 2025*
*Versión: 1.0.0*

