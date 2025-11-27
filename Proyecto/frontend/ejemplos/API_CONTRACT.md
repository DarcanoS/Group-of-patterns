# 📘 Contrato de API - Backend Air Quality Monitoring

**Versión:** 1.0.0  
**Base URL:** `http://localhost:8000/api/v1`  
**Fecha:** 27 de Noviembre, 2025

---

## 📋 Tabla de Contenidos

1. [Autenticación](#autenticación)
2. [Endpoints de Authentication](#1-authentication)
3. [Endpoints de Stations](#2-stations)
4. [Endpoints de Air Quality](#3-air-quality)
5. [Endpoints de Recommendations](#4-recommendations)
6. [Endpoints de Admin](#5-admin)
7. [Endpoints de Settings](#6-settings)
8. [Endpoints de Reports](#7-reports)
9. [Modelos de Datos](#modelos-de-datos)
10. [Códigos de Error](#códigos-de-error)

---

## 🔐 Autenticación

### Tipo de Autenticación
- **Bearer Token** (JWT)
- Header: `Authorization: Bearer {token}`

### Obtener Token
```http
POST /api/v1/auth/login
```

### Niveles de Acceso
- 🟢 **Público**: No requiere autenticación
- 🟡 **Usuario**: Requiere token de usuario autenticado
- 🔴 **Admin**: Requiere token de usuario con rol Admin

---

## 1. Authentication

### 1.1 Login (Iniciar Sesión)
**POST** `/api/v1/auth/login` 🟢

Obtiene un token de acceso para futuras peticiones.

**Request Body (form-data):**
```json
{
  "username": "user@example.com",  // Email del usuario
  "password": "password123"
}
```

**Response 200:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "full_name": "John Doe",
    "role": {
      "id": 1,
      "name": "Citizen",
      "description": "Regular citizen user"
    },
    "created_at": "2025-11-27T10:30:00",
    "is_active": true
  }
}
```

**Errores:**
- `401`: Email o contraseña incorrectos

**Ejemplo cURL:**
```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=user@example.com&password=password123"
```

---

### 1.2 Get Current User (Usuario Actual)
**GET** `/api/v1/auth/me` 🟡

Obtiene información del usuario autenticado.

**Headers:**
```
Authorization: Bearer {token}
```

**Response 200:**
```json
{
  "id": 1,
  "email": "user@example.com",
  "full_name": "John Doe",
  "role": {
    "id": 1,
    "name": "Citizen",
    "description": "Regular citizen user"
  },
  "created_at": "2025-11-27T10:30:00",
  "is_active": true
}
```

**Errores:**
- `401`: Token inválido o expirado

---

## 2. Stations

### 2.1 List Stations (Listar Estaciones)
**GET** `/api/v1/stations` 🟢

Lista todas las estaciones de monitoreo con filtros opcionales.

**Query Parameters:**
| Parámetro | Tipo | Requerido | Default | Descripción |
|-----------|------|-----------|---------|-------------|
| skip | int | No | 0 | Registros a omitir (paginación) |
| limit | int | No | 100 | Máximo de registros (1-1000) |
| city | string | No | - | Filtrar por ciudad |
| country | string | No | - | Filtrar por país |
| region_id | int | No | - | Filtrar por región |

**Response 200:**
```json
[
  {
    "id": 1,
    "name": "Downtown Station",
    "latitude": 40.7128,
    "longitude": -74.0060,
    "city": "New York",
    "country": "USA",
    "region": {
      "id": 1,
      "name": "North America",
      "description": "North American region"
    },
    "is_active": true,
    "created_at": "2025-01-15T08:00:00"
  }
]
```

**Ejemplo:**
```bash
curl "http://localhost:8000/api/v1/stations?city=New%20York&limit=10"
```

---

### 2.2 Get Station (Obtener Estación)
**GET** `/api/v1/stations/{station_id}` 🟢

Obtiene información detallada de una estación específica.

**Path Parameters:**
- `station_id` (int): ID de la estación

**Response 200:**
```json
{
  "id": 1,
  "name": "Downtown Station",
  "latitude": 40.7128,
  "longitude": -74.0060,
  "city": "New York",
  "country": "USA",
  "region": {
    "id": 1,
    "name": "North America",
    "description": "North American region"
  },
  "is_active": true,
  "created_at": "2025-01-15T08:00:00"
}
```

**Errores:**
- `404`: Estación no encontrada

---

### 2.3 Get Current Readings (Lecturas Actuales)
**GET** `/api/v1/stations/{station_id}/readings/current` 🟢

Obtiene las lecturas más recientes de todos los contaminantes para una estación.

**Path Parameters:**
- `station_id` (int): ID de la estación

**Response 200:**
```json
{
  "station": {
    "id": 1,
    "name": "Downtown Station",
    "city": "New York"
  },
  "readings": [
    {
      "pollutant": {
        "id": 1,
        "name": "PM2.5",
        "unit": "µg/m³",
        "description": "Fine particulate matter"
      },
      "value": 35.5,
      "timestamp": "2025-11-27T14:30:00",
      "aqi": 102
    },
    {
      "pollutant": {
        "id": 2,
        "name": "PM10",
        "unit": "µg/m³"
      },
      "value": 55.2,
      "timestamp": "2025-11-27T14:30:00",
      "aqi": 75
    }
  ],
  "last_updated": "2025-11-27T14:30:00"
}
```

**Errores:**
- `404`: Estación no encontrada

---

## 3. Air Quality

### 3.1 Get Current AQI (AQI Actual)
**GET** `/api/v1/air-quality/current` 🟢

Obtiene el índice de calidad del aire actual para una ciudad.

**Query Parameters:**
| Parámetro | Tipo | Requerido | Descripción |
|-----------|------|-----------|-------------|
| city | string | **Sí** | Nombre de la ciudad |

**Response 200:**
```json
{
  "city": "New York",
  "aqi": 102,
  "primary_pollutant": "PM2.5",
  "risk_category": {
    "level": "Unhealthy for Sensitive Groups",
    "color": "#FF9800",
    "health_implications": "Members of sensitive groups may experience health effects",
    "cautionary_statement": "Active children and adults, and people with respiratory disease should limit prolonged outdoor exertion"
  },
  "timestamp": "2025-11-27T14:30:00",
  "station": {
    "id": 1,
    "name": "Downtown Station"
  }
}
```

**Errores:**
- `404`: No se encontraron datos para la ciudad

**Ejemplo:**
```bash
curl "http://localhost:8000/api/v1/air-quality/current?city=New%20York"
```

---

### 3.2 Get Dashboard Data (Datos del Dashboard)
**GET** `/api/v1/air-quality/dashboard` 🟢

Obtiene datos completos para el dashboard (usa patrón Builder).

**Query Parameters:**
| Parámetro | Tipo | Requerido | Descripción |
|-----------|------|-----------|-------------|
| city | string | No* | Nombre de la ciudad |
| station_id | int | No* | ID de la estación |

*Uno de los dos es requerido

**Response 200:**
```json
{
  "station": {
    "id": 1,
    "name": "Downtown Station",
    "city": "New York",
    "country": "USA",
    "latitude": 40.7128,
    "longitude": -74.0060
  },
  "current_readings": [
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
  "daily_stats": {
    "date": "2025-11-27",
    "avg_aqi": 95.5,
    "max_aqi": 115,
    "min_aqi": 78,
    "dominant_pollutant": "PM2.5"
  },
  "risk_assessment": {
    "level": "Unhealthy for Sensitive Groups",
    "color": "#FF9800",
    "health_implications": "Members of sensitive groups may experience health effects",
    "recommended_actions": [
      "Limit prolonged outdoor exertion",
      "Close windows",
      "Use air purifier indoors"
    ]
  },
  "last_updated": "2025-11-27T14:30:00"
}
```

**Ejemplo:**
```bash
curl "http://localhost:8000/api/v1/air-quality/dashboard?city=New%20York"
```

---

### 3.3 Get Daily Stats (Estadísticas Diarias)
**GET** `/api/v1/air-quality/daily-stats` 🟢

Obtiene estadísticas diarias agregadas con filtros.

**Query Parameters:**
| Parámetro | Tipo | Requerido | Descripción |
|-----------|------|-----------|-------------|
| station_id | int | No | Filtrar por estación |
| pollutant_id | int | No | Filtrar por contaminante |
| start_date | date | No | Fecha inicio (YYYY-MM-DD) |
| end_date | date | No | Fecha fin (YYYY-MM-DD) |
| skip | int | No | Paginación (default: 0) |
| limit | int | No | Límite (default: 100) |

**Response 200:**
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
  }
]
```

**Ejemplo:**
```bash
curl "http://localhost:8000/api/v1/air-quality/daily-stats?station_id=1&start_date=2025-11-01&end_date=2025-11-27"
```

---

## 4. Recommendations

### 4.1 Get Current Recommendation (Recomendación Actual)
**GET** `/api/v1/recommendations/current` 🟡

Genera una recomendación personalizada usando el patrón Factory según el rol del usuario.

**Headers:**
```
Authorization: Bearer {token}
```

**Query Parameters:**
| Parámetro | Tipo | Requerido | Descripción |
|-----------|------|-----------|-------------|
| location | string | No | Ubicación específica |
| aqi | int | No | Valor AQI explícito (0-500) |

**Response 200:**
```json
{
  "id": 1,
  "user_id": 1,
  "location": "New York",
  "aqi": 102,
  "risk_level": "Unhealthy for Sensitive Groups",
  "recommendation_text": "Based on current air quality conditions, we recommend the following actions...",
  "health_advice": [
    "Limit prolonged outdoor activities",
    "Keep windows closed",
    "Monitor symptoms if you have respiratory conditions"
  ],
  "actions": [
    "Use N95 masks when going outside",
    "Enable air purifiers indoors",
    "Check air quality before planning outdoor activities"
  ],
  "products": [
    {
      "type": "mask",
      "name": "N95 Respirator Mask",
      "description": "High-efficiency mask for particle filtration",
      "priority": "high"
    },
    {
      "type": "air_purifier",
      "name": "HEPA Air Purifier",
      "description": "Removes 99.97% of particles from indoor air",
      "priority": "medium"
    }
  ],
  "created_at": "2025-11-27T14:30:00"
}
```

**Ejemplo:**
```bash
curl -H "Authorization: Bearer {token}" \
  "http://localhost:8000/api/v1/recommendations/current?location=New%20York"
```

---

### 4.2 Get Recommendation History (Historial)
**GET** `/api/v1/recommendations/history` 🟡

Obtiene el historial de recomendaciones del usuario.

**Headers:**
```
Authorization: Bearer {token}
```

**Query Parameters:**
| Parámetro | Tipo | Requerido | Default |
|-----------|------|-----------|---------|
| skip | int | No | 0 |
| limit | int | No | 100 |

**Response 200:**
```json
[
  {
    "id": 1,
    "location": "New York",
    "aqi": 102,
    "risk_level": "Unhealthy for Sensitive Groups",
    "recommendation_text": "...",
    "created_at": "2025-11-27T14:30:00"
  }
]
```

---

## 5. Admin

### 5.1 Health Check
**GET** `/api/v1/admin/health` 🟢

Verifica el estado de la API y la base de datos.

**Response 200:**
```json
{
  "status": "healthy",
  "database": "connected",
  "message": "Database contains 6 pollutants"
}
```

---

### 5.2 List Stations (Admin)
**GET** `/api/v1/admin/stations` 🔴

Lista todas las estaciones (solo administradores).

**Headers:**
```
Authorization: Bearer {admin_token}
```

**Query Parameters:**
| Parámetro | Tipo | Default |
|-----------|------|---------|
| skip | int | 0 |
| limit | int | 100 |

**Response 200:**
```json
[
  {
    "id": 1,
    "name": "Downtown Station",
    "latitude": 40.7128,
    "longitude": -74.0060,
    "city": "New York",
    "country": "USA",
    "region": {...},
    "is_active": true,
    "created_at": "2025-01-15T08:00:00"
  }
]
```

**Errores:**
- `403`: Permisos insuficientes (no es admin)

---

### 5.3 Create Station (Crear Estación)
**POST** `/api/v1/admin/stations` 🔴

Crea una nueva estación de monitoreo.

**Headers:**
```
Authorization: Bearer {admin_token}
```

**Request Body:**
```json
{
  "name": "New Station",
  "latitude": 40.7128,
  "longitude": -74.0060,
  "city": "New York",
  "country": "USA",
  "region_id": 1
}
```

**Response 201:**
```json
{
  "id": 2,
  "name": "New Station",
  "latitude": 40.7128,
  "longitude": -74.0060,
  "city": "New York",
  "country": "USA",
  "region": {
    "id": 1,
    "name": "North America"
  },
  "is_active": true,
  "created_at": "2025-11-27T14:30:00"
}
```

**Errores:**
- `403`: Permisos insuficientes
- `422`: Datos de validación incorrectos

---

### 5.4 Update Station (Actualizar Estación)
**PUT** `/api/v1/admin/stations/{station_id}` 🔴

Actualiza una estación existente.

**Headers:**
```
Authorization: Bearer {admin_token}
```

**Path Parameters:**
- `station_id` (int): ID de la estación

**Request Body (todos los campos opcionales):**
```json
{
  "name": "Updated Station Name",
  "latitude": 40.7200,
  "longitude": -74.0100,
  "city": "New York City",
  "country": "USA",
  "is_active": false
}
```

**Response 200:**
```json
{
  "id": 1,
  "name": "Updated Station Name",
  "latitude": 40.7200,
  "longitude": -74.0100,
  "city": "New York City",
  "country": "USA",
  "region": {...},
  "is_active": false,
  "created_at": "2025-01-15T08:00:00"
}
```

**Errores:**
- `403`: Permisos insuficientes
- `404`: Estación no encontrada
- `422`: Datos de validación incorrectos

---

### 5.5 Delete Station (Eliminar Estación)
**DELETE** `/api/v1/admin/stations/{station_id}` 🔴

Elimina una estación de monitoreo.

**Headers:**
```
Authorization: Bearer {admin_token}
```

**Path Parameters:**
- `station_id` (int): ID de la estación

**Response 200:**
```json
{
  "message": "Station 1 deleted successfully"
}
```

**Errores:**
- `403`: Permisos insuficientes
- `404`: Estación no encontrada

---

### 5.6 List Users (Listar Usuarios)
**GET** `/api/v1/admin/users` 🔴

Lista todos los usuarios del sistema.

**Headers:**
```
Authorization: Bearer {admin_token}
```

**Query Parameters:**
| Parámetro | Tipo | Default |
|-----------|------|---------|
| skip | int | 0 |
| limit | int | 100 |

**Response 200:**
```json
[
  {
    "id": 1,
    "email": "user@example.com",
    "full_name": "John Doe",
    "role": {
      "id": 1,
      "name": "Citizen"
    },
    "created_at": "2025-11-01T10:00:00",
    "is_active": true
  }
]
```

**Errores:**
- `403`: Permisos insuficientes

---

### 5.7 Update User Role (Actualizar Rol)
**PUT** `/api/v1/admin/users/{user_id}/role` 🔴

Actualiza el rol de un usuario.

**Headers:**
```
Authorization: Bearer {admin_token}
```

**Path Parameters:**
- `user_id` (int): ID del usuario

**Request Body:**
```json
{
  "role_id": 2
}
```

**Response 200:**
```json
{
  "id": 1,
  "email": "user@example.com",
  "full_name": "John Doe",
  "role": {
    "id": 2,
    "name": "Researcher",
    "description": "Research and analysis role"
  },
  "created_at": "2025-11-01T10:00:00",
  "is_active": true
}
```

**Errores:**
- `403`: Permisos insuficientes
- `404`: Usuario no encontrado

---

## 6. Settings

### 6.1 Get User Preferences (Obtener Preferencias)
**GET** `/api/v1/settings/preferences` 🟡

Obtiene las preferencias del usuario actual.

**Headers:**
```
Authorization: Bearer {token}
```

**Response 200:**
```json
{
  "user_id": 1,
  "theme": "dark",
  "language": "en",
  "notifications_enabled": true,
  "email_alerts": true,
  "aqi_threshold": 100,
  "preferred_units": "metric"
}
```

---

### 6.2 Update User Preferences (Actualizar Preferencias)
**PUT** `/api/v1/settings/preferences` 🟡

Actualiza las preferencias del usuario.

**Headers:**
```
Authorization: Bearer {token}
```

**Request Body (todos los campos opcionales):**
```json
{
  "theme": "light",
  "language": "es",
  "notifications_enabled": false,
  "email_alerts": true,
  "aqi_threshold": 150,
  "preferred_units": "imperial"
}
```

**Response 200:**
```json
{
  "user_id": 1,
  "theme": "light",
  "language": "es",
  "notifications_enabled": false,
  "email_alerts": true,
  "aqi_threshold": 150,
  "preferred_units": "imperial"
}
```

---

### 6.3 Get Dashboard Config (Configuración Dashboard)
**GET** `/api/v1/settings/dashboard` 🟡

Obtiene la configuración personalizada del dashboard (usa patrón Prototype).

**Headers:**
```
Authorization: Bearer {token}
```

**Response 200:**
```json
{
  "user_id": 1,
  "widgets": [
    {
      "id": "aqi-gauge",
      "type": "gauge",
      "position": {"x": 0, "y": 0},
      "size": {"width": 2, "height": 2},
      "settings": {
        "show_history": true,
        "time_range": "24h"
      }
    },
    {
      "id": "pollutants-chart",
      "type": "chart",
      "position": {"x": 2, "y": 0},
      "size": {"width": 4, "height": 2},
      "settings": {
        "chart_type": "line",
        "pollutants": ["PM2.5", "PM10", "O3"]
      }
    }
  ],
  "layout": "grid",
  "refresh_interval": 300
}
```

---

### 6.4 Update Dashboard Config (Actualizar Dashboard)
**PUT** `/api/v1/settings/dashboard` 🟡

Actualiza la configuración del dashboard.

**Headers:**
```
Authorization: Bearer {token}
```

**Request Body:**
```json
{
  "widgets": [
    {
      "id": "aqi-gauge",
      "type": "gauge",
      "position": {"x": 0, "y": 0},
      "size": {"width": 3, "height": 2},
      "settings": {
        "show_history": true,
        "time_range": "48h"
      }
    }
  ],
  "layout": "flex",
  "refresh_interval": 180
}
```

**Response 200:**
```json
{
  "user_id": 1,
  "widgets": [...],
  "layout": "flex",
  "refresh_interval": 180
}
```

---

## 7. Reports

### 7.1 Create Report (Crear Reporte)
**POST** `/api/v1/reports` 🟡

Crea un nuevo reporte de calidad del aire.

**Headers:**
```
Authorization: Bearer {token}
```

**Request Body:**
```json
{
  "city": "New York",
  "start_date": "2025-11-01",
  "end_date": "2025-11-27",
  "station_id": 1,
  "pollutant_id": 1
}
```

**Response 201:**
```json
{
  "id": 1,
  "user_id": 1,
  "city": "New York",
  "start_date": "2025-11-01",
  "end_date": "2025-11-27",
  "station_id": 1,
  "pollutant_id": 1,
  "file_path": "/reports/user_1/report_New_York_2025-11-01_2025-11-27.pdf",
  "status": "completed",
  "created_at": "2025-11-27T14:30:00"
}
```

---

### 7.2 List User Reports (Listar Reportes)
**GET** `/api/v1/reports` 🟡

Lista los reportes del usuario actual.

**Headers:**
```
Authorization: Bearer {token}
```

**Query Parameters:**
| Parámetro | Tipo | Default |
|-----------|------|---------|
| skip | int | 0 |
| limit | int | 100 |

**Response 200:**
```json
[
  {
    "id": 1,
    "user_id": 1,
    "city": "New York",
    "start_date": "2025-11-01",
    "end_date": "2025-11-27",
    "station_id": 1,
    "pollutant_id": 1,
    "file_path": "/reports/user_1/report_New_York_2025-11-01_2025-11-27.pdf",
    "status": "completed",
    "created_at": "2025-11-27T14:30:00"
  }
]
```

---

### 7.3 Get Report (Obtener Reporte)
**GET** `/api/v1/reports/{report_id}` 🟡

Obtiene un reporte específico.

**Headers:**
```
Authorization: Bearer {token}
```

**Path Parameters:**
- `report_id` (int): ID del reporte

**Response 200:**
```json
{
  "id": 1,
  "user_id": 1,
  "city": "New York",
  "start_date": "2025-11-01",
  "end_date": "2025-11-27",
  "station_id": 1,
  "pollutant_id": 1,
  "file_path": "/reports/user_1/report_New_York_2025-11-01_2025-11-27.pdf",
  "status": "completed",
  "created_at": "2025-11-27T14:30:00"
}
```

**Errores:**
- `403`: No tienes permiso para acceder a este reporte
- `404`: Reporte no encontrado

---

## 📊 Modelos de Datos

### User (Usuario)
```typescript
interface User {
  id: number;
  email: string;
  full_name: string;
  role: Role;
  created_at: string; // ISO 8601
  is_active: boolean;
}
```

### Role (Rol)
```typescript
interface Role {
  id: number;
  name: "Citizen" | "Researcher" | "Admin";
  description: string;
}
```

### Station (Estación)
```typescript
interface Station {
  id: number;
  name: string;
  latitude: number;
  longitude: number;
  city: string;
  country: string;
  region: Region;
  is_active: boolean;
  created_at: string;
}
```

### Region (Región)
```typescript
interface Region {
  id: number;
  name: string;
  description: string;
}
```

### Pollutant (Contaminante)
```typescript
interface Pollutant {
  id: number;
  name: string; // "PM2.5", "PM10", "O3", "NO2", "SO2", "CO"
  unit: string; // "µg/m³", "ppm"
  description: string;
}
```

### Reading (Lectura)
```typescript
interface Reading {
  pollutant: Pollutant;
  value: number;
  aqi: number;
  timestamp: string; // ISO 8601
}
```

### Risk Category (Categoría de Riesgo)
```typescript
interface RiskCategory {
  level: "Good" | "Moderate" | "Unhealthy for Sensitive Groups" | "Unhealthy" | "Very Unhealthy" | "Hazardous";
  color: string; // Hex color code
  health_implications: string;
  cautionary_statement: string;
}
```

### Recommendation (Recomendación)
```typescript
interface Recommendation {
  id: number;
  user_id: number;
  location: string;
  aqi: number;
  risk_level: string;
  recommendation_text: string;
  health_advice: string[];
  actions: string[];
  products: ProductRecommendation[];
  created_at: string;
}
```

### Product Recommendation
```typescript
interface ProductRecommendation {
  type: "mask" | "air_purifier" | "monitor" | "medication";
  name: string;
  description: string;
  priority: "low" | "medium" | "high";
}
```

### Daily Stats
```typescript
interface DailyStats {
  id: number;
  date: string; // YYYY-MM-DD
  station_id: number;
  pollutant_id: number;
  avg_value: number;
  max_value: number;
  min_value: number;
  avg_aqi: number;
  readings_count: number;
}
```

### Dashboard Config Widget
```typescript
interface Widget {
  id: string;
  type: "gauge" | "chart" | "map" | "table" | "alert";
  position: {
    x: number;
    y: number;
  };
  size: {
    width: number;
    height: number;
  };
  settings: Record<string, any>;
}
```

---

## ⚠️ Códigos de Error

### HTTP Status Codes

| Código | Nombre | Descripción |
|--------|--------|-------------|
| 200 | OK | Solicitud exitosa |
| 201 | Created | Recurso creado exitosamente |
| 400 | Bad Request | Solicitud mal formada |
| 401 | Unauthorized | No autenticado o token inválido |
| 403 | Forbidden | No autorizado (sin permisos) |
| 404 | Not Found | Recurso no encontrado |
| 422 | Unprocessable Entity | Error de validación |
| 500 | Internal Server Error | Error del servidor |

### Error Response Format

Todos los errores siguen este formato:

```json
{
  "detail": "Error message description"
}
```

O para errores de validación (422):

```json
{
  "detail": [
    {
      "loc": ["body", "field_name"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

---

## 🔄 Ejemplos de Flujos Comunes

### Flujo 1: Login y Obtener Dashboard
```bash
# 1. Login
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=user@example.com&password=password123"

# Response: { "access_token": "eyJ...", ... }

# 2. Obtener datos del dashboard
curl -H "Authorization: Bearer eyJ..." \
  "http://localhost:8000/api/v1/air-quality/dashboard?city=New%20York"
```

### Flujo 2: Obtener Recomendación Personalizada
```bash
# 1. Autenticarse (obtener token)
TOKEN="eyJ..."

# 2. Obtener recomendación actual
curl -H "Authorization: Bearer $TOKEN" \
  "http://localhost:8000/api/v1/recommendations/current?location=New%20York"

# 3. Ver historial de recomendaciones
curl -H "Authorization: Bearer $TOKEN" \
  "http://localhost:8000/api/v1/recommendations/history?limit=10"
```

### Flujo 3: Admin - Crear y Gestionar Estación
```bash
# 1. Login como admin
ADMIN_TOKEN="eyJ..."

# 2. Crear nueva estación
curl -X POST "http://localhost:8000/api/v1/admin/stations" \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Central Park Station",
    "latitude": 40.7829,
    "longitude": -73.9654,
    "city": "New York",
    "country": "USA",
    "region_id": 1
  }'

# 3. Listar todas las estaciones
curl -H "Authorization: Bearer $ADMIN_TOKEN" \
  "http://localhost:8000/api/v1/admin/stations"
```

---

## 🌐 CORS Configuration

El backend está configurado para aceptar peticiones de:
- `http://localhost:3000` (desarrollo frontend)
- `http://localhost:5173` (Vite)
- Otros orígenes configurados en producción

---

## 📝 Notas Importantes

### Formato de Fechas
- Todas las fechas siguen el formato **ISO 8601**: `YYYY-MM-DDTHH:mm:ss`
- Para parámetros de query: `YYYY-MM-DD`

### Paginación
- Parámetros estándar: `skip` y `limit`
- Límite máximo: 1000 registros por petición
- Default: 100 registros

### Rate Limiting
- No implementado actualmente
- Recomendado para producción: 100 requests/minuto por IP

### Logs
- Todas las operaciones importantes se registran
- Incluye: logins, creación/edición/eliminación de recursos

---

## 🎨 Patrones de Diseño Utilizados

| Patrón | Endpoint | Descripción |
|--------|----------|-------------|
| **Strategy** | `/air-quality/current` | Categorización de riesgo según niveles de AQI |
| **Builder** | `/air-quality/dashboard` | Construcción compleja de respuesta de dashboard |
| **Factory** | `/recommendations/current` | Generación de recomendaciones según tipo de usuario |
| **Prototype** | `/settings/dashboard` | Clonación de configuraciones por defecto |

---

## 📧 Soporte

Para cualquier duda o problema con la API, contacta al equipo de backend.

**Última actualización:** 27 de Noviembre, 2025  
**Versión:** 1.0.0

