# 🚀 Guía de Integración Rápida para Frontend

## 📦 Archivos de Integración

Hemos creado 3 archivos esenciales para facilitar la integración del frontend con el backend:

1. **`API_CONTRACT.md`** - Documentación completa de todos los endpoints
2. **`api-types.ts`** - Definiciones de tipos TypeScript
3. **`api-client-example.ts`** - Cliente API listo para usar

---

## ⚡ Quick Start

### 1. Copiar Archivos al Proyecto Frontend

```bash
# Copia los archivos TypeScript a tu proyecto frontend
cp api-types.ts /path/to/frontend/src/types/
cp api-client-example.ts /path/to/frontend/src/api/
```

### 2. Instalar Dependencias (si es necesario)

El cliente API usa `fetch` nativo, no requiere dependencias adicionales.

### 3. Configurar el Cliente API

```typescript
// src/api/index.ts
import { AirQualityAPI } from './api-client-example';

// Crear instancia del cliente
export const api = new AirQualityAPI('http://localhost:8000/api/v1');

// O usar variable de entorno
export const api = new AirQualityAPI(
  process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1'
);
```

### 4. Ejemplo de Uso en Componente React

```typescript
// Login.tsx
import React, { useState } from 'react';
import { api } from './api';

export function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const response = await api.auth.login(email, password);
      
      // Guardar token
      localStorage.setItem('token', response.access_token);
      api.setToken(response.access_token);
      
      // Guardar usuario
      localStorage.setItem('user', JSON.stringify(response.user));
      
      console.log('Login exitoso:', response.user);
      
      // Redirigir al dashboard
      window.location.href = '/dashboard';
    } catch (err: any) {
      setError(err.message || 'Error al iniciar sesión');
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleLogin}>
      <input
        type="email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        placeholder="Email"
        required
      />
      <input
        type="password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        placeholder="Password"
        required
      />
      {error && <p className="error">{error}</p>}
      <button type="submit" disabled={loading}>
        {loading ? 'Iniciando sesión...' : 'Iniciar Sesión'}
      </button>
    </form>
  );
}
```

### 5. Ejemplo de Dashboard

```typescript
// Dashboard.tsx
import React, { useEffect, useState } from 'react';
import { api } from './api';
import type { DashboardResponse } from './types/api-types';

export function Dashboard() {
  const [dashboard, setDashboard] = useState<DashboardResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const loadDashboard = async () => {
      try {
        // Cargar token del localStorage
        const token = localStorage.getItem('token');
        if (token) {
          api.setToken(token);
        }

        // Obtener datos del dashboard
        const data = await api.airQuality.getDashboard({ 
          city: 'New York' 
        });
        
        setDashboard(data);
      } catch (err: any) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    loadDashboard();
  }, []);

  if (loading) return <div>Cargando...</div>;
  if (error) return <div>Error: {error}</div>;
  if (!dashboard) return <div>No hay datos</div>;

  return (
    <div className="dashboard">
      <h1>{dashboard.station.city}</h1>
      
      <div className="aqi-card">
        <h2>AQI Promedio</h2>
        <div className="aqi-value" style={{ 
          backgroundColor: dashboard.risk_assessment.color 
        }}>
          {dashboard.daily_stats.avg_aqi}
        </div>
        <p>{dashboard.risk_assessment.level}</p>
      </div>

      <div className="readings">
        <h2>Lecturas Actuales</h2>
        {dashboard.current_readings.map((reading, index) => (
          <div key={index} className="reading-card">
            <h3>{reading.pollutant.name}</h3>
            <p>{reading.value} {reading.pollutant.unit}</p>
            <p>AQI: {reading.aqi}</p>
          </div>
        ))}
      </div>

      <div className="recommendations">
        <h2>Recomendaciones</h2>
        <ul>
          {dashboard.risk_assessment.recommended_actions.map((action, i) => (
            <li key={i}>{action}</li>
          ))}
        </ul>
      </div>
    </div>
  );
}
```

---

## 🔐 Manejo de Autenticación

### Configurar Interceptor de Token

```typescript
// src/api/auth-manager.ts
import { api } from './index';

export class AuthManager {
  static initialize() {
    // Cargar token al iniciar la app
    const token = localStorage.getItem('token');
    if (token) {
      api.setToken(token);
    }
  }

  static async login(email: string, password: string) {
    const response = await api.auth.login(email, password);
    
    // Guardar token y usuario
    localStorage.setItem('token', response.access_token);
    localStorage.setItem('user', JSON.stringify(response.user));
    
    // Configurar token en el cliente
    api.setToken(response.access_token);
    
    return response;
  }

  static logout() {
    // Limpiar storage
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    
    // Limpiar token del cliente
    api.clearToken();
    
    // Redirigir al login
    window.location.href = '/login';
  }

  static getCurrentUser() {
    const userStr = localStorage.getItem('user');
    return userStr ? JSON.parse(userStr) : null;
  }

  static isAuthenticated() {
    return !!localStorage.getItem('token');
  }

  static isAdmin() {
    const user = this.getCurrentUser();
    return user?.role?.name === 'Admin';
  }
}

// Inicializar al cargar la app
AuthManager.initialize();
```

### Usar en App.tsx

```typescript
// App.tsx
import { useEffect, useState } from 'react';
import { AuthManager } from './api/auth-manager';

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  useEffect(() => {
    setIsAuthenticated(AuthManager.isAuthenticated());
  }, []);

  return (
    <div className="App">
      {isAuthenticated ? <Dashboard /> : <Login />}
    </div>
  );
}
```

---

## 🎯 Ejemplos de Casos de Uso Comunes

### 1. Listar Estaciones con Filtro

```typescript
async function loadStations() {
  try {
    const stations = await api.stations.list({
      city: 'New York',
      limit: 20,
      skip: 0
    });
    
    console.log('Estaciones encontradas:', stations);
    return stations;
  } catch (error) {
    console.error('Error al cargar estaciones:', error);
  }
}
```

### 2. Obtener Lecturas Actuales de una Estación

```typescript
async function loadStationReadings(stationId: number) {
  try {
    const readings = await api.stations.getCurrentReadings(stationId);
    
    console.log('Lecturas:', readings.readings);
    console.log('Última actualización:', readings.last_updated);
    
    return readings;
  } catch (error) {
    console.error('Error al cargar lecturas:', error);
  }
}
```

### 3. Obtener Recomendación Personalizada

```typescript
async function getRecommendation(location: string) {
  try {
    const recommendation = await api.recommendations.getCurrent({ 
      location 
    });
    
    console.log('Consejos de salud:', recommendation.health_advice);
    console.log('Acciones recomendadas:', recommendation.actions);
    console.log('Productos:', recommendation.products);
    
    return recommendation;
  } catch (error) {
    console.error('Error al obtener recomendación:', error);
  }
}
```

### 4. Actualizar Preferencias de Usuario

```typescript
async function updateTheme(theme: 'light' | 'dark') {
  try {
    const preferences = await api.settings.updatePreferences({
      theme: theme
    });
    
    console.log('Preferencias actualizadas:', preferences);
    return preferences;
  } catch (error) {
    console.error('Error al actualizar preferencias:', error);
  }
}
```

### 5. Admin: Crear Nueva Estación

```typescript
async function createStation() {
  try {
    const newStation = await api.admin.createStation({
      name: 'Brooklyn Station',
      latitude: 40.6782,
      longitude: -73.9442,
      city: 'Brooklyn',
      country: 'USA',
      region_id: 1
    });
    
    console.log('Estación creada:', newStation);
    return newStation;
  } catch (error) {
    if (error.statusCode === 403) {
      console.error('No tienes permisos de administrador');
    } else {
      console.error('Error al crear estación:', error);
    }
  }
}
```

### 6. Generar Reporte

```typescript
async function generateReport() {
  try {
    const report = await api.reports.create({
      city: 'New York',
      start_date: '2025-11-01',
      end_date: '2025-11-27',
      station_id: 1,
      pollutant_id: 1
    });
    
    console.log('Reporte generado:', report);
    console.log('Descargar desde:', report.file_path);
    
    return report;
  } catch (error) {
    console.error('Error al generar reporte:', error);
  }
}
```

---

## 🎨 Integración con React Query (Opcional)

Si usas React Query para manejo de estado:

```typescript
// hooks/useAirQuality.ts
import { useQuery } from '@tanstack/react-query';
import { api } from '../api';

export function useCurrentAQI(city: string) {
  return useQuery({
    queryKey: ['aqi', city],
    queryFn: () => api.airQuality.getCurrentAQI(city),
    enabled: !!city,
    refetchInterval: 300000, // Refetch cada 5 minutos
  });
}

export function useDashboard(city?: string, stationId?: number) {
  return useQuery({
    queryKey: ['dashboard', city, stationId],
    queryFn: () => api.airQuality.getDashboard({ city, station_id: stationId }),
    enabled: !!(city || stationId),
    refetchInterval: 300000,
  });
}

export function useStations(filters?: { city?: string; country?: string }) {
  return useQuery({
    queryKey: ['stations', filters],
    queryFn: () => api.stations.list(filters),
  });
}

export function useRecommendation(location?: string, aqi?: number) {
  return useQuery({
    queryKey: ['recommendation', location, aqi],
    queryFn: () => api.recommendations.getCurrent({ location, aqi }),
    enabled: !!location || !!aqi,
  });
}
```

Uso en componente:

```typescript
function DashboardWithQuery() {
  const { data, isLoading, error } = useDashboard('New York');

  if (isLoading) return <div>Cargando...</div>;
  if (error) return <div>Error: {error.message}</div>;

  return <div>AQI: {data.daily_stats.avg_aqi}</div>;
}
```

---

## 🌐 Variables de Entorno

Crea un archivo `.env` en tu proyecto frontend:

```bash
# .env
REACT_APP_API_URL=http://localhost:8000/api/v1
VITE_API_URL=http://localhost:8000/api/v1  # Si usas Vite

# Producción
# REACT_APP_API_URL=https://api.airquality.com/api/v1
```

Usar en el código:

```typescript
const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1';
export const api = new AirQualityAPI(API_URL);
```

---

## 🔍 Debugging y Logs

Agregar logging al cliente:

```typescript
// api/logger.ts
export class APILogger {
  static log(method: string, endpoint: string, data?: any) {
    if (process.env.NODE_ENV === 'development') {
      console.log(`[API] ${method} ${endpoint}`, data);
    }
  }

  static error(method: string, endpoint: string, error: any) {
    console.error(`[API Error] ${method} ${endpoint}`, error);
  }
}
```

---

## 📱 Ejemplo Completo: App de Calidad del Aire

```typescript
// App.tsx - Aplicación completa
import React, { useEffect, useState } from 'react';
import { api } from './api';
import { AuthManager } from './api/auth-manager';

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [currentView, setCurrentView] = useState('dashboard');

  useEffect(() => {
    setIsAuthenticated(AuthManager.isAuthenticated());
  }, []);

  if (!isAuthenticated) {
    return <LoginPage onLogin={() => setIsAuthenticated(true)} />;
  }

  return (
    <div className="app">
      <Sidebar onNavigate={setCurrentView} />
      <main>
        {currentView === 'dashboard' && <Dashboard />}
        {currentView === 'stations' && <StationsList />}
        {currentView === 'recommendations' && <Recommendations />}
        {currentView === 'reports' && <Reports />}
        {currentView === 'settings' && <Settings />}
      </main>
    </div>
  );
}

function LoginPage({ onLogin }: { onLogin: () => void }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await AuthManager.login(email, password);
      onLogin();
    } catch (error) {
      alert('Error al iniciar sesión');
    }
  };

  return (
    <div className="login-page">
      <form onSubmit={handleLogin}>
        <h1>Air Quality Monitor</h1>
        <input
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="Email"
        />
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="Password"
        />
        <button type="submit">Login</button>
      </form>
    </div>
  );
}

export default App;
```

---

## 🚨 Manejo de Errores

```typescript
import { APIError } from './api/api-client-example';

async function handleAPICall() {
  try {
    const data = await api.airQuality.getCurrentAQI('New York');
    return data;
  } catch (error) {
    if (error instanceof APIError) {
      switch (error.statusCode) {
        case 401:
          // Token expirado, redirigir al login
          AuthManager.logout();
          break;
        case 403:
          alert('No tienes permisos para esta acción');
          break;
        case 404:
          alert('Recurso no encontrado');
          break;
        case 422:
          alert('Datos de entrada inválidos');
          break;
        default:
          alert(`Error: ${error.message}`);
      }
    } else {
      alert('Error de red o servidor no disponible');
    }
  }
}
```

---

## ✅ Checklist de Integración

- [ ] Copiar `api-types.ts` al proyecto
- [ ] Copiar `api-client-example.ts` al proyecto
- [ ] Configurar variable de entorno `API_URL`
- [ ] Crear `AuthManager` para manejo de autenticación
- [ ] Implementar página de Login
- [ ] Implementar Dashboard principal
- [ ] Probar endpoints públicos (stations, air-quality)
- [ ] Probar endpoints autenticados (recommendations, settings)
- [ ] Probar endpoints de admin (si aplica)
- [ ] Implementar manejo de errores
- [ ] Agregar loading states
- [ ] Agregar validación de formularios

---

## 📚 Recursos Adicionales

- **Documentación completa**: Ver `API_CONTRACT.md`
- **Tipos TypeScript**: Ver `api-types.ts`
- **Cliente API**: Ver `api-client-example.ts`

---

## 🆘 Soporte

Si encuentras problemas durante la integración, verifica:

1. ✅ El backend está corriendo en `http://localhost:8000`
2. ✅ CORS está habilitado en el backend
3. ✅ El token de autenticación es válido
4. ✅ Los datos enviados cumplen con los esquemas de validación

**¡Feliz codificación! 🎉**

