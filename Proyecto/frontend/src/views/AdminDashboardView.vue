<template>
  <div class="dashboard">
    <h1>Admin Dashboard</h1>

    <div v-if="loading" class="loading">Cargando datos del sistema...</div>
    <div v-if="error" class="error">{{ error }}</div>

    <!-- SYSTEM STATUS -->
    <div class="card">
      <h2>System Status</h2>
      <p><strong>Backend:</strong> {{ system.status }}</p>
      <p><strong>Database:</strong> {{ system.database }}</p>
      <p><strong>Info:</strong> {{ system.message }}</p>
      <p><strong>Last Sync:</strong> {{ system.lastSync }}</p>
    </div>

    <!-- USERS MANAGEMENT -->
    <div class="card">
      <h2>Users Management</h2>
      <p v-if="loadingUsers">Cargando usuarios...</p>
      <table v-else-if="users.length > 0">
        <thead>
          <tr>
            <th>ID</th>
            <th>Nombre</th>
            <th>Email</th>
            <th>Rol</th>
            <th>Estado</th>
            <th>Fecha Creación</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="user in users" :key="user.id">
            <td>{{ user.id }}</td>
            <td>{{ user.full_name }}</td>
            <td>{{ user.email }}</td>
            <td>
              <span class="badge" :class="getRoleBadgeClass(user.role.name)">
                {{ user.role.name }}
              </span>
            </td>
            <td>
              <span :class="user.is_active ? 'status-active' : 'status-inactive'">
                {{ user.is_active ? 'Activo' : 'Inactivo' }}
              </span>
            </td>
            <td>{{ formatDate(user.created_at) }}</td>
          </tr>
        </tbody>
      </table>
      <p v-else>No hay usuarios registrados.</p>
    </div>

    <!-- STATIONS MANAGEMENT -->
    <div class="card">
      <h2>Estaciones de calidad de aire</h2>
      <p v-if="loadingStations">Cargando estaciones...</p>
      <table v-else-if="stations.length > 0">
        <thead>
          <tr>
            <th>ID</th>
            <th>Nombre</th>
            <th>Ciudad</th>
            <th>País</th>
            <th>Latitud</th>
            <th>Longitud</th>
            <th>Estado</th>
            <th>Fecha Creación</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="station in stations" :key="station.id">
            <td>{{ station.id }}</td>
            <td>{{ station.name }}</td>
            <td>{{ station.city }}</td>
            <td>{{ station.country }}</td>
            <td>{{ station.latitude.toFixed(4) }}</td>
            <td>{{ station.longitude.toFixed(4) }}</td>
            <td>
              <span :class="station.is_active ? 'status-active' : 'status-inactive'">
                {{ station.is_active ? 'Activa' : 'Inactiva' }}
              </span>
            </td>
            <td>{{ formatDate(station.created_at) }}</td>
          </tr>
        </tbody>
      </table>
      <p v-else>No hay estaciones registradas.</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import { getHealthStatus, getUsers, getStations } from "@/services/adminService";

const loading = ref(true);
const loadingUsers = ref(true);
const loadingStations = ref(true);
const error = ref("");

const system = ref({
  status: "Unknown",
  database: "Unknown",
  message: "",
  lastSync: ""
});

const users = ref<any[]>([]);
const stations = ref<any[]>([]);

// Cargar estado del sistema
async function loadSystemHealth() {
  try {
    console.log("🔄 Obteniendo estado del sistema...");
    const health = await getHealthStatus();
    system.value = {
      status: health.status,
      database: health.database,
      message: health.message,
      lastSync: new Date().toLocaleString()
    };
    console.log("✅ Estado del sistema obtenido:", health);
  } catch (err: any) {
    console.error("❌ Error obteniendo estado del sistema:", err);
    error.value = "Error al obtener el estado del sistema";
  } finally {
    loading.value = false;
  }
}

// Cargar usuarios
async function loadUsers() {
  try {
    console.log("🔄 Obteniendo usuarios...");
    const data = await getUsers(0, 100);
    users.value = data;
    console.log("✅ Usuarios obtenidos:", data.length);
  } catch (err: any) {
    console.error("❌ Error obteniendo usuarios:", err);
    error.value = "Error al obtener usuarios del sistema";
  } finally {
    loadingUsers.value = false;
  }
}

// Cargar estaciones
async function loadStations() {
  try {
    console.log("🔄 Obteniendo estaciones...");
    const data = await getStations(0, 100);
    stations.value = data;
    console.log("✅ Estaciones obtenidas:", data.length);
  } catch (err: any) {
    console.error("❌ Error obteniendo estaciones:", err);
    error.value = "Error al obtener estaciones";
  } finally {
    loadingStations.value = false;
  }
}

// Formatear fecha
function formatDate(dateString: string): string {
  const date = new Date(dateString);
  return date.toLocaleDateString('es-ES', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  });
}

// Obtener clase CSS para el badge del rol
function getRoleBadgeClass(roleName: string): string {
  const roleMap: Record<string, string> = {
    'Admin': 'badge-admin',
    'Researcher': 'badge-researcher',
    'Citizen': 'badge-citizen'
  };
  return roleMap[roleName] || 'badge-default';
}

// Cargar todos los datos al montar el componente
onMounted(() => {
  loadSystemHealth();
  loadUsers();
  loadStations();
});
</script>

<style scoped>
.dashboard {
  padding: 2rem;
  color: white;
}

h1 {
  margin-bottom: 2rem;
}

.loading {
  padding: 2rem;
  text-align: center;
  background: #1f2937;
  border-radius: 12px;
  margin-bottom: 2rem;
  color: #60a5fa;
  font-size: 1.1rem;
}

.error {
  padding: 1rem;
  background: #ef4444;
  border-radius: 8px;
  margin-bottom: 2rem;
  color: white;
}

.card {
  background: #1f2937;
  padding: 1.5rem;
  border-radius: 12px;
  margin-bottom: 2rem;
}

h2 {
  margin-bottom: 1rem;
  color: #60a5fa;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 1rem;
}

th, td {
  padding: 12px;
  border-bottom: 1px solid #374151;
  text-align: left;
}

th {
  background: #111827;
  font-weight: 600;
  color: #9ca3af;
  text-transform: uppercase;
  font-size: 0.75rem;
  letter-spacing: 0.05em;
}

tbody tr:hover {
  background: #111827;
}

.badge {
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 0.875rem;
  font-weight: 600;
  display: inline-block;
}

.badge-admin {
  background: #dc2626;
  color: white;
}

.badge-researcher {
  background: #2563eb;
  color: white;
}

.badge-citizen {
  background: #059669;
  color: white;
}

.badge-default {
  background: #6b7280;
  color: white;
}

.status-active {
  color: #10b981;
  font-weight: 600;
}

.status-inactive {
  color: #6b7280;
  font-weight: 600;
}

button {
  margin-right: 8px;
  padding: 6px 10px;
  border-radius: 6px;
  border: none;
  cursor: pointer;
  font-size: 0.875rem;
}

.danger {
  background-color: #dc2626;
  color: white;
}

.danger:hover {
  background-color: #b91c1c;
}

p strong {
  color: #9ca3af;
  margin-right: 0.5rem;
}
</style>
