<template>
  <div class="dashboard">
    <h1>tablero ciudadano</h1>
    <p class="subtitle">Calidad del aire actual {{ data?.city }}</p>

    <div v-if="loading" class="loading">cargando datos...</div>
    <div v-if="error" class="error">{{ error }}</div>

    <div v-if="data" class="grid">

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


      <!-- NEARBY STATIONS (FULL WIDTH) -->
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

      <!-- HISTORICAL CHART (FULL WIDTH) -->
      <div class="card chart-card">
        <h2>Historico de 7 dias </h2>
        <canvas ref="chartCanvas"></canvas>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, nextTick } from "vue";
import Chart from "chart.js/auto";
import { getAirQuality } from "../services/api";

const loading = ref(true);
const error = ref(null);
const data = ref(null);
const chartCanvas = ref(null);

onMounted(async () => {
  try {
    data.value = await getAirQuality();
    await nextTick();

    new Chart(chartCanvas.value, {
      type: "line",
      data: {
        labels: ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
        datasets: [
          {
            label: "AQI",
            data: data.value.history,
            fill: false,
            tension: 0.4
          }
        ]
      },
      options: {
        responsive: true,
        plugins: {
          legend: { display: false }
        }
      }
    });

  } catch (err) {
    error.value = "Unable to connect to air quality service.";
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
</script>

<style scoped>
.dashboard {
  padding: 2rem;
  color: white;
  background: #0f172a;
  min-height: 100vh;
}

.subtitle {
  opacity: 0.7;
  margin-bottom: 2rem;
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
  gap: 1.5rem;
}

.top-row {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1.5rem;
}

.card {
  background: #1e293b;
  padding: 1.5rem;
  border-radius: 14px;
  box-shadow: 0 0 12px rgba(0,0,0,.3);
}

.aqi-card {
  text-align: center;
}

.aqi {
  font-size: 3.5rem;
  font-weight: bold;
  margin: 0.5rem 0;
}

.level {
  font-size: 1.1rem;
  opacity: 0.8;
}

.pollutant {
  margin-top: 1rem;
  font-size: 0.9rem;
  opacity: 0.8;
}

.status-level {
  font-size: 1.4rem;
  font-weight: bold;
  margin-bottom: 1rem;
}

.health-implications {
  margin: 0.8rem 0;
  font-weight: 500;
}

.cautionary-statement {
  margin-top: 1rem;
  font-style: italic;
  opacity: 0.85;
  padding: 0.8rem;
  background: rgba(255,255,255,0.05);
  border-radius: 8px;
}

.chart-card {
  width: 100%;
}

.good { color: #2ecc71; }
.moderate { color: #f1c40f; }
.unhealthy { color: #e67e22; }
.danger { color: #e74c3c; }

/* Stations Card */
.stations-card {
  width: 100%;
}

.no-data {
  text-align: center;
  padding: 2rem;
  opacity: 0.6;
}

.stations-list {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.station-item {
  background: rgba(15, 23, 42, 0.5);
  border: 1px solid rgba(148, 163, 184, 0.1);
  border-radius: 10px;
  padding: 1.25rem;
  transition: all 0.3s ease;
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
}

.station-name {
  margin: 0;
  font-size: 1.1rem;
  font-weight: 600;
  color: #f1f5f9;
}

.station-location {
  margin: 0.25rem 0 0 0;
  font-size: 0.85rem;
  color: #94a3b8;
}

.station-updated {
  margin: 0.25rem 0 0 0;
  font-size: 0.8rem;
  color: #64748b;
  font-style: italic;
}

.station-aqi {
  font-size: 1.8rem;
  font-weight: bold;
  padding: 0.5rem 1rem;
  border-radius: 8px;
  min-width: 60px;
  text-align: center;
}

.pollutants-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
  gap: 0.75rem;
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
}

.pollutant-badge:hover {
  background: rgba(30, 41, 59, 1);
  border-color: rgba(148, 163, 184, 0.3);
}

.pollutant-name {
  font-size: 0.75rem;
  font-weight: 600;
  color: #64748b;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.pollutant-value {
  font-size: 1rem;
  font-weight: bold;
  color: #f1f5f9;
}

.pollutant-value small {
  font-size: 0.7rem;
  font-weight: normal;
  color: #94a3b8;
  margin-left: 2px;
}

.pollutant-aqi {
  font-size: 0.7rem;
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

@media (max-width: 768px) {
  .top-row {
    grid-template-columns: 1fr;
  }

  .pollutants-grid {
    grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
  }
}
</style>
