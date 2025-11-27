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
              <circle cx="24" cy="24" r="20" stroke="var(--color-secondary-green)" stroke-width="2" opacity="0.3"/>
              <circle cx="24" cy="24" r="14" stroke="var(--color-secondary-green)" stroke-width="2"/>
              <circle cx="24" cy="24" r="8" fill="var(--color-secondary-green)"/>
              <path d="M24 4 L24 10" stroke="var(--color-primary-teal)" stroke-width="2" stroke-linecap="round"/>
              <path d="M24 38 L24 44" stroke="var(--color-primary-teal)" stroke-width="2" stroke-linecap="round"/>
              <path d="M4 24 L10 24" stroke="var(--color-primary-teal)" stroke-width="2" stroke-linecap="round"/>
              <path d="M38 24 L44 24" stroke="var(--color-primary-teal)" stroke-width="2" stroke-linecap="round"/>
            </svg>
          </div>
          <h1 class="auth-card__title">Create your account</h1>
          <p class="auth-card__subtitle">Join our platform and start monitoring air quality</p>
        </div>

        <!-- Register Form -->
        <form @submit.prevent="handleRegister" class="auth-form">
          <!-- Name Input -->
          <div class="form-group">
            <label for="name" class="form-label">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
                <circle cx="12" cy="7" r="4"/>
              </svg>
              Full name
            </label>
            <input
              id="name"
              v-model="name"
              type="text"
              class="form-input"
              placeholder="John Doe"
              required
              autocomplete="name"
            />
          </div>

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
                placeholder="Minimum 6 characters"
                required
                minlength="6"
                autocomplete="new-password"
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
            <div class="password-strength">
              <div class="password-strength-bar" :class="passwordStrengthClass"></div>
            </div>
            <p class="form-hint">Must be at least 6 characters long</p>
          </div>

          <!-- Role Selection -->
          <div class="form-group">
            <label class="form-label">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/>
                <circle cx="9" cy="7" r="4"/>
                <path d="M23 21v-2a4 4 0 0 0-3-3.87"/>
                <path d="M16 3.13a4 4 0 0 1 0 7.75"/>
              </svg>
              I am a
            </label>
            <div class="role-selector">
              <label class="role-option" :class="{ 'role-option--active': selectedRole === 1 }">
                <input type="radio" v-model="selectedRole" :value="1" class="role-radio" />
                <div class="role-content">
                  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
                    <circle cx="12" cy="7" r="4"/>
                  </svg>
                  <div>
                    <span class="role-title">Citizen</span>
                    <span class="role-desc">Monitor air quality in my city</span>
                  </div>
                </div>
              </label>

              <label class="role-option" :class="{ 'role-option--active': selectedRole === 2 }">
                <input type="radio" v-model="selectedRole" :value="2" class="role-radio" />
                <div class="role-content">
                  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/>
                    <polyline points="3.27 6.96 12 12.01 20.73 6.96"/>
                    <line x1="12" y1="22.08" x2="12" y2="12"/>
                  </svg>
                  <div>
                    <span class="role-title">Researcher</span>
                    <span class="role-desc">Analyze historical data</span>
                  </div>
                </div>
              </label>
            </div>
          </div>

          <!-- Terms and Privacy -->
          <div class="form-group">
            <label class="checkbox-label">
              <input type="checkbox" class="checkbox-input" required />
              <span>
                I agree to the
                <a href="#" class="inline-link">Terms of Service</a>
                and
                <a href="#" class="inline-link">Privacy Policy</a>
              </span>
            </label>
          </div>

          <!-- Success Message -->
          <transition name="fade">
            <div v-if="success" class="alert alert--success">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/>
                <polyline points="22 4 12 14.01 9 11.01"/>
              </svg>
              {{ success }}
            </div>
          </transition>

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
            <span v-if="!loading">Create account</span>
            <span v-else class="btn-loading">
              <svg class="spinner" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="10"/>
              </svg>
              Creating account...
            </span>
          </button>
        </form>

        <!-- Footer -->
        <div class="auth-card__footer">
          <p class="auth-card__footer-text">
            Already have an account?
            <router-link to="/login" class="auth-card__footer-link">Sign in</router-link>
          </p>
        </div>
      </div>

      <!-- Additional Info -->
      <div class="auth-page__info">
        <div class="info-item">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <polyline points="20 6 9 17 4 12"/>
          </svg>
          <span>Free forever</span>
        </div>
        <div class="info-item">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
          </svg>
          <span>No credit card required</span>
        </div>
        <div class="info-item">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="10"/>
            <polyline points="12 6 12 12 16 14"/>
          </svg>
          <span>Setup in 2 minutes</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from "vue";
import { useRouter } from "vue-router";
import { register } from "@/services/authService";

const router = useRouter();
const name = ref("");
const email = ref("");
const password = ref("");
const showPassword = ref(false);
const selectedRole = ref(1); // Default to Citizen
const loading = ref(false);
const error = ref("");
const success = ref("");

const passwordStrengthClass = computed(() => {
  const len = password.value.length;
  if (len === 0) return '';
  if (len < 6) return 'password-strength-bar--weak';
  if (len < 10) return 'password-strength-bar--medium';
  return 'password-strength-bar--strong';
});

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
      role_id: selectedRole.value
    });

    console.log("✅ Registro exitoso:", response);
    success.value = "Account created successfully! Redirecting to login...";

    // Esperar 2 segundos para mostrar el mensaje de éxito
    setTimeout(() => {
      router.push("/login");
    }, 2000);

  } catch (err: any) {
    console.error("❌ Error en registro:", err);
    error.value = err.message || "Error creating account. Please try again.";
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
  background: radial-gradient(circle, rgba(67, 160, 71, 0.15) 0%, transparent 70%);
  animation: float 20s ease-in-out infinite;
}

.bg-circle--1 {
  width: 400px;
  height: 400px;
  top: -200px;
  right: -100px;
  animation-delay: 0s;
}

.bg-circle--2 {
  width: 300px;
  height: 300px;
  bottom: -150px;
  left: -50px;
  animation-delay: -7s;
}

.bg-circle--3 {
  width: 250px;
  height: 250px;
  top: 50%;
  right: 20%;
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
  max-width: 520px;
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
  color: var(--color-secondary-green);
  gap: var(--space-3);
}

.auth-card {
  background: var(--color-bg-surface);
  border: 1px solid var(--color-border-subtle);
  border-radius: var(--radius-lg);
  padding: var(--space-6);
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.4);
  width: 100%;
  max-width: 520px;
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
  border-color: var(--color-secondary-green);
  background: rgba(67, 160, 71, 0.05);
  box-shadow: 0 0 0 3px rgba(67, 160, 71, 0.1);
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
  color: var(--color-secondary-green);
  background: rgba(67, 160, 71, 0.1);
}

.password-strength {
  height: 4px;
  background: rgba(0, 0, 0, 0.2);
  border-radius: 2px;
  overflow: hidden;
  margin-top: -var(--space-1);
}

.password-strength-bar {
  height: 100%;
  width: 0;
  transition: all 0.3s ease;
  border-radius: 2px;
}

.password-strength-bar--weak {
  width: 33%;
  background: var(--color-accent-red);
}

.password-strength-bar--medium {
  width: 66%;
  background: var(--color-accent-amber);
}

.password-strength-bar--strong {
  width: 100%;
  background: var(--color-secondary-green);
}

.form-hint {
  font-size: 13px;
  color: var(--color-text-secondary);
  margin: -var(--space-1) 0 0;
}

.role-selector {
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
}

.role-option {
  cursor: pointer;
  border: 2px solid var(--color-border-subtle);
  background: rgba(0, 0, 0, 0.2);
  border-radius: var(--radius-md);
  padding: var(--space-4);
  transition: all 0.2s ease;
  position: relative;
}

.role-option:hover {
  border-color: var(--color-secondary-green);
  background: rgba(67, 160, 71, 0.05);
}

.role-option--active {
  border-color: var(--color-secondary-green);
  background: rgba(67, 160, 71, 0.1);
}

.role-option--active::after {
  content: '';
  position: absolute;
  top: var(--space-3);
  right: var(--space-3);
  width: 20px;
  height: 20px;
  background: var(--color-secondary-green);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.role-option--active::before {
  content: '✓';
  position: absolute;
  top: var(--space-3);
  right: var(--space-3);
  width: 20px;
  height: 20px;
  color: white;
  font-size: 12px;
  font-weight: bold;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1;
}

.role-radio {
  position: absolute;
  opacity: 0;
}

.role-content {
  display: flex;
  align-items: center;
  gap: var(--space-3);
}

.role-content svg {
  color: var(--color-secondary-green);
  flex-shrink: 0;
}

.role-title {
  display: block;
  font-weight: 600;
  color: var(--color-text-primary);
  font-size: 15px;
  margin-bottom: 2px;
}

.role-desc {
  display: block;
  font-size: 13px;
  color: var(--color-text-secondary);
}

.checkbox-label {
  display: flex;
  align-items: flex-start;
  gap: var(--space-2);
  font-size: 14px;
  color: var(--color-text-secondary);
  cursor: pointer;
  line-height: 1.5;
}

.checkbox-input {
  width: 18px;
  height: 18px;
  cursor: pointer;
  accent-color: var(--color-secondary-green);
  margin-top: 2px;
  flex-shrink: 0;
}

.inline-link {
  color: var(--color-secondary-green);
  text-decoration: none;
  font-weight: 500;
}

.inline-link:hover {
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

.alert--success {
  background: rgba(67, 160, 71, 0.1);
  border: 1px solid rgba(67, 160, 71, 0.3);
  color: var(--color-secondary-green);
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
  background: var(--color-secondary-green);
  color: white;
  box-shadow: 0 4px 12px rgba(67, 160, 71, 0.3);
}

.btn--primary:hover:not(:disabled) {
  background: #4caf50;
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(67, 160, 71, 0.4);
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
  color: var(--color-secondary-green);
  text-decoration: none;
  font-weight: 600;
  transition: color 0.2s ease;
}

.auth-card__footer-link:hover {
  color: #4caf50;
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
  color: var(--color-secondary-green);
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
}
</style>
