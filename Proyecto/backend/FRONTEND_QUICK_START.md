# 🚀 Guía Rápida para Integración Frontend - Histórico 7 Días

## Para el Desarrollador Frontend

¡Hola! 👋 Este endpoint está listo para usar. Aquí tienes todo lo que necesitas saber:

---

## 📍 URL del Endpoint

```
GET http://localhost:8000/api/v1/air-quality/historical/7-days
```

🟢 **No requiere autenticación** - Puedes llamarlo directamente

---

## 🎯 Parámetros

### Requeridos
- **station_id** (número): ID de la estación que quieres consultar

### Opcionales
- **end_date** (fecha): Fecha final en formato YYYY-MM-DD (default: hoy)

---

## 💡 Ejemplos de Uso

### JavaScript/TypeScript (Fetch)

```typescript
// Ejemplo 1: Últimos 7 días (hasta hoy)
const response = await fetch(
  'http://localhost:8000/api/v1/air-quality/historical/7-days?station_id=1'
);
const data = await response.json();

// Ejemplo 2: Con fecha específica
const response = await fetch(
  'http://localhost:8000/api/v1/air-quality/historical/7-days?station_id=1&end_date=2025-11-27'
);
const data = await response.json();
```

### Axios

```typescript
import axios from 'axios';

const getData = async (stationId: number) => {
  const response = await axios.get('/api/v1/air-quality/historical/7-days', {
    params: { station_id: stationId }
  });
  return response.data;
};
```

### React Query

```typescript
import { useQuery } from '@tanstack/react-query';

function useHistoricalData(stationId: number) {
  return useQuery({
    queryKey: ['historical', stationId],
    queryFn: async () => {
      const response = await fetch(
        `/api/v1/air-quality/historical/7-days?station_id=${stationId}`
      );
      if (!response.ok) throw new Error('Error al cargar datos');
      return response.json();
    },
    enabled: !!stationId,
  });
}

// Uso en componente
function MyComponent() {
  const { data, isLoading, error } = useHistoricalData(1);
  
  if (isLoading) return <div>Cargando...</div>;
  if (error) return <div>Error: {error.message}</div>;
  
  return <Chart data={data} />;
}
```

---

## 📊 Estructura de la Respuesta

```typescript
interface Response {
  station: {
    id: number;
    name: string;
    city: string;
    country: string;
    latitude: number;
    longitude: number;
  };
  start_date: string;  // "2025-11-21"
  end_date: string;    // "2025-11-27"
  pollutants_data: Array<{
    pollutant: {
      id: number;
      name: string;      // "PM2.5", "PM10", "O3", etc.
      unit: string;      // "µg/m³", "ppm"
      description: string;
    };
    data_points: Array<{
      date: string;      // "2025-11-21"
      value: number;     // 32.5
      aqi: number;       // 95
    }>;
  }>;
}
```

---

## 🎨 Ejemplo de Visualización

### Chart.js

```typescript
import { Line } from 'react-chartjs-2';

function HistoricalChart({ stationId }) {
  const [data, setData] = useState(null);

  useEffect(() => {
    fetch(`/api/v1/air-quality/historical/7-days?station_id=${stationId}`)
      .then(res => res.json())
      .then(setData);
  }, [stationId]);

  if (!data) return <div>Loading...</div>;

  const chartData = {
    labels: data.pollutants_data[0].data_points.map(dp => dp.date),
    datasets: data.pollutants_data.map(pd => ({
      label: `${pd.pollutant.name} (${pd.pollutant.unit})`,
      data: pd.data_points.map(dp => dp.value),
      borderColor: getColor(pd.pollutant.name),
    }))
  };

  return <Line data={chartData} />;
}
```

### Recharts

```typescript
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts';

function HistoricalChart({ stationId }) {
  const [data, setData] = useState(null);

  useEffect(() => {
    fetch(`/api/v1/air-quality/historical/7-days?station_id=${stationId}`)
      .then(res => res.json())
      .then(setData);
  }, [stationId]);

  if (!data) return <div>Loading...</div>;

  // Transformar datos para Recharts
  const chartData = data.pollutants_data[0].data_points.map((_, index) => {
    const point: any = { date: data.pollutants_data[0].data_points[index].date };
    data.pollutants_data.forEach(pd => {
      point[pd.pollutant.name] = pd.data_points[index].value;
    });
    return point;
  });

  return (
    <LineChart width={800} height={400} data={chartData}>
      <CartesianGrid strokeDasharray="3 3" />
      <XAxis dataKey="date" />
      <YAxis />
      <Tooltip />
      <Legend />
      {data.pollutants_data.map(pd => (
        <Line 
          key={pd.pollutant.id}
          type="monotone" 
          dataKey={pd.pollutant.name}
          stroke={getColor(pd.pollutant.name)}
        />
      ))}
    </LineChart>
  );
}
```

---

## 🎨 Colores Recomendados para Contaminantes

```typescript
const POLLUTANT_COLORS = {
  'PM2.5': '#FF6384',  // Rosa/Rojo
  'PM10': '#36A2EB',   // Azul
  'O3': '#FFCE56',     // Amarillo
  'NO2': '#4BC0C0',    // Verde agua
  'SO2': '#9966FF',    // Morado
  'CO': '#FF9F40',     // Naranja
};

function getColor(pollutantName: string): string {
  return POLLUTANT_COLORS[pollutantName] || '#CCCCCC';
}
```

---

## 🔄 Flujo Completo Recomendado

### 1. Obtener Lista de Estaciones

```typescript
// Primero, obtén las estaciones disponibles
const stations = await fetch('/api/v1/stations?city=Bogotá').then(r => r.json());

// Muestra un selector
<select onChange={(e) => setSelectedStation(e.target.value)}>
  {stations.map(s => (
    <option key={s.id} value={s.id}>{s.name}</option>
  ))}
</select>
```

### 2. Cargar Histórico de la Estación Seleccionada

```typescript
useEffect(() => {
  if (selectedStation) {
    fetch(`/api/v1/air-quality/historical/7-days?station_id=${selectedStation}`)
      .then(res => res.json())
      .then(data => setHistoricalData(data));
  }
}, [selectedStation]);
```

### 3. Mostrar Gráfico

```typescript
{historicalData && (
  <Chart data={historicalData} />
)}
```

---

## ⚠️ Manejo de Errores

```typescript
try {
  const response = await fetch(
    `/api/v1/air-quality/historical/7-days?station_id=${stationId}`
  );
  
  if (!response.ok) {
    if (response.status === 404) {
      alert('Estación no encontrada');
    } else {
      alert('Error al cargar datos');
    }
    return;
  }
  
  const data = await response.json();
  setHistoricalData(data);
} catch (error) {
  console.error('Error:', error);
  alert('Error de conexión');
}
```

---

## 🧪 Testing Local

### Probar el Endpoint Manualmente

```bash
# En tu navegador o Postman
http://localhost:8000/api/v1/air-quality/historical/7-days?station_id=1
```

### Verificar que el Backend Esté Corriendo

```bash
curl http://localhost:8000/api/v1/admin/health
# Debe responder: {"status":"healthy","database":"connected",...}
```

---

## 📱 Ejemplo Completo React + TypeScript

Ver archivo: `frontend-example-historical.tsx`

Incluye:
- ✅ Hook personalizado para cargar datos
- ✅ Componente de gráfico con Chart.js
- ✅ Selector de estación
- ✅ Manejo de loading y errores
- ✅ Estilos con Tailwind CSS
- ✅ TypeScript completo

---

## 💻 Instalación de Dependencias

### Chart.js

```bash
npm install react-chartjs-2 chart.js
```

### Recharts

```bash
npm install recharts
```

### React Query (opcional, pero recomendado)

```bash
npm install @tanstack/react-query
```

---

## 🎯 Checklist de Integración

- [ ] Instalar dependencias de gráficos
- [ ] Crear servicio/API para llamar al endpoint
- [ ] Crear componente de gráfico
- [ ] Agregar selector de estación
- [ ] Implementar manejo de errores
- [ ] Probar con diferentes estaciones
- [ ] Agregar loading states
- [ ] Estilizar según diseño
- [ ] Probar responsive
- [ ] Optimizar performance (usar React Query o similar)

---

## 🚦 Estados de la UI Recomendados

```typescript
{loading && (
  <div className="flex justify-center items-center h-64">
    <Spinner />
    <span>Cargando datos históricos...</span>
  </div>
)}

{error && (
  <div className="bg-red-50 border border-red-200 rounded p-4">
    <p className="text-red-800">Error: {error}</p>
  </div>
)}

{!data?.pollutants_data.length && (
  <div className="text-center text-gray-500 py-8">
    No hay datos disponibles para esta estación
  </div>
)}

{data && <Chart data={data} />}
```

---

## 🔗 Recursos Adicionales

- **Documentación completa**: `HISTORICAL_ENDPOINT_README.md`
- **Ejemplo TypeScript**: `frontend-example-historical.tsx`
- **API Contract**: `API_CONTRACT.md` (sección 3.4)
- **Backend Code**: `app/api/v1/endpoints/air_quality.py`

---

## 💬 ¿Preguntas?

Si tienes alguna duda sobre la integración:

1. Revisa `HISTORICAL_ENDPOINT_README.md` para más detalles
2. Mira el ejemplo completo en `frontend-example-historical.tsx`
3. Prueba el endpoint manualmente con curl o Postman
4. Contacta al equipo de backend

---

## ✅ El endpoint está listo para usar

**Status**: 🟢 Funcionando  
**Versión**: 1.0.0  
**Última actualización**: 27 de Noviembre, 2025

¡Feliz codificación! 🎉

