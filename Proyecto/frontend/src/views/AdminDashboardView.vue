<template>
  <div class="dashboard">
    <h1>Admin Dashboard</h1>

    <!-- SYSTEM STATUS -->
    <div class="card">
      <h2>System Status</h2>
      <p><strong>Backend:</strong> {{ system.backend }}</p>
      <p><strong>Last Sync:</strong> {{ system.lastSync }}</p>
      <p><strong>Total Records:</strong> {{ system.totalRecords }}</p>
    </div>

    <!-- USERS MANAGEMENT -->
    <div class="card">
      <h2>Users Management</h2>
      <table>
        <thead>
          <tr>
            <th>Nombre</th>
            <th>Email</th>
            <th>Rol</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="user in users" :key="user.id">
            <td>{{ user.name }}</td>
            <td>{{ user.email }}</td>
            <td>{{ user.role }}</td>
            <td>
              <button @click="editUser(user)">Edit</button>
              <button class="danger" @click="deleteUser(user.id)">Delete</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- STATIONS MANAGEMENT -->
    <div class="card">
      <h2>Estaciones de calidad de aire</h2>
      <table>
        <thead>
          <tr>
            <th>Nombre</th>
            <th>Ciudad</th>
            <th>Estatus</th>
            <th>AQI</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="station in stations" :key="station.id">
            <td>{{ station.name }}</td>
            <td>{{ station.city }}</td>
            <td>{{ station.status }}</td>
            <td>{{ station.aqi }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";

const system = ref({
  backend: "Connected (Mock)",
  lastSync: new Date().toLocaleString(),
  totalRecords: 3120
});

const users = ref([
  { id: 1, name: "Admin User", email: "admin@test.com", role: "Admin" },
  { id: 2, name: "Research User", email: "research@test.com", role: "Researcher" },
  { id: 3, name: "Citizen User", email: "citizen@test.com", role: "Citizen" }
]);

const stations = ref([
  { id: 1, name: "Station Norte", city: "Bogotá", status: "Active", aqi: 72 },
  { id: 2, name: "Station Sur", city: "Bogotá", status: "Active", aqi: 88 },
  { id: 3, name: "Station Centro", city: "Medellín", status: "Maintenance", aqi: 55 }
]);

function editUser(user) {
  alert(`Edit user: ${user.name}`);
}

function deleteUser(id) {
  users.value = users.value.filter(user => user.id !== id);
}
</script>

<style scoped>
.dashboard {
  padding: 2rem;
}

h1 {
  margin-bottom: 2rem;
}

.card {
  background: #1f2937;
  padding: 1.5rem;
  border-radius: 12px;
  margin-bottom: 2rem;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th, td {
  padding: 10px;
  border-bottom: 1px solid #374151;
  text-align: left;
}

button {
  margin-right: 8px;
  padding: 6px 10px;
  border-radius: 6px;
  border: none;
  cursor: pointer;
}

.danger {
  background-color: #dc2626;
  color: white;
}
</style>
