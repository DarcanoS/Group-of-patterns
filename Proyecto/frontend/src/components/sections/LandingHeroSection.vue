<template>
  <section class="hero">
    <div class="hero__content">
      <span class="hero__label">Calidad de aire en vivo</span>

      <h1 class="hero__title">
        Monitoreo de calidad de aire en la ciudad.
      </h1>

      <p class="hero__text">
        Air Quality Platform brinda lecturas en tiempo real de los niveles de polucion del aire .
      </p>

      <div class="hero__actions">
        <router-link to="/login" class="btn btn--primary">
          ingresar 
        </router-link>

        <a href="#" class="hero__link">Explorar</a>
      </div>
    </div>

    <div class="hero__card">
      <h3>Hoy en Bogotá</h3>

      <div class="hero__aqi">
        <strong>AQI 58</strong>
        <span class="badge badge--amber">Moderado</span>
      </div>

      <ul class="hero__pollutants">
        <li>PM2.5: 18 µg/m³</li>
        <li>PM10: 42 µg/m³</li>
        <li>O₃: 31 ppb</li>
      </ul>

      <div class="hero__chart">
        <div class="chart-placeholder">AQI Chart (mock)</div>
      </div>
    </div>
  </section>
</template>

<style scoped>
.hero {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--space-6);
  padding: var(--space-6);
}

.hero__label {
  color: var(--color-secondary-green);
  font-size: 14px;
}

.hero__title {
  font-size: 40px;
  margin: var(--space-3) 0;
}

.hero__text {
  color: var(--color-text-secondary);
  max-width: 520px;
}

.hero__actions {
  margin-top: var(--space-4);
  display: flex;
  gap: var(--space-4);
}

.btn {
  padding: var(--space-3) var(--space-5);
  border-radius: var(--radius-md);
}

.btn--primary {
  background: var(--color-primary-teal);
  color: white;
}

.hero__link {
  align-self: center;
  color: var(--color-text-secondary);
  text-decoration: underline;
}

.hero__card {
  background: var(--color-bg-surface);
  border-radius: var(--radius-lg);
  padding: var(--space-5);
  border: 1px solid var(--color-border-subtle);
}

.hero__aqi {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  margin: var(--space-3) 0;
}

.badge {
  padding: 4px 10px;
  border-radius: 999px;
  font-size: 12px;
}

.badge--amber {
  background: var(--color-accent-amber);
  color: black;
}

.hero__pollutants {
  list-style: none;
  padding: 0;
  color: var(--color-text-secondary);
}

.chart-placeholder {
  margin-top: var(--space-4);
  height: 120px;
  background: #1c2333;
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--color-text-secondary);
}
</style>
