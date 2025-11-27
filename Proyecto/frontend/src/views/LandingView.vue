<template>
  <main class="landing">
    <LandingHeroSection />
    <LandingRolesSection />
    <LandingHowItWorksSection />
    <LandingInsightsSection />
  </main>
</template>

<script setup lang="ts">
import LandingHeroSection from '../components/sections/LandingHeroSection.vue'
import LandingRolesSection from '../components/sections/LandingRolesSection.vue'
import LandingHowItWorksSection from '../components/sections/LandingHowItWorksSection.vue'
import LandingInsightsSection from '../components/sections/LandingInsightsSection.vue'
</script>

<style scoped>
.landing {
  display: flex;
  flex-direction: column;
  gap: var(--space-6);
}
</style>
