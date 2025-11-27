<template>
  <nav class="navbar">
    <div class="navbar__container">
      <!-- Logo and Brand -->
      <router-link to="/" class="navbar__brand">
        <div class="navbar__logo">
          <svg width="36" height="36" viewBox="0 0 48 48" fill="none">
            <circle cx="24" cy="24" r="20" stroke="var(--color-primary-teal)" stroke-width="2" opacity="0.3"/>
            <circle cx="24" cy="24" r="14" stroke="var(--color-primary-teal)" stroke-width="2"/>
            <circle cx="24" cy="24" r="8" fill="var(--color-primary-teal)"/>
            <path d="M24 4 L24 10" stroke="var(--color-secondary-green)" stroke-width="2" stroke-linecap="round"/>
            <path d="M24 38 L24 44" stroke="var(--color-secondary-green)" stroke-width="2" stroke-linecap="round"/>
            <path d="M4 24 L10 24" stroke="var(--color-secondary-green)" stroke-width="2" stroke-linecap="round"/>
            <path d="M38 24 L44 24" stroke="var(--color-secondary-green)" stroke-width="2" stroke-linecap="round"/>
          </svg>
        </div>
        <span class="navbar__title">Air Quality Platform</span>
      </router-link>

      <!-- Desktop Navigation -->
      <div class="navbar__nav">
        <a href="#overview" class="navbar__link">Overview</a>
        <a href="#features" class="navbar__link">Features</a>
        <a href="#api" class="navbar__link">API</a>
        <a href="#docs" class="navbar__link">Docs</a>
      </div>

      <!-- Actions -->
      <div class="navbar__actions">
        <router-link to="/login" class="navbar__button navbar__button--secondary">
          Sign up
        </router-link>
        <router-link to="/login" class="navbar__button navbar__button--primary">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M15 3h4a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2h-4"/>
            <polyline points="10 17 15 12 10 7"/>
            <line x1="15" y1="12" x2="3" y2="12"/>
          </svg>
          Sign in
        </router-link>
      </div>

      <!-- Mobile Menu Button -->
      <button class="navbar__mobile-toggle" @click="toggleMobileMenu" aria-label="Toggle menu">
        <svg v-if="!isMobileMenuOpen" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <line x1="3" y1="12" x2="21" y2="12"/>
          <line x1="3" y1="6" x2="21" y2="6"/>
          <line x1="3" y1="18" x2="21" y2="18"/>
        </svg>
        <svg v-else width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <line x1="18" y1="6" x2="6" y2="18"/>
          <line x1="6" y1="6" x2="18" y2="18"/>
        </svg>
      </button>
    </div>

    <!-- Mobile Menu -->
    <transition name="mobile-menu">
      <div v-if="isMobileMenuOpen" class="navbar__mobile-menu">
        <a href="#overview" class="navbar__mobile-link" @click="closeMobileMenu">Overview</a>
        <a href="#features" class="navbar__mobile-link" @click="closeMobileMenu">Features</a>
        <a href="#api" class="navbar__mobile-link" @click="closeMobileMenu">API</a>
        <a href="#docs" class="navbar__mobile-link" @click="closeMobileMenu">Docs</a>
        <div class="navbar__mobile-actions">
          <router-link to="/login" class="navbar__button navbar__button--secondary navbar__button--block">
            Sign up
          </router-link>
          <router-link to="/login" class="navbar__button navbar__button--primary navbar__button--block">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M15 3h4a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2h-4"/>
              <polyline points="10 17 15 12 10 7"/>
              <line x1="15" y1="12" x2="3" y2="12"/>
            </svg>
            Sign in
          </router-link>
        </div>
      </div>
    </transition>
  </nav>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const isMobileMenuOpen = ref(false)

const toggleMobileMenu = () => {
  isMobileMenuOpen.value = !isMobileMenuOpen.value
}

const closeMobileMenu = () => {
  isMobileMenuOpen.value = false
}
</script>

<style scoped>
.navbar {
  background: var(--color-bg-surface);
  border-bottom: 1px solid var(--color-border-subtle);
  position: sticky;
  top: 0;
  z-index: 100;
  backdrop-filter: blur(10px);
  background: rgba(18, 24, 38, 0.95);
}

.navbar__container {
  max-width: 1400px;
  margin: 0 auto;
  padding: var(--space-4) var(--space-5);
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--space-4);
}

.navbar__brand {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  text-decoration: none;
  transition: transform 0.2s ease;
}

.navbar__brand:hover {
  transform: scale(1.02);
}

.navbar__logo {
  display: flex;
  align-items: center;
  justify-content: center;
}

.navbar__title {
  font-size: 20px;
  font-weight: 700;
  color: var(--color-text-primary);
  background: linear-gradient(135deg, var(--color-text-primary) 0%, var(--color-primary-teal) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.navbar__nav {
  display: none;
  gap: var(--space-1);
}

@media (min-width: 768px) {
  .navbar__nav {
    display: flex;
  }
}

.navbar__link {
  padding: var(--space-2) var(--space-3);
  color: var(--color-text-secondary);
  text-decoration: none;
  font-weight: 500;
  font-size: 15px;
  border-radius: var(--radius-md);
  transition: all 0.2s ease;
  position: relative;
}

.navbar__link:hover {
  color: var(--color-text-primary);
  background: rgba(0, 137, 123, 0.1);
}

.navbar__link::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%) scaleX(0);
  width: 80%;
  height: 2px;
  background: var(--color-primary-teal);
  transition: transform 0.2s ease;
}

.navbar__link:hover::after {
  transform: translateX(-50%) scaleX(1);
}

.navbar__actions {
  display: none;
  gap: var(--space-2);
}

@media (min-width: 768px) {
  .navbar__actions {
    display: flex;
  }
}

.navbar__button {
  padding: var(--space-2) var(--space-4);
  border-radius: var(--radius-md);
  font-weight: 600;
  font-size: 14px;
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  gap: var(--space-2);
  transition: all 0.2s ease;
  border: none;
  cursor: pointer;
  white-space: nowrap;
}

.navbar__button--secondary {
  background: transparent;
  color: var(--color-text-secondary);
  border: 1px solid var(--color-border-subtle);
}

.navbar__button--secondary:hover {
  color: var(--color-text-primary);
  border-color: var(--color-primary-teal);
  background: rgba(0, 137, 123, 0.05);
}

.navbar__button--primary {
  background: var(--color-primary-teal);
  color: white;
  box-shadow: 0 2px 8px rgba(0, 137, 123, 0.3);
}

.navbar__button--primary:hover {
  background: #00a589;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 137, 123, 0.4);
}

.navbar__button--block {
  width: 100%;
  justify-content: center;
}

.navbar__mobile-toggle {
  display: flex;
  align-items: center;
  justify-content: center;
  background: transparent;
  border: none;
  color: var(--color-text-primary);
  cursor: pointer;
  padding: var(--space-2);
  border-radius: var(--radius-md);
  transition: all 0.2s ease;
}

.navbar__mobile-toggle:hover {
  background: rgba(0, 137, 123, 0.1);
}

@media (min-width: 768px) {
  .navbar__mobile-toggle {
    display: none;
  }
}

.navbar__mobile-menu {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
  padding: var(--space-4) var(--space-5);
  border-top: 1px solid var(--color-border-subtle);
  background: var(--color-bg-app);
}

@media (min-width: 768px) {
  .navbar__mobile-menu {
    display: none;
  }
}

.navbar__mobile-link {
  padding: var(--space-3);
  color: var(--color-text-secondary);
  text-decoration: none;
  font-weight: 500;
  font-size: 16px;
  border-radius: var(--radius-md);
  transition: all 0.2s ease;
}

.navbar__mobile-link:hover {
  color: var(--color-text-primary);
  background: rgba(0, 137, 123, 0.1);
  padding-left: var(--space-4);
}

.navbar__mobile-actions {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
  margin-top: var(--space-4);
  padding-top: var(--space-4);
  border-top: 1px solid var(--color-border-subtle);
}

/* Mobile menu transitions */
.mobile-menu-enter-active,
.mobile-menu-leave-active {
  transition: all 0.3s ease;
}

.mobile-menu-enter-from {
  opacity: 0;
  transform: translateY(-10px);
}

.mobile-menu-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}
</style>
