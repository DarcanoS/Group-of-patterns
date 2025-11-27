/**
 * Ejemplo de integración del endpoint de histórico de 7 días
 * Este archivo muestra cómo consumir el endpoint desde un frontend React/TypeScript
 */

import { useState, useEffect } from 'react';
import { Line } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js';

// Registrar componentes de Chart.js
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

// ============================================================================
// TIPOS DE DATOS (basados en la respuesta del endpoint)
// ============================================================================

interface Station {
  id: number;
  name: string;
  city: string;
  country: string;
  latitude: number;
  longitude: number;
}

interface Pollutant {
  id: number;
  name: string;
  unit: string;
  description: string;
}

interface DataPoint {
  date: string;  // YYYY-MM-DD
  value: number;
  aqi: number;
}

interface PollutantHistoricalData {
  pollutant: Pollutant;
  data_points: DataPoint[];
}

interface HistoricalDataResponse {
  station: Station;
  start_date: string;
  end_date: string;
  pollutants_data: PollutantHistoricalData[];
}

// ============================================================================
// CONFIGURACIÓN DE COLORES PARA CONTAMINANTES
// ============================================================================

const POLLUTANT_COLORS: Record<string, string> = {
  'PM2.5': '#FF6384',    // Rosa/Rojo
  'PM10': '#36A2EB',     // Azul
  'O3': '#FFCE56',       // Amarillo
  'NO2': '#4BC0C0',      // Verde agua
  'SO2': '#9966FF',      // Morado
  'CO': '#FF9F40',       // Naranja
};

const getColorForPollutant = (pollutantName: string): string => {
  return POLLUTANT_COLORS[pollutantName] || '#CCCCCC';
};

// ============================================================================
// HOOK PERSONALIZADO PARA OBTENER DATOS
// ============================================================================

function useHistoricalData(stationId: number | null, endDate?: string) {
  const [data, setData] = useState<HistoricalDataResponse | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!stationId) {
      setData(null);
      return;
    }

    setLoading(true);
    setError(null);

    const params = new URLSearchParams({
      station_id: stationId.toString(),
      ...(endDate && { end_date: endDate })
    });

    fetch(`/api/v1/air-quality/historical/7-days?${params}`)
      .then(response => {
        if (!response.ok) {
          throw new Error(`Error: ${response.status}`);
        }
        return response.json();
      })
      .then(data => {
        setData(data);
        setLoading(false);
      })
      .catch(err => {
        setError(err.message);
        setLoading(false);
      });
  }, [stationId, endDate]);

  return { data, loading, error };
}

// ============================================================================
// COMPONENTE: GRÁFICO DE HISTÓRICO
// ============================================================================

interface HistoricalChartProps {
  stationId: number;
  endDate?: string;
}

export function HistoricalChart({ stationId, endDate }: HistoricalChartProps) {
  const { data, loading, error } = useHistoricalData(stationId, endDate);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-gray-500">Cargando datos históricos...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-red-500">Error: {error}</div>
      </div>
    );
  }

  if (!data || data.pollutants_data.length === 0) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-gray-500">No hay datos disponibles para esta estación</div>
      </div>
    );
  }

  // Preparar datos para el gráfico
  const labels = data.pollutants_data[0]?.data_points.map(dp =>
    new Date(dp.date).toLocaleDateString('es-ES', {
      month: 'short',
      day: 'numeric'
    })
  ) || [];

  const datasets = data.pollutants_data.map(pollutantData => ({
    label: `${pollutantData.pollutant.name} (${pollutantData.pollutant.unit})`,
    data: pollutantData.data_points.map(dp => dp.value),
    borderColor: getColorForPollutant(pollutantData.pollutant.name),
    backgroundColor: getColorForPollutant(pollutantData.pollutant.name) + '20', // Transparencia
    tension: 0.4, // Suavizar líneas
    pointRadius: 4,
    pointHoverRadius: 6,
  }));

  const chartData = {
    labels,
    datasets,
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'top' as const,
        labels: {
          usePointStyle: true,
          padding: 15,
        }
      },
      title: {
        display: true,
        text: `Histórico de Calidad del Aire - ${data.station.name}`,
        font: {
          size: 16,
          weight: 'bold' as const,
        }
      },
      tooltip: {
        mode: 'index' as const,
        intersect: false,
        callbacks: {
          label: function(context: any) {
            const label = context.dataset.label || '';
            const value = context.parsed.y;
            // Buscar el AQI correspondiente
            const pollutantData = data.pollutants_data[context.datasetIndex];
            const dataPoint = pollutantData.data_points[context.dataIndex];
            return `${label}: ${value.toFixed(2)} (AQI: ${dataPoint.aqi})`;
          }
        }
      }
    },
    scales: {
      x: {
        display: true,
        title: {
          display: true,
          text: 'Fecha'
        }
      },
      y: {
        display: true,
        title: {
          display: true,
          text: 'Valor'
        },
        beginAtZero: true,
      }
    },
    interaction: {
      mode: 'nearest' as const,
      axis: 'x' as const,
      intersect: false
    }
  };

  return (
    <div className="w-full bg-white rounded-lg shadow-lg p-6">
      {/* Header con información de la estación */}
      <div className="mb-4">
        <h3 className="text-xl font-semibold text-gray-800">
          {data.station.name}
        </h3>
        <p className="text-sm text-gray-600">
          {data.station.city}, {data.station.country}
        </p>
        <p className="text-xs text-gray-500 mt-1">
          Período: {new Date(data.start_date).toLocaleDateString('es-ES')} - {new Date(data.end_date).toLocaleDateString('es-ES')}
        </p>
      </div>

      {/* Gráfico */}
      <div className="h-96">
        <Line data={chartData} options={options} />
      </div>

      {/* Resumen de contaminantes */}
      <div className="mt-4 grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-2">
        {data.pollutants_data.map((pollutantData) => {
          const latestPoint = pollutantData.data_points[pollutantData.data_points.length - 1];
          return (
            <div
              key={pollutantData.pollutant.id}
              className="border rounded p-2 text-center"
              style={{ borderColor: getColorForPollutant(pollutantData.pollutant.name) }}
            >
              <div className="text-xs font-semibold text-gray-600">
                {pollutantData.pollutant.name}
              </div>
              <div className="text-lg font-bold" style={{ color: getColorForPollutant(pollutantData.pollutant.name) }}>
                {latestPoint?.value.toFixed(1)}
              </div>
              <div className="text-xs text-gray-500">
                {pollutantData.pollutant.unit}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}

// ============================================================================
// COMPONENTE: SELECTOR DE ESTACIÓN CON HISTÓRICO
// ============================================================================

interface StationWithHistoricalProps {
  city?: string;
}

export function StationWithHistorical({ city = 'Bogotá' }: StationWithHistoricalProps) {
  const [stations, setStations] = useState<Station[]>([]);
  const [selectedStation, setSelectedStation] = useState<number | null>(null);
  const [loading, setLoading] = useState(true);

  // Cargar estaciones al montar el componente
  useEffect(() => {
    fetch(`/api/v1/stations?city=${encodeURIComponent(city)}`)
      .then(res => res.json())
      .then(data => {
        setStations(data);
        if (data.length > 0) {
          setSelectedStation(data[0].id); // Seleccionar primera estación por defecto
        }
        setLoading(false);
      })
      .catch(err => {
        console.error('Error loading stations:', err);
        setLoading(false);
      });
  }, [city]);

  if (loading) {
    return <div>Cargando estaciones...</div>;
  }

  if (stations.length === 0) {
    return <div>No se encontraron estaciones en {city}</div>;
  }

  return (
    <div className="space-y-6">
      {/* Selector de Estación */}
      <div className="bg-white rounded-lg shadow p-4">
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Selecciona una estación:
        </label>
        <select
          value={selectedStation || ''}
          onChange={(e) => setSelectedStation(Number(e.target.value))}
          className="w-full md:w-auto px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        >
          {stations.map(station => (
            <option key={station.id} value={station.id}>
              {station.name} - {station.city}
            </option>
          ))}
        </select>
      </div>

      {/* Gráfico de Histórico */}
      {selectedStation && (
        <HistoricalChart stationId={selectedStation} />
      )}
    </div>
  );
}

// ============================================================================
// COMPONENTE: EJEMPLO DE USO COMPLETO
// ============================================================================

export default function HistoricalDataExample() {
  return (
    <div className="container mx-auto px-4 py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">
          Histórico de Calidad del Aire
        </h1>
        <p className="text-gray-600">
          Visualiza los últimos 7 días de datos de contaminantes para estaciones cercanas
        </p>
      </div>

      <StationWithHistorical city="Bogotá" />

      {/* Información adicional */}
      <div className="mt-8 bg-blue-50 border border-blue-200 rounded-lg p-4">
        <h3 className="text-sm font-semibold text-blue-800 mb-2">
          ℹ️ Sobre los datos
        </h3>
        <ul className="text-sm text-blue-700 space-y-1">
          <li>• Los valores mostrados son promedios diarios</li>
          <li>• El AQI (Índice de Calidad del Aire) se muestra en los tooltips</li>
          <li>• Los datos se actualizan diariamente</li>
          <li>• Puedes hacer hover sobre las líneas para ver valores exactos</li>
        </ul>
      </div>
    </div>
  );
}

// ============================================================================
// EJEMPLO DE USO SIMPLE
// ============================================================================

/*
import HistoricalDataExample from './components/HistoricalDataExample';

function App() {
  return (
    <div className="App">
      <HistoricalDataExample />
    </div>
  );
}
*/

// ============================================================================
// EJEMPLO DE USO CON ESTACIÓN ESPECÍFICA
// ============================================================================

/*
import { HistoricalChart } from './components/HistoricalDataExample';

function CustomDashboard() {
  return (
    <div>
      <h1>Mi Dashboard Personalizado</h1>
      <HistoricalChart stationId={1} />
    </div>
  );
}
*/

