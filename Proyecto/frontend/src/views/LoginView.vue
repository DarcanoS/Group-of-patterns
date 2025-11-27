<template>
  <section class="auth-container">
    <h2>Iniciar Sesión</h2>

    <form @submit.prevent="handleLogin">
      <input v-model="email" type="email" placeholder="Email" required />
      <input v-model="password" type="password" placeholder="Password" required />

      <button type="submit" :disabled="loading">
        {{ loading ? 'Iniciando sesión...' : 'Login' }}
      </button>

      <p v-if="error" class="error">{{ error }}</p>
      <p class="link" @click="goRegister">¿Sin cuenta? Registrar</p>
    </form>
  </section>
</template>

<script setup lang="ts">
import { ref } from "vue";
import { useRouter } from "vue-router";
import { login } from "@/services/authService";

const router = useRouter();
const email = ref("");
const password = ref("");
const loading = ref(false);
const error = ref("");

const handleLogin = async () => {
  loading.value = true;
  error.value = "";

  try {
    console.log("🔄 Intentando login con:", email.value);
    const response = await login(email.value, password.value);

    console.log("✅ Login exitoso:", response);
    console.log("👤 Usuario:", response.user);
    console.log("🎭 Rol:", response.user.role.name);

    // Redireccionar según el rol del usuario
    const roleName = response.user.role.name.toLowerCase();

    if (roleName === 'citizen') {
      router.push('/dashboard/citizen');
    } else if (roleName === 'researcher') {
      router.push('/dashboard/researcher');
    } else if (roleName === 'admin') {
      router.push('/dashboard/admin');
    } else {
      router.push('/');
    }

  } catch (err: any) {
    console.error("❌ Error en login:", err);
    error.value = err.message || "Error al iniciar sesión. Verifica tus credenciales.";
  } finally {
    loading.value = false;
  }
};

const goRegister = () => {
  router.push("/register");
};
</script>

<style scoped>
.auth-container {
  max-width: 400px;
  margin: 120px auto;
  padding: 40px;
  background: #1e293b;
  border-radius: 12px;
  text-align: center;
  color: white;
}

h2 {
  margin-bottom: 20px;
}

input {
  width: 100%;
  margin: 10px 0;
  padding: 10px;
  border-radius: 8px;
  border: none;
}

button {
  margin-top: 10px;
  width: 100%;
  padding: 10px;
  background: #0ea5e9;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: background 0.3s;
}

button:hover:not(:disabled) {
  background: #0284c7;
}

button:disabled {
  background: #64748b;
  cursor: not-allowed;
}

.error {
  margin-top: 15px;
  padding: 10px;
  background: #ef4444;
  border-radius: 8px;
  color: white;
  font-size: 14px;
}

.link {
  margin-top: 10px;
  color: #38bdf8;
  cursor: pointer;
  text-decoration: underline;
}

.link:hover {
  color: #7dd3fc;
}
</style>
