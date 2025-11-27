<template>
  <div class="dashboard">
    <h1>tablero ciudadano</h1>
    <p class="subtitle">Calidad del aire actual {{ data?.city }}</p>

    <div v-if="loading" class="loading">cargando datos...</div>
    <div v-if="error" class="error">{{ error }}</div>

    <div v-if="data" class="grid">

      <!-- AQI CARD -->
      <div class="card aqi-card">
        <h2>Air Quality </h2>
        <p class="aqi" :class="aqiColor">{{ data.aqi }}</p>
        <span class="level">{{ data.level }}</span>
        <small>ultima actualizacion: {{ data.updatedAt }}</small>
      </div>

      <!-- STATUS CARD -->
      <div class="card">
        <h2>Status</h2>
        <p>{{ data.status }}</p>
        <p class="recommendation">{{ recommendation }}</p>
      </div>

      <!-- NEARBY STATIONS -->
      <div class="card">
        <h2>Estaciones cercanaas </h2>
        <ul>
          <li v-for="station in data.stations" :key="station.name">
            {{ station.name }} — AQI {{ station.aqi }}
          </li>
        </ul>
      </div>

      <!-- PRODUCT SUGGESTIONS -->
      <div class="card">
        <h2>Sugerencias </h2>
        <ul>
          <li v-for="product in data.products" :key="product.name">
            <strong>{{ product.name }}</strong>
            <p class="product-desc">{{ product.description }}</p>
          </li>
        </ul>
      </div>

      <!-- HISTORICAL CHART -->
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

.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
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

.recommendation {
  margin-top: 1rem;
  font-style: italic;
}

.product-desc {
  font-size: 0.9rem;
  opacity: 0.7;
}

.chart-card {
  grid-column: span 2;
}

.good { color: #2ecc71; }
.moderate { color: #f1c40f; }
.unhealthy { color: #e67e22; }
.danger { color: #e74c3c; }
</style>
