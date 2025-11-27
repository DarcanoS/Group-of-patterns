# 📊 Endpoint de Histórico de 7 Días

## Descripción General

Este endpoint permite obtener datos históricos de calidad del aire de los últimos 7 días para una estación específica, incluyendo **todos los tipos de contaminantes** en un mismo rango de fechas. Esto facilita la visualización comparativa de múltiples contaminantes en un solo gráfico.

---

## 🎯 Endpoint

```
GET /api/v1/air-quality/historical/7-days
```

### Nivel de Acceso
🟢 **Público** - No requiere autenticación

---

## 📥 Parámetros

### Query Parameters

| Parámetro | Tipo | Requerido | Default | Descripción |
|-----------|------|-----------|---------|-------------|
| `station_id` | `int` | ✅ Sí | - | ID de la estación de monitoreo |
| `end_date` | `date` | ❌ No | Hoy | Fecha final del rango (formato: YYYY-MM-DD) |

### Ejemplos de URL

```bash
# Últimos 7 días hasta hoy
/api/v1/air-quality/historical/7-days?station_id=1

# 7 días hasta una fecha específica
/api/v1/air-quality/historical/7-days?station_id=1&end_date=2025-11-27
```

---

## 📤 Respuesta

### Estructura de la Respuesta (200 OK)

```typescript
interface HistoricalDataResponse {
  station: {
    id: number;
    name: string;
    city: string;
    country: string;
    latitude: number;
    longitude: number;
  };
  start_date: string;  // YYYY-MM-DD
  end_date: string;    // YYYY-MM-DD
  pollutants_data: PollutantHistoricalData[];
}

interface PollutantHistoricalData {
  pollutant: {
    id: number;
    name: string;        // "PM2.5", "PM10", "O3", etc.
    unit: string;        // "µg/m³", "ppm", etc.
    description: string;
  };
  data_points: DataPoint[];
}

interface DataPoint {
  date: string;   // YYYY-MM-DD
  value: number;  // Valor promedio diario
  aqi: number;    // AQI promedio diario
}
```

### Ejemplo de Respuesta

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
  "start_date": "2025-11-20",
  "end_date": "2025-11-27",
  "pollutants_data": [
    {
      "pollutant": {
        "id": 1,
        "name": "PM2.5",
        "unit": "µg/m³",
        "description": "Fine particulate matter"
      },
      "data_points": [
        {"date": "2025-11-20", "value": 32.5, "aqi": 95},
        {"date": "2025-11-21", "value": 35.8, "aqi": 101},
        {"date": "2025-11-22", "value": 28.3, "aqi": 85},
        {"date": "2025-11-23", "value": 41.2, "aqi": 115},
        {"date": "2025-11-24", "value": 38.7, "aqi": 108},
        {"date": "2025-11-25", "value": 33.9, "aqi": 97},
        {"date": "2025-11-26", "value": 36.4, "aqi": 103}
      ]
    },
    {
      "pollutant": {
        "id": 2,
        "name": "PM10",
        "unit": "µg/m³",
        "description": "Particulate matter"
      },
      "data_points": [
        {"date": "2025-11-20", "value": 52.1, "aqi": 72},
        {"date": "2025-11-21", "value": 58.4, "aqi": 78},
        {"date": "2025-11-22", "value": 48.9, "aqi": 68},
        {"date": "2025-11-23", "value": 65.2, "aqi": 85},
        {"date": "2025-11-24", "value": 61.7, "aqi": 82},
        {"date": "2025-11-25", "value": 54.3, "aqi": 74},
        {"date": "2025-11-26", "value": 59.8, "aqi": 80}
      ]
    }
  ]
}
```

---

## ⚠️ Códigos de Error

| Código | Descripción | Detalle |
|--------|-------------|---------|
| `404` | Not Found | La estación con el ID especificado no existe |
| `422` | Validation Error | Parámetros inválidos (ej: `station_id` no numérico) |

### Ejemplo de Error

```json
{
  "detail": "Station with ID 99999 not found"
}
```

---

## 💡 Casos de Uso

### 1. Dashboard con Gráfico Comparativo

Mostrar múltiples contaminantes en un mismo gráfico de líneas:

```javascript
// Fetch data
const response = await fetch('/api/v1/air-quality/historical/7-days?station_id=1');
const data = await response.json();

// Preparar datos para Chart.js
const labels = data.pollutants_data[0].data_points.map(dp => dp.date);
const datasets = data.pollutants_data.map(pd => ({
  label: `${pd.pollutant.name} (${pd.pollutant.unit})`,
  data: pd.data_points.map(dp => dp.value),
  borderColor: getColorForPollutant(pd.pollutant.name),
  fill: false
}));

// Renderizar gráfico
new Chart(ctx, {
  type: 'line',
  data: { labels, datasets },
  options: { responsive: true }
});
```

### 2. Selección de Estación Cercana

Combinar con el endpoint de estaciones para permitir al usuario seleccionar:

```javascript
// 1. Obtener estaciones cercanas
const nearbyStations = await fetch('/api/v1/stations?city=New York');

// 2. Cuando el usuario selecciona una estación
const selectedStationId = stations[0].id;

// 3. Obtener histórico de esa estación
const historicalData = await fetch(
  `/api/v1/air-quality/historical/7-days?station_id=${selectedStationId}`
);
```

### 3. Análisis de Tendencias

Identificar patrones y tendencias en la calidad del aire:

```javascript
const response = await fetch('/api/v1/air-quality/historical/7-days?station_id=1');
const data = await response.json();

// Calcular tendencia para PM2.5
const pm25Data = data.pollutants_data.find(p => p.pollutant.name === 'PM2.5');
const values = pm25Data.data_points.map(dp => dp.value);
const trend = calculateTrend(values); // Función personalizada

if (trend > 0) {
  console.log('⚠️ La calidad del aire está empeorando');
} else {
  console.log('✅ La calidad del aire está mejorando');
}
```

---

## 🔧 Implementación Técnica

### Arquitectura

El endpoint sigue el patrón de arquitectura en capas:

```
Controller (Endpoint)
    ↓
Service (Business Logic)
    ↓
Repository (Database Access)
    ↓
Database (PostgreSQL)
```

### Flujo de Datos

1. **Request**: Cliente solicita datos con `station_id` y opcionalmente `end_date`
2. **Validación**: FastAPI valida los parámetros
3. **Cálculo de Fechas**: Si no hay `end_date`, se usa la fecha actual; se calcula `start_date` (7 días antes)
4. **Consulta DB**: Se consulta la tabla `air_quality_daily_stats` con filtros
5. **Organización**: Los datos se agrupan por contaminante
6. **Respuesta**: Se devuelve JSON estructurado

### Consulta SQL Subyacente

```sql
SELECT 
    aqs.*,
    p.id as pollutant_id,
    p.name as pollutant_name,
    p.unit as pollutant_unit
FROM air_quality_daily_stats aqs
JOIN pollutant p ON aqs.pollutant_id = p.id
WHERE 
    aqs.station_id = :station_id
    AND aqs.date >= :start_date
    AND aqs.date <= :end_date
ORDER BY aqs.date ASC;
```

---

## 📊 Datos Utilizados

El endpoint utiliza la tabla `air_quality_daily_stats`, que contiene:

- **Promedios diarios** calculados a partir de múltiples lecturas
- **AQI promedio, mínimo y máximo** del día
- **Conteo de lecturas** utilizadas en el cálculo

Esto garantiza:
- ✅ Respuestas rápidas (datos pre-agregados)
- ✅ Consistencia en los valores
- ✅ Reducción de carga en la base de datos

---

## 🧪 Testing

### Prueba Manual

```bash
# Asegúrate de que el backend esté corriendo
cd /path/to/backend
python test_historical_endpoint.py
```

### Prueba con cURL

```bash
# Test básico
curl "http://localhost:8000/api/v1/air-quality/historical/7-days?station_id=1"

# Test con fecha específica
curl "http://localhost:8000/api/v1/air-quality/historical/7-days?station_id=1&end_date=2025-11-27"

# Test con estación inválida (debe retornar 404)
curl "http://localhost:8000/api/v1/air-quality/historical/7-days?station_id=99999"
```

### Prueba con Postman

1. Crear nueva request GET
2. URL: `http://localhost:8000/api/v1/air-quality/historical/7-days`
3. Params:
   - `station_id`: 1
   - `end_date`: 2025-11-27 (opcional)
4. Send

---

## 📱 Integración con Frontend

### React Example

```typescript
import { useState, useEffect } from 'react';
import { Line } from 'react-chartjs-2';

interface HistoricalData {
  station: Station;
  start_date: string;
  end_date: string;
  pollutants_data: PollutantData[];
}

function HistoricalChart({ stationId }: { stationId: number }) {
  const [data, setData] = useState<HistoricalData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(`/api/v1/air-quality/historical/7-days?station_id=${stationId}`)
      .then(res => res.json())
      .then(data => {
        setData(data);
        setLoading(false);
      });
  }, [stationId]);

  if (loading) return <div>Loading...</div>;
  if (!data) return <div>No data available</div>;

  const chartData = {
    labels: data.pollutants_data[0]?.data_points.map(dp => dp.date) || [],
    datasets: data.pollutants_data.map(pd => ({
      label: `${pd.pollutant.name} (${pd.pollutant.unit})`,
      data: pd.data_points.map(dp => dp.value),
      borderColor: getPollutantColor(pd.pollutant.name),
      backgroundColor: getPollutantColor(pd.pollutant.name, 0.1),
    }))
  };

  return (
    <div>
      <h2>{data.station.name} - 7 Day History</h2>
      <p>{data.start_date} to {data.end_date}</p>
      <Line data={chartData} />
    </div>
  );
}
```

---

## 🎨 Recomendaciones de UI/UX

### Visualización

1. **Gráfico de Líneas**: Múltiples series para comparar contaminantes
2. **Colores Distintivos**: Usar colores diferentes para cada contaminante
3. **Leyenda Clara**: Incluir nombre y unidad de medida
4. **Tooltips**: Mostrar valores exactos al pasar el mouse
5. **Zoom**: Permitir hacer zoom en períodos específicos

### Interactividad

1. **Selector de Estación**: Dropdown o mapa para seleccionar estación
2. **Toggle de Contaminantes**: Permitir ocultar/mostrar contaminantes
3. **Selector de Rango**: Opción para cambiar el rango de fechas
4. **Export**: Botón para exportar datos en CSV/Excel

---

## 🔍 Consideraciones

### Performance

- ✅ Usa datos pre-agregados (daily_stats)
- ✅ Consulta limitada a 7 días
- ✅ Índices en `station_id` y `date`
- ⚡ Tiempo de respuesta típico: < 100ms

### Limitaciones

- Solo muestra promedios diarios (no datos por hora)
- Requiere que existan datos en `air_quality_daily_stats`
- No incluye datos históricos más allá de lo almacenado en DB

### Mejoras Futuras

- [ ] Agregar parámetro para rangos personalizados (no solo 7 días)
- [ ] Incluir datos horarios cuando sea necesario
- [ ] Agregar cálculo de tendencias en el backend
- [ ] Implementar cache para estaciones populares
- [ ] Agregar predicciones basadas en histórico

---

## 📚 Referencias

- **API Contract**: Ver `API_CONTRACT.md` sección 3.4
- **Testing Guide**: Ver `test_historical_endpoint.py`
- **Models**: Ver `app/models/daily_stats.py`
- **Schemas**: Ver `app/schemas/air_quality.py`

---

## 👥 Contacto

Para preguntas o reportar problemas con este endpoint, contacta al equipo de backend.

**Creado:** 27 de Noviembre, 2025  
**Versión:** 1.0.0

