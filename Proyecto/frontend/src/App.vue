<template>
  <div class="app-shell">
    <AppNavbar />
    <RouterView />
    <AppFooter />
  </div>
</template>

<script setup lang="ts">
import { RouterView } from 'vue-router'
import AppNavbar from './components/layout/AppNavbar.vue'
import AppFooter from './components/layout/AppFooter.vue'
</script>

<style>
.app-shell {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}
</style>
