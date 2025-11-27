<template>
  <div class="dashboard">
    <h1>tablero ciudadano</h1>
    <p class="subtitle">Calidad del aire actual {{ data?.city }}</p>

    <div v-if="loading" class="loading">cargando datos...</div>
    <div v-if="error" class="error">{{ error }}</div>

    <div v-if="data" class="dashboard-layout">

      <!-- TOP ROW: AQI + STATUS -->
      <div class="top-row">
        <!-- AQI CARD -->
        <div class="card aqi-card">
          <h2>Air Quality Index</h2>
          <p class="aqi" :class="aqiColor">{{ data.aqi }}</p>
          <span class="level">{{ data.level }}</span>
          <p v-if="data.primaryPollutant" class="pollutant">
            Contaminante principal: <strong>{{ data.primaryPollutant }}</strong>
          </p>
          <small>ultima actualizacion: {{ data.updatedAt }}</small>
        </div>

        <!-- STATUS CARD -->
        <div class="card">
          <h2>Estado de Salud</h2>
          <p class="status-level" :class="aqiColor">{{ data.riskCategory.level }}</p>
          <p class="health-implications">{{ data.riskCategory.health_implications }}</p>
          <p class="cautionary-statement">{{ data.riskCategory.cautionary_statement }}</p>
        </div>
      </div>

      <!-- NEARBY STATIONS (FULL WIDTH) -->
      <div class="card stations-card">
        <h2>Nearby Stations</h2>
        <div v-if="!data.stations || data.stations.length === 0" class="no-data">
          No stations available
        </div>
        <div v-else class="stations-list">
          <div v-for="station in data.stations" :key="station.id" class="station-item">
            <div class="station-header">
              <div>
                <h3 class="station-name">{{ station.name }}</h3>
                <p class="station-location">📍 {{ station.city }}, {{ station.country }}</p>
                <p class="station-updated" v-if="station.readings.length > 0">
                  🕒 {{ formatDateTime(station.readings[0].datetime) }}
                </p>
              </div>
              <div class="station-aqi" :class="getStationAqiColor(station.maxAqi)">
                {{ station.maxAqi }}
              </div>
            </div>
            <div class="pollutants-grid">
              <div
                v-for="reading in station.readings.slice(0, 6)"
                :key="reading.pollutant.name"
                class="pollutant-badge"
              >
                <span class="pollutant-name">{{ reading.pollutant.name }}</span>
                <span class="pollutant-value">
                  {{ reading.value }} <small>{{ reading.pollutant.unit }}</small>
                </span>
                <span
                  v-if="reading.aqi !== null"
                  class="pollutant-aqi"
                  :class="getPollutantAqiColor(reading.aqi)"
                >
                  AQI {{ reading.aqi }}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- HISTORICAL CHARTS (FULL WIDTH) -->
      <div class="card chart-card">
        <div class="chart-header">
          <h2>Histórico de 7 días</h2>
          <div class="station-selector">
            <label for="station-select">Estación:</label>
            <select 
              id="station-select" 
              v-model="selectedStationId" 
              @change="loadHistoricalData"
              :disabled="loadingHistory || availableStations.length === 0"
            >
              <option value="" disabled>Selecciona una estación</option>
              <option 
                v-for="station in availableStations" 
                :key="station.id" 
                :value="station.id"
              >
                {{ station.name }} - {{ station.city }}
              </option>
            </select>
          </div>
        </div>
        <div v-if="loadingHistory" class="loading-chart">Cargando datos históricos...</div>
        <div v-else-if="historicalError" class="error-chart">{{ historicalError }}</div>
        <div v-else-if="!selectedStationId" class="no-selection">Selecciona una estación para ver el histórico</div>
        <div v-show="selectedStationId && !loadingHistory && !historicalError" class="charts-grid">
          <div 
            v-for="(pollutantData, index) in pollutantsChartData" 
            :key="pollutantData.pollutant.id"
            class="mini-chart-container"
          >
            <h3 class="pollutant-chart-title">
              {{ pollutantData.pollutant.name }}
              <span class="pollutant-unit">({{ pollutantData.pollutant.unit }})</span>
            </h3>
            <canvas :ref="el => setPollutantChartRef(el, index)"></canvas>
          </div>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, nextTick, watch } from "vue";
import Chart from "chart.js/auto";
import { getAirQuality, getStations, getHistoricalData } from "../services/api";

const loading = ref(true);
const error = ref(null);
const data = ref(null);

// Variables para el histórico
const availableStations = ref([]);
const selectedStationId = ref("");
const historicalData = ref(null);
const loadingHistory = ref(false);
const historicalError = ref(null);
const pollutantsChartData = ref([]);
const pollutantChartRefs = ref([]);
const pollutantChartInstances = ref([]);

// Función para asignar refs de los canvas de contaminantes
const setPollutantChartRef = (el, index) => {
  if (el) {
    pollutantChartRefs.value[index] = el;
  }
};

onMounted(async () => {
  try {
    // Cargar datos de calidad del aire
    data.value = await getAirQuality();
    
    // Cargar todas las estaciones disponibles
    availableStations.value = await getStations('Bogotá', null, 0, 50);
    
    // Seleccionar la primera estación por defecto si hay estaciones disponibles
    if (availableStations.value.length > 0) {
      selectedStationId.value = availableStations.value[0].id;
      await loadHistoricalData();
    }

  } catch (err) {
    error.value = "Unable to connect to air quality service.";
    console.error(err);
  } finally {
    loading.value = false;
  }
});

const aqiColor = computed(() => {
  if (!data.value) return "";
  if (data.value.aqi <= 50) return "good";
  if (data.value.aqi <= 100) return "moderate";
  if (data.value.aqi <= 150) return "unhealthy";
  return "danger";
});

const recommendation = computed(() => {
  if (!data.value) return "";
  const aqi = data.value.aqi;
  if (aqi <= 50) return "Air quality is excellent. Ideal for outdoor activities.";
  if (aqi <= 100) return "Moderate air quality. Sensitive people should limit prolonged exertion.";
  if (aqi <= 150) return "Unhealthy for sensitive groups. Reduce outdoor activity.";
  return "Hazardous air quality. Stay indoors.";
});

const getStationAqiColor = (aqi) => {
  if (aqi <= 50) return "aqi-good";
  if (aqi <= 100) return "aqi-moderate";
  if (aqi <= 150) return "aqi-unhealthy";
  return "aqi-danger";
};

const getPollutantAqiColor = (aqi) => {
  if (aqi <= 50) return "aqi-good";
  if (aqi <= 100) return "aqi-moderate";
  if (aqi <= 150) return "aqi-unhealthy";
  return "aqi-danger";
};

const formatDateTime = (datetime) => {
  if (!datetime) return "";
  const date = new Date(datetime);
  return date.toLocaleString('es-ES', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    hour12: false
  });
};

// Función para cargar datos históricos
const loadHistoricalData = async () => {
  if (!selectedStationId.value) return;
  
  loadingHistory.value = true;
  historicalError.value = null;
  
  try {
    console.log('🔍 Loading historical data for station:', selectedStationId.value);
    historicalData.value = await getHistoricalData(selectedStationId.value);
    console.log('📊 Historical data received:', historicalData.value);
    
    pollutantsChartData.value = historicalData.value?.pollutants_data || [];
    console.log('📈 Pollutants chart data:', pollutantsChartData.value);
    
    await nextTick();
    renderCharts();
  } catch (err) {
    historicalError.value = "No se pudieron cargar los datos históricos.";
    console.error("❌ Error loading historical data:", err);
  } finally {
    loadingHistory.value = false;
  }
};

// Función para renderizar los gráficos individuales
const renderCharts = () => {
  console.log('🎨 Rendering individual pollutant charts...');
  
  if (pollutantsChartData.value.length === 0) {
    console.log('⚠️ No pollutants data available');
    historicalError.value = "No hay datos disponibles para esta estación en los últimos 7 días.";
    return;
  }
  
  // Destruir gráficos anteriores si existen
  pollutantChartInstances.value.forEach(chart => {
    if (chart) chart.destroy();
  });
  pollutantChartInstances.value = [];
  
  // Colores para cada contaminante
  const pollutantColors = {
    'PM2.5': '#e74c3c',
    'PM10': '#e67e22',
    'O3': '#3498db',
    'NO2': '#9b59b6',
    'SO2': '#f1c40f',
    'CO': '#2ecc71'
  };
  
  // Crear un gráfico para cada contaminante
  pollutantsChartData.value.forEach((pollutantData, index) => {
    const canvas = pollutantChartRefs.value[index];
    if (!canvas) {
      console.log(`⚠️ Canvas not found for ${pollutantData.pollutant.name}`);
      return;
    }
    
    // Preparar datos
    const labels = pollutantData.data_points.map(d => {
      const date = new Date(d.date);
      return date.toLocaleDateString('es-ES', { month: 'short', day: 'numeric' });
    });
    
    const values = pollutantData.data_points.map(d => d.value);
    
    const color = pollutantColors[pollutantData.pollutant.name] || '#94a3b8';
    
    console.log(`📊 Creating chart for ${pollutantData.pollutant.name}:`, { labels, values });
    
    // Crear gráfico
    const chartInstance = new Chart(canvas, {
      type: 'line',
      data: {
        labels: labels,
        datasets: [{
          label: pollutantData.pollutant.unit,
          data: values,
          borderColor: color,
          backgroundColor: color + '20',
          fill: true,
          tension: 0.4,
          pointRadius: 4,
          pointHoverRadius: 6,
          pointBackgroundColor: color,
          pointBorderColor: '#fff',
          pointBorderWidth: 2
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            display: false
          },
          tooltip: {
            backgroundColor: 'rgba(30, 41, 59, 0.95)',
            titleColor: '#f1f5f9',
            bodyColor: '#cbd5e1',
            borderColor: 'rgba(148, 163, 184, 0.3)',
            borderWidth: 1,
            padding: 10,
            displayColors: false,
            callbacks: {
              label: function(context) {
                return `${context.parsed.y} ${pollutantData.pollutant.unit}`;
              }
            }
          }
        },
        scales: {
          x: {
            grid: {
              color: 'rgba(148, 163, 184, 0.1)',
              drawBorder: false
            },
            ticks: {
              color: '#94a3b8',
              font: {
                size: 10
              }
            }
          },
          y: {
            beginAtZero: true,
            grid: {
              color: 'rgba(148, 163, 184, 0.1)',
              drawBorder: false
            },
            ticks: {
              color: '#94a3b8',
              font: {
                size: 10
              }
            }
          }
        }
      }
    });
    
    pollutantChartInstances.value.push(chartInstance);
  });
  
  console.log(`✅ Created ${pollutantChartInstances.value.length} charts`);
};
</script>

<style scoped>
.dashboard {
  padding: 1.5rem;
  color: white;
  background: #0f172a;
  min-height: 100vh;
  max-width: 100vw;
  overflow-x: hidden;
  box-sizing: border-box;
}

.dashboard h1 {
  margin: 0 0 0.5rem 0;
  font-size: clamp(1.5rem, 4vw, 2rem);
}

.subtitle {
  opacity: 0.7;
  margin-bottom: 1.5rem;
  font-size: clamp(0.875rem, 2vw, 1rem);
}

.loading {
  color: #ccc;
}

.error {
  color: red;
}

.dashboard-layout {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
  max-width: 100%;
}

.top-row {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(min(100%, 300px), 1fr));
  gap: 1.25rem;
}

.card {
  background: #1e293b;
  padding: 1.25rem;
  border-radius: 14px;
  box-shadow: 0 0 12px rgba(0,0,0,.3);
  box-sizing: border-box;
  width: 100%;
}

.aqi-card {
  text-align: center;
}

.aqi-card h2 {
  margin: 0 0 0.75rem 0;
  font-size: clamp(1rem, 2.5vw, 1.25rem);
}

.aqi {
  font-size: clamp(2.5rem, 6vw, 3.5rem);
  font-weight: bold;
  margin: 0.5rem 0;
}

.level {
  font-size: clamp(0.9rem, 2vw, 1.1rem);
  opacity: 0.8;
}

.pollutant {
  margin-top: 1rem;
  font-size: clamp(0.8rem, 1.8vw, 0.9rem);
  opacity: 0.8;
}

.pollutant strong {
  font-weight: 600;
}

.card small {
  font-size: clamp(0.7rem, 1.5vw, 0.8rem);
  opacity: 0.7;
}

.card h2 {
  margin: 0 0 1rem 0;
  font-size: clamp(1rem, 2.5vw, 1.25rem);
}

.status-level {
  font-size: clamp(1.1rem, 2.5vw, 1.4rem);
  font-weight: bold;
  margin-bottom: 1rem;
}

.health-implications {
  margin: 0.8rem 0;
  font-weight: 500;
  font-size: clamp(0.85rem, 1.8vw, 0.95rem);
}

.cautionary-statement {
  margin-top: 1rem;
  font-style: italic;
  opacity: 0.85;
  padding: 0.8rem;
  background: rgba(255,255,255,0.05);
  border-radius: 8px;
  font-size: clamp(0.8rem, 1.8vw, 0.9rem);
}

.chart-card {
  width: 100%;
  position: relative;
  max-width: 100%;
  overflow: hidden;
}

.charts-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(min(300px, 100%), 1fr));
  gap: 1.5rem;
  width: 100%;
}

.mini-chart-container {
  background: rgba(15, 23, 42, 0.5);
  border: 1px solid rgba(148, 163, 184, 0.1);
  border-radius: 10px;
  padding: 1rem;
  height: 250px;
  display: flex;
  flex-direction: column;
}

.pollutant-chart-title {
  margin: 0 0 0.75rem 0;
  font-size: clamp(0.9rem, 2vw, 1rem);
  font-weight: 600;
  color: #f1f5f9;
  text-align: center;
}

.pollutant-unit {
  font-size: clamp(0.75rem, 1.6vw, 0.85rem);
  font-weight: 400;
  color: #94a3b8;
  margin-left: 0.25rem;
}

.mini-chart-container canvas {
  flex: 1;
  max-width: 100%;
  max-height: 100%;
}

.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.25rem;
  gap: 1rem;
  flex-wrap: wrap;
}

.chart-header h2 {
  margin: 0;
  font-size: clamp(1rem, 2.5vw, 1.25rem);
}

.station-selector {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  flex-wrap: wrap;
}

.station-selector label {
  font-size: clamp(0.8rem, 1.8vw, 0.9rem);
  color: #94a3b8;
  font-weight: 500;
}

.station-selector select {
  background-color: rgba(30, 41, 59, 0.8);
  color: #f1f5f9;
  border: 1px solid rgba(148, 163, 184, 0.3);
  border-radius: 8px;
  padding: 0.6rem 2.5rem 0.6rem 1rem;
  font-size: clamp(0.8rem, 1.8vw, 0.9rem);
  cursor: pointer;
  transition: all 0.2s ease;
  min-width: min(250px, 100%);
  max-width: 100%;
  appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 12 12'%3E%3Cpath fill='%2394a3b8' d='M6 9L1 4h10z'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 0.75rem center;
}

.station-selector select:hover:not(:disabled) {
  border-color: rgba(148, 163, 184, 0.5);
  background-color: rgba(30, 41, 59, 1);
}

.station-selector select:focus {
  outline: none;
  border-color: #2ecc71;
  box-shadow: 0 0 0 3px rgba(46, 204, 113, 0.1);
}

.station-selector select:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.loading-chart,
.error-chart,
.no-selection {
  text-align: center;
  padding: 3rem 2rem;
  color: #94a3b8;
  font-size: 0.95rem;
}

.error-chart {
  color: #e74c3c;
}

.loading-chart::after {
  content: '...';
  animation: dots 1.5s steps(4, end) infinite;
}

@keyframes dots {
  0%, 20% { content: '.'; }
  40% { content: '..'; }
  60%, 100% { content: '...'; }
}

.good { color: #2ecc71; }
.moderate { color: #f1c40f; }
.unhealthy { color: #e67e22; }
.danger { color: #e74c3c; }

/* Stations Card */
.stations-card {
  width: 100%;
  max-width: 100%;
  margin: 0 auto;
  box-sizing: border-box;
}

.stations-card h2 {
  margin: 0 0 1rem 0;
  font-size: clamp(1rem, 2.5vw, 1.25rem);
}

.no-data {
  text-align: center;
  padding: 2rem;
  opacity: 0.6;
  font-size: clamp(0.85rem, 1.8vw, 0.95rem);
}

.stations-list {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.station-item {
  background: rgba(15, 23, 42, 0.5);
  border: 1px solid rgba(148, 163, 184, 0.1);
  border-radius: 10px;
  padding: 1rem;
  transition: all 0.3s ease;
  box-sizing: border-box;
  width: 100%;
}

.station-item:hover {
  border-color: rgba(148, 163, 184, 0.3);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.station-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid rgba(148, 163, 184, 0.1);
  gap: 1rem;
  flex-wrap: wrap;
}

.station-name {
  margin: 0;
  font-size: clamp(0.95rem, 2.2vw, 1.1rem);
  font-weight: 600;
  color: #f1f5f9;
}

.station-location {
  margin: 0.25rem 0 0 0;
  font-size: clamp(0.75rem, 1.6vw, 0.85rem);
  color: #94a3b8;
}

.station-updated {
  margin: 0.25rem 0 0 0;
  font-size: clamp(0.7rem, 1.5vw, 0.8rem);
  color: #64748b;
  font-style: italic;
}

.station-aqi {
  font-size: clamp(1.4rem, 3vw, 1.8rem);
  font-weight: bold;
  padding: 0.5rem 1rem;
  border-radius: 8px;
  min-width: 60px;
  text-align: center;
}

.pollutants-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(min(120px, 100%), 1fr));
  gap: 0.6rem;
}

.pollutant-badge {
  background: rgba(30, 41, 59, 0.8);
  border: 1px solid rgba(148, 163, 184, 0.15);
  border-radius: 8px;
  padding: 0.75rem;
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
  transition: all 0.2s ease;
  box-sizing: border-box;
}

.pollutant-badge:hover {
  background: rgba(30, 41, 59, 1);
  border-color: rgba(148, 163, 184, 0.3);
}

.pollutant-name {
  font-size: clamp(0.65rem, 1.4vw, 0.75rem);
  font-weight: 600;
  color: #64748b;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.pollutant-value {
  font-size: clamp(0.9rem, 2vw, 1rem);
  font-weight: bold;
  color: #f1f5f9;
}

.pollutant-value small {
  font-size: clamp(0.65rem, 1.3vw, 0.7rem);
  font-weight: normal;
  color: #94a3b8;
  margin-left: 2px;
}

.pollutant-aqi {
  font-size: clamp(0.65rem, 1.3vw, 0.7rem);
  font-weight: 600;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  width: fit-content;
}

/* AQI Color Classes */
.aqi-good {
  background-color: rgba(46, 204, 113, 0.2);
  color: #2ecc71;
  border: 1px solid rgba(46, 204, 113, 0.3);
}

.aqi-moderate {
  background-color: rgba(241, 196, 15, 0.2);
  color: #f1c40f;
  border: 1px solid rgba(241, 196, 15, 0.3);
}

.aqi-unhealthy {
  background-color: rgba(230, 126, 34, 0.2);
  color: #e67e22;
  border: 1px solid rgba(230, 126, 34, 0.3);
}

.aqi-danger {
  background-color: rgba(231, 76, 60, 0.2);
  color: #e74c3c;
  border: 1px solid rgba(231, 76, 60, 0.3);
}

.loading-chart,
.error-chart,
.no-selection {
  text-align: center;
  padding: 2rem 1rem;
  color: #94a3b8;
  font-size: clamp(0.85rem, 1.8vw, 0.95rem);
}

.error-chart {
  color: #e74c3c;
}

.loading-chart::after {
  content: '...';
  animation: dots 1.5s steps(4, end) infinite;
}

@keyframes dots {
  0%, 20% { content: '.'; }
  40% { content: '..'; }
  60%, 100% { content: '...'; }
}

.good { color: #2ecc71; }
.moderate { color: #f1c40f; }
.unhealthy { color: #e67e22; }
.danger { color: #e74c3c; }

@media (max-width: 768px) {
  .dashboard {
    padding: 1rem;
  }

  .top-row {
    grid-template-columns: 1fr;
  }

  .chart-header {
    flex-direction: column;
    align-items: flex-start;
  }

  .station-selector {
    width: 100%;
  }

  .station-selector select {
    width: 100%;
    min-width: unset;
  }

  .charts-grid {
    grid-template-columns: 1fr;
  }

  .mini-chart-container {
    height: 220px;
  }

  .pollutants-grid {
    grid-template-columns: repeat(auto-fit, minmax(min(110px, 100%), 1fr));
  }

  .station-header {
    flex-direction: column;
    align-items: flex-start;
  }

  .station-aqi {
    align-self: flex-start;
  }
}

@media (max-width: 480px) {
  .dashboard {
    padding: 0.75rem;
  }

  .dashboard-layout {
    gap: 1rem;
  }

  .card {
    padding: 1rem;
  }

  .mini-chart-container {
    height: 200px;
  }

  .pollutants-grid {
    grid-template-columns: 1fr;
  }
}
</style>
