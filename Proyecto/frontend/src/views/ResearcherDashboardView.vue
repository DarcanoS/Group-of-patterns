<template>
  <div class="researcher-dashboard">
    <h1>historicos</h1>
    <p class="subtitle">Analizar</p>

    <!-- Filters card -->
    <div class="card filters-card" role="region" aria-label="Filters">
      <div class="filters-grid">
        <label>
          City
          <select v-model="filters.city" @change="onFilterChange">
            <option value="">todo</option>
            <option>Bogotá</option>
            <option>Medellín</option>
            <option>Cali</option>
          </select>
        </label>

        <label>
          Estacion
          <select v-model="filters.station" @change="onFilterChange">
            <option value="">All</option>
            <option>Estacion Centro</option>
            <option>Estacion Norte</option>
            <option>Estacion Sur</option>
          </select>
        </label>

        <label>
          polucion
          <select v-model="filters.pollutant" @change="onFilterChange">
            <option>PM2.5</option>
            <option>PM10</option>
            <option>O3</option>
            <option>NO2</option>
          </select>
        </label>

        <div class="date-range">
          <label>
            Start
            <input type="date" v-model="filters.startDate" @change="onFilterChange" />
          </label>
          <label>
            End
            <input type="date" v-model="filters.endDate" @change="onFilterChange" />
          </label>
        </div>
      </div>

      <div class="filters-actions">
        <button class="btn" @click="refresh">Apply</button>
        <button class="btn btn--secondary" @click="resetFilters">Reset</button>
      </div>
    </div>

    <!-- Chart card -->
    <div class="card">
      <div class="card-header">
        <h2>Daily AQI Trend</h2>
        <div class="card-actions">
          <button class="btn" @click="exportCSV" :disabled="!records.length">Export CSV</button>
          <button class="btn btn--ghost" @click="downloadJSON" :disabled="!records.length">Download JSON</button>
        </div>
      </div>

      <div v-if="loading" class="loading">Loading data...</div>
      <div v-if="error" class="error">{{ error }}</div>

      <div v-if="!loading && !error">
        <canvas ref="chartCanvas" aria-label="AQI trend chart"></canvas>
      </div>
    </div>

    <!-- Table / Records -->
    <div class="card">
      <h3>Data table</h3>
      <div v-if="records.length === 0" class="empty">No records to display</div>
      <table v-else class="table" role="table" aria-label="Daily AQI records">
        <thead>
          <tr>
            <th>fecha</th>
            <th>Ciudad</th>
            <th>Estacion</th>
            <th>polucion</th>
            <th>Promedio AQI</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="r in records" :key="r.date + r.station">
            <td>{{ r.date }}</td>
            <td>{{ r.city }}</td>
            <td>{{ r.station }}</td>
            <td>{{ r.pollutant }}</td>
            <td>{{ r.avg_aqi }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch, nextTick } from "vue";
import Chart from "chart.js/auto";
import { fetchDailyStats } from "../services/researchService";

const filters = ref({
  city: "",
  station: "",
  pollutant: "PM2.5",
  startDate: "",
  endDate: ""
});

const loading = ref(false);
const error = ref<string | null>(null);
const labels = ref<string[]>([]);
const values = ref<number[]>([]);
const records = ref<any[]>([]);
const chartCanvas = ref<HTMLCanvasElement | null>(null);
let chartInstance: Chart | null = null;

async function loadData() {
  loading.value = true;
  error.value = null;
  try {
    const res = await fetchDailyStats(filters.value);
    labels.value = res.labels;
    values.value = res.values;
    records.value = res.records;
    await renderChart();
  } catch (e: any) {
    error.value = "Failed to load researcher data.";
    console.error(e);
  } finally {
    loading.value = false;
  }
}

async function renderChart() {
  await nextTick();
  if (!chartCanvas.value) return;

  if (chartInstance) {
    chartInstance.data.labels = labels.value;
    (chartInstance.data.datasets[0].data as number[]) = values.value;
    chartInstance.update();
    return;
  }

  chartInstance = new Chart(chartCanvas.value, {
    type: "line",
    data: {
      labels: labels.value,
      datasets: [
        {
          label: "Avg AQI",
          data: values.value,
          borderColor: getComputedStyle(document.documentElement).getPropertyValue("--color-primary-teal") || "#00897B",
          backgroundColor: "rgba(0,0,0,0)",
          tension: 0.35,
          pointRadius: 3
        }
      ]
    },
    options: {
      responsive: true,
      plugins: {
        legend: { display: false }
      },
      scales: {
        y: {
          beginAtZero: false,
          suggestedMin: 0
        }
      }
    }
  });
}

function onFilterChange() {
  // Optionally debounce in future - for now keep simple
}

function resetFilters() {
  filters.value = {
    city: "",
    station: "",
    pollutant: "PM2.5",
    startDate: "",
    endDate: ""
  };
  loadData();
}

function refresh() {
  loadData();
}

function exportCSV() {
  if (!records.value.length) return;
  const header = ["date", "city", "station", "pollutant", "avg_aqi"];
  const csvRows = [header.join(",")];
  for (const r of records.value) {
    const row = [r.date, r.city, r.station, r.pollutant, r.avg_aqi].map(x => `"${String(x).replace(/"/g, '""')}"`);
    csvRows.push(row.join(","));
  }
  const blob = new Blob([csvRows.join("\n")], { type: "text/csv;charset=utf-8;" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = `air-quality-export-${new Date().toISOString().slice(0,10)}.csv`;
  document.body.appendChild(a);
  a.click();
  a.remove();
  URL.revokeObjectURL(url);
}

function downloadJSON() {
  const blob = new Blob([JSON.stringify(records.value, null, 2)], { type: "application/json" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = `air-quality-export-${new Date().toISOString().slice(0,10)}.json`;
  document.body.appendChild(a);
  a.click();
  a.remove();
  URL.revokeObjectURL(url);
}

onMounted(() => {
  loadData();
});
</script>

<style scoped>
.researcher-dashboard {
  padding: var(--space-6);
  color: var(--color-text-primary);
}

.subtitle {
  color: var(--color-text-secondary);
  margin-bottom: var(--space-4);
}

.card {
  background: var(--color-bg-surface);
  border: 1px solid var(--color-border-subtle);
  padding: var(--space-4);
  border-radius: var(--radius-md);
  margin-bottom: var(--space-4);
}

/* Filters grid */
.filters-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: var(--space-4);
  align-items: end;
}
.filters-grid label {
  display: block;
}
.date-range input {
  display: block;
  width: 100%;
  margin-top: var(--space-2);
  padding: 8px;
  border-radius: var(--radius-sm);
  border: 1px solid var(--color-border-subtle);
  background: transparent;
  color: var(--color-text-primary);
}

.filters-actions {
  margin-top: var(--space-3);
  display: flex;
  gap: var(--space-3);
}

.btn {
  background: var(--color-primary-teal);
  color: white;
  padding: 8px 12px;
  border-radius: var(--radius-sm);
  border: none;
  cursor: pointer;
}

.btn--secondary {
  background: transparent;
  border: 1px solid var(--color-border-subtle);
  color: var(--color-text-primary);
}

.btn--ghost {
  background: transparent;
  border: none;
  color: var(--color-text-secondary);
  cursor: pointer;
}

/* Table */
.table {
  width: 100%;
  border-collapse: collapse;
}
.table th, .table td {
  padding: 10px;
  border-bottom: 1px solid var(--color-border-subtle);
  text-align: left;
}

/* Responsive */
@media (max-width: 900px) {
  .filters-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>
