<template>
  <section class="auth-container">
    <h2>Crear cuenta</h2>

    <form @submit.prevent="handleRegister">
      <input v-model="name" type="text" placeholder="Nombre completo" required />
      <input v-model="email" type="email" placeholder="Email" required />
      <input v-model="password" type="password" placeholder="Password" required minlength="6" />

      <button type="submit" :disabled="loading">
        {{ loading ? 'Registrando...' : 'Registro' }}
      </button>

      <p v-if="error" class="error">{{ error }}</p>
      <p v-if="success" class="success">{{ success }}</p>

      <p class="link" @click="goLogin">
        ¿Ya tienes una cuenta? Iniciar sesión
      </p>
    </form>
  </section>
</template>

<script setup lang="ts">
import { ref } from "vue";
import { useRouter } from "vue-router";
import { register } from "@/services/authService";

const router = useRouter();
const name = ref("");
const email = ref("");
const password = ref("");
const loading = ref(false);
const error = ref("");
const success = ref("");

const handleRegister = async () => {
  loading.value = true;
  error.value = "";
  success.value = "";

  try {
    console.log("🔄 Intentando registro:", name.value, email.value);

    const response = await register({
      email: email.value,
      password: password.value,
      full_name: name.value,
      role_id: 1 // Por defecto, registramos como Citizen (rol_id: 1)
    });

    console.log("✅ Registro exitoso:", response);
    success.value = "¡Registro exitoso! Redirigiendo al login...";

    // Esperar 2 segundos para mostrar el mensaje de éxito
    setTimeout(() => {
      router.push("/login");
    }, 2000);

  } catch (err: any) {
    console.error("❌ Error en registro:", err);
    error.value = err.message || "Error al registrar. Por favor intenta de nuevo.";
  } finally {
    loading.value = false;
  }
};

const goLogin = () => {
  router.push("/login");
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
  background: #22c55e;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: background 0.3s;
}

button:hover:not(:disabled) {
  background: #16a34a;
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

.success {
  margin-top: 15px;
  padding: 10px;
  background: #22c55e;
  border-radius: 8px;
  color: white;
  font-size: 14px;
}

.link {
  margin-top: 10px;
  color: #38bdf8;
  cursor: pointer;
  font-size: 14px;
  text-decoration: underline;
}

.link:hover {
  color: #7dd3fc;
}
</style>
