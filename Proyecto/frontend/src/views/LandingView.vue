<template>
  <main class="landing">
    <LandingHeroSection />
    <LandingRolesSection />
    <LandingHowItWorksSection />
    <LandingApiSection />
    <LandingInsightsSection />
  </main>
</template>

<script setup lang="ts">
import LandingHeroSection from '../components/sections/LandingHeroSection.vue'
import LandingRolesSection from '../components/sections/LandingRolesSection.vue'
import LandingHowItWorksSection from '../components/sections/LandingHowItWorksSection.vue'
import LandingApiSection from '../components/sections/LandingApiSection.vue'
import LandingInsightsSection from '../components/sections/LandingInsightsSection.vue'
</script>

<style scoped>
.landing {
  display: flex;
  flex-direction: column;
}
</style>
