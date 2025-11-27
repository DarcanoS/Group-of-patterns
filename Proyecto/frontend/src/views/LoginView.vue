<template>
  <div class="auth-page">
    <div class="auth-page__background">
      <!-- Animated background circles -->
      <div class="bg-circle bg-circle--1"></div>
      <div class="bg-circle bg-circle--2"></div>
      <div class="bg-circle bg-circle--3"></div>
    </div>

    <div class="auth-page__content">
      <!-- Back to home link -->
      <router-link to="/" class="auth-page__back">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <line x1="19" y1="12" x2="5" y2="12"/>
          <polyline points="12 19 5 12 12 5"/>
        </svg>
        Back to home
      </router-link>

      <div class="auth-card">
        <!-- Logo and Title -->
        <div class="auth-card__header">
          <div class="auth-card__logo">
            <svg width="48" height="48" viewBox="0 0 48 48" fill="none">
              <circle cx="24" cy="24" r="20" stroke="var(--color-primary-teal)" stroke-width="2" opacity="0.3"/>
              <circle cx="24" cy="24" r="14" stroke="var(--color-primary-teal)" stroke-width="2"/>
              <circle cx="24" cy="24" r="8" fill="var(--color-primary-teal)"/>
              <path d="M24 4 L24 10" stroke="var(--color-secondary-green)" stroke-width="2" stroke-linecap="round"/>
              <path d="M24 38 L24 44" stroke="var(--color-secondary-green)" stroke-width="2" stroke-linecap="round"/>
              <path d="M4 24 L10 24" stroke="var(--color-secondary-green)" stroke-width="2" stroke-linecap="round"/>
              <path d="M38 24 L44 24" stroke="var(--color-secondary-green)" stroke-width="2" stroke-linecap="round"/>
            </svg>
          </div>
          <h1 class="auth-card__title">Welcome back</h1>
          <p class="auth-card__subtitle">Sign in to access your dashboard</p>
        </div>

        <!-- Login Form -->
        <form @submit.prevent="handleLogin" class="auth-form">
          <!-- Email Input -->
          <div class="form-group">
            <label for="email" class="form-label">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/>
                <polyline points="22,6 12,13 2,6"/>
              </svg>
              Email address
            </label>
            <input
              id="email"
              v-model="email"
              type="email"
              class="form-input"
              placeholder="you@example.com"
              required
              autocomplete="email"
            />
          </div>

          <!-- Password Input -->
          <div class="form-group">
            <label for="password" class="form-label">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <rect x="3" y="11" width="18" height="11" rx="2" ry="2"/>
                <path d="M7 11V7a5 5 0 0 1 10 0v4"/>
              </svg>
              Password
            </label>
            <div class="password-input-wrapper">
              <input
                id="password"
                v-model="password"
                :type="showPassword ? 'text' : 'password'"
                class="form-input"
                placeholder="Enter your password"
                required
                autocomplete="current-password"
              />
              <button
                type="button"
                class="password-toggle"
                @click="showPassword = !showPassword"
                aria-label="Toggle password visibility"
              >
                <svg v-if="!showPassword" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>
                  <circle cx="12" cy="12" r="3"/>
                </svg>
                <svg v-else width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"/>
                  <line x1="1" y1="1" x2="23" y2="23"/>
                </svg>
              </button>
            </div>
          </div>

          <!-- Remember me and Forgot password -->
          <div class="form-options">
            <label class="checkbox-label">
              <input type="checkbox" class="checkbox-input" />
              <span>Remember me</span>
            </label>
            <a href="#" class="form-link">Forgot password?</a>
          </div>

          <!-- Error Message -->
          <transition name="fade">
            <div v-if="error" class="alert alert--error">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="10"/>
                <line x1="12" y1="8" x2="12" y2="12"/>
                <line x1="12" y1="16" x2="12.01" y2="16"/>
              </svg>
              {{ error }}
            </div>
          </transition>

          <!-- Submit Button -->
          <button type="submit" class="btn btn--primary btn--large" :disabled="loading">
            <span v-if="!loading">Sign in</span>
            <span v-else class="btn-loading">
              <svg class="spinner" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="10"/>
              </svg>
              Signing in...
            </span>
          </button>
        </form>

        <!-- Footer -->
        <div class="auth-card__footer">
          <p class="auth-card__footer-text">
            Don't have an account?
            <router-link to="/register" class="auth-card__footer-link">Sign up for free</router-link>
          </p>
        </div>
      </div>

      <!-- Additional Info -->
      <div class="auth-page__info">
        <div class="info-item">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
          </svg>
          <span>Secure authentication</span>
        </div>
        <div class="info-item">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="10"/>
            <polyline points="12 6 12 12 16 14"/>
          </svg>
          <span>Access 24/7</span>
        </div>
        <div class="info-item">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
            <circle cx="12" cy="7" r="4"/>
          </svg>
          <span>Multi-role support</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import { useRouter } from "vue-router";
import { login } from "@/services/authService";

const router = useRouter();
const email = ref("");
const password = ref("");
const showPassword = ref(false);
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

</script>

<style scoped>
.auth-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: var(--space-5);
  position: relative;
  overflow: hidden;
}

.auth-page__background {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 0;
  background: linear-gradient(135deg, var(--color-bg-app) 0%, rgba(18, 24, 38, 0.95) 100%);
}

.bg-circle {
  position: absolute;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(0, 137, 123, 0.15) 0%, transparent 70%);
  animation: float 20s ease-in-out infinite;
}

.bg-circle--1 {
  width: 400px;
  height: 400px;
  top: -200px;
  left: -100px;
  animation-delay: 0s;
}

.bg-circle--2 {
  width: 300px;
  height: 300px;
  bottom: -150px;
  right: -50px;
  animation-delay: -7s;
}

.bg-circle--3 {
  width: 250px;
  height: 250px;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  animation-delay: -14s;
}

@keyframes float {
  0%, 100% {
    transform: translate(0, 0) scale(1);
  }
  33% {
    transform: translate(30px, -30px) scale(1.1);
  }
  66% {
    transform: translate(-20px, 20px) scale(0.9);
  }
}

.auth-page__content {
  position: relative;
  z-index: 1;
  width: 100%;
  max-width: 460px;
  display: flex;
  flex-direction: column;
  align-items: stretch;
}

.auth-page__back {
  display: inline-flex;
  align-items: center;
  gap: var(--space-2);
  color: var(--color-text-secondary);
  text-decoration: none;
  margin-bottom: var(--space-5);
  font-size: 14px;
  font-weight: 500;
  transition: all 0.2s ease;
}

.auth-page__back:hover {
  color: var(--color-primary-teal);
  gap: var(--space-3);
}

.auth-card {
  background: var(--color-bg-surface);
  border: 1px solid var(--color-border-subtle);
  border-radius: var(--radius-lg);
  padding: var(--space-6);
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.4);
  width: 100%;
  max-width: 460px;
}

.auth-card__header {
  text-align: center;
  margin-bottom: var(--space-6);
}

.auth-card__logo {
  display: flex;
  justify-content: center;
  margin-bottom: var(--space-4);
}

.auth-card__title {
  font-size: 28px;
  font-weight: 700;
  color: var(--color-text-primary);
  margin: 0 0 var(--space-2);
}

.auth-card__subtitle {
  color: var(--color-text-secondary);
  font-size: 15px;
  margin: 0;
}

.auth-form {
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.form-label {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  font-size: 14px;
  font-weight: 600;
  color: var(--color-text-primary);
}

.form-label svg {
  color: var(--color-text-secondary);
}

.form-input {
  width: 100%;
  padding: var(--space-3) var(--space-4);
  background: rgba(0, 0, 0, 0.2);
  border: 1px solid var(--color-border-subtle);
  border-radius: var(--radius-md);
  color: var(--color-text-primary);
  font-size: 15px;
  transition: all 0.2s ease;
  box-sizing: border-box;
}

.form-input::placeholder {
  color: var(--color-text-secondary);
  opacity: 0.6;
}

.form-input:focus {
  outline: none;
  border-color: var(--color-primary-teal);
  background: rgba(0, 137, 123, 0.05);
  box-shadow: 0 0 0 3px rgba(0, 137, 123, 0.1);
}

.password-input-wrapper {
  position: relative;
  width: 100%;
}

.password-input-wrapper .form-input {
  padding-right: 48px;
  box-sizing: border-box;
}

.password-toggle {
  position: absolute;
  right: var(--space-3);
  top: 50%;
  transform: translateY(-50%);
  background: transparent;
  border: none;
  color: var(--color-text-secondary);
  cursor: pointer;
  padding: var(--space-1);
  display: flex;
  align-items: center;
  border-radius: var(--radius-sm);
  transition: all 0.2s ease;
}

.password-toggle:hover {
  color: var(--color-primary-teal);
  background: rgba(0, 137, 123, 0.1);
}

.form-options {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  font-size: 14px;
  color: var(--color-text-secondary);
  cursor: pointer;
}

.checkbox-input {
  width: 18px;
  height: 18px;
  cursor: pointer;
  accent-color: var(--color-primary-teal);
}

.form-link {
  font-size: 14px;
  color: var(--color-primary-teal);
  text-decoration: none;
  font-weight: 500;
  transition: color 0.2s ease;
}

.form-link:hover {
  color: var(--color-secondary-green);
  text-decoration: underline;
}

.alert {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-3) var(--space-4);
  border-radius: var(--radius-md);
  font-size: 14px;
  line-height: 1.5;
}

.alert--error {
  background: rgba(229, 57, 53, 0.1);
  border: 1px solid rgba(229, 57, 53, 0.3);
  color: var(--color-accent-red);
}

.alert svg {
  flex-shrink: 0;
}

.btn {
  padding: var(--space-3) var(--space-5);
  border-radius: var(--radius-md);
  font-weight: 600;
  font-size: 15px;
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: var(--space-2);
  transition: all 0.2s ease;
  border: none;
  cursor: pointer;
}

.btn--large {
  padding: var(--space-4) var(--space-5);
  width: 100%;
}

.btn--primary {
  background: var(--color-primary-teal);
  color: white;
  box-shadow: 0 4px 12px rgba(0, 137, 123, 0.3);
}

.btn--primary:hover:not(:disabled) {
  background: #00a589;
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(0, 137, 123, 0.4);
}

.btn--primary:disabled {
  background: var(--color-border-subtle);
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.btn-loading {
  display: flex;
  align-items: center;
  gap: var(--space-2);
}

.spinner {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.auth-card__footer {
  margin-top: var(--space-5);
  padding-top: var(--space-5);
  border-top: 1px solid var(--color-border-subtle);
  text-align: center;
}

.auth-card__footer-text {
  font-size: 14px;
  color: var(--color-text-secondary);
  margin: 0;
}

.auth-card__footer-link {
  color: var(--color-primary-teal);
  text-decoration: none;
  font-weight: 600;
  transition: color 0.2s ease;
}

.auth-card__footer-link:hover {
  color: var(--color-secondary-green);
  text-decoration: underline;
}

.auth-page__info {
  display: flex;
  justify-content: center;
  gap: var(--space-5);
  margin-top: var(--space-5);
  flex-wrap: wrap;
}

.info-item {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  font-size: 13px;
  color: var(--color-text-secondary);
}

.info-item svg {
  color: var(--color-primary-teal);
  flex-shrink: 0;
}

.fade-enter-active,
.fade-leave-active {
  transition: all 0.3s ease;
}

.fade-enter-from {
  opacity: 0;
  transform: translateY(-10px);
}

.fade-leave-to {
  opacity: 0;
  transform: translateY(10px);
}

@media (max-width: 640px) {
  .auth-card {
    padding: var(--space-5);
  }
  
  .auth-card__title {
    font-size: 24px;
  }
  
  .auth-page__info {
    flex-direction: column;
    align-items: center;
    gap: var(--space-3);
  }
  
  .form-options {
    flex-direction: column;
    align-items: flex-start;
    gap: var(--space-3);
  }
}
</style>
