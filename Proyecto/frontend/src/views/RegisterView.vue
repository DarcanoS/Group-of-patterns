<template>
  <section class="auth-container">
    <h2>Crear cuenta?</h2>

    <form @submit.prevent="register">
      <input v-model="name" type="text" placeholder="Name" required />
      <input v-model="email" type="email" placeholder="Email" required />
      <input v-model="password" type="password" placeholder="Password" required />

      <button type="submit">Registro</button>

      <p class="link" @click="goLogin">
       Ya tiene una cuenta?
      </p>
    </form>
  </section>
</template>

<script setup lang="ts">
import { ref } from "vue";
import { useRouter } from "vue-router";

const router = useRouter();
const name = ref("");
const email = ref("");
const password = ref("");

const register = () => {
  console.log("Register:", name.value, email.value, password.value);
  router.push("/login"); // Simulación
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
}

.link {
  margin-top: 10px;
  color: #38bdf8;
  cursor: pointer;
  font-size: 14px;
}
</style>
