<template>
  <section class="how-section">
    <div class="container">
      <div class="section-header">
        <h2 class="section-title">How the platform works</h2>
        <p class="section-subtitle">
          A seamless data pipeline from sensors to insights
        </p>
      </div>

      <div class="steps-container">
        <div class="step">
          <div class="step__number">01</div>
          <div class="step__icon">
            <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/>
              <polyline points="7.5 4.21 12 6.81 16.5 4.21"/>
              <polyline points="7.5 19.79 7.5 14.6 3 12"/>
              <polyline points="21 12 16.5 14.6 16.5 19.79"/>
              <polyline points="3.27 6.96 12 12.01 20.73 6.96"/>
              <line x1="12" y1="22.08" x2="12" y2="12"/>
            </svg>
          </div>
          <h3 class="step__title">Ingest</h3>
          <p class="step__description">
            We connect to external air quality APIs and validate incoming data from monitoring stations.
          </p>
          <div class="step__tech">
            <span>Python</span>
            <span>FastAPI</span>
            <span>Adapters</span>
          </div>
        </div>

        <div class="step-connector">
          <svg width="100%" height="40" viewBox="0 0 100 40" preserveAspectRatio="none">
            <defs>
              <linearGradient id="arrowGradient1" x1="0%" y1="0%" x2="100%" y2="0%">
                <stop offset="0%" style="stop-color:var(--color-primary-teal);stop-opacity:0.3" />
                <stop offset="100%" style="stop-color:var(--color-primary-teal);stop-opacity:1" />
              </linearGradient>
            </defs>
            <path d="M0,20 L80,20" stroke="url(#arrowGradient1)" stroke-width="2" fill="none" stroke-dasharray="4 4"/>
            <polygon points="85,20 75,15 75,25" fill="var(--color-primary-teal)"/>
          </svg>
        </div>

        <div class="step">
          <div class="step__number">02</div>
          <div class="step__icon">
            <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/>
            </svg>
          </div>
          <h3 class="step__title">Transform</h3>
          <p class="step__description">
            We normalize readings and compute daily statistics for each station and pollutant.
          </p>
          <div class="step__tech">
            <span>PostgreSQL</span>
            <span>PostGIS</span>
            <span>Analytics</span>
          </div>
        </div>

        <div class="step-connector">
          <svg width="100%" height="40" viewBox="0 0 100 40" preserveAspectRatio="none">
            <defs>
              <linearGradient id="arrowGradient2" x1="0%" y1="0%" x2="100%" y2="0%">
                <stop offset="0%" style="stop-color:var(--color-primary-teal);stop-opacity:0.3" />
                <stop offset="100%" style="stop-color:var(--color-primary-teal);stop-opacity:1" />
              </linearGradient>
            </defs>
            <path d="M0,20 L80,20" stroke="url(#arrowGradient2)" stroke-width="2" fill="none" stroke-dasharray="4 4"/>
            <polygon points="85,20 75,15 75,25" fill="var(--color-primary-teal)"/>
          </svg>
        </div>

        <div class="step">
          <div class="step__number">03</div>
          <div class="step__icon">
            <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <rect x="2" y="3" width="20" height="14" rx="2" ry="2"/>
              <line x1="8" y1="21" x2="16" y2="21"/>
              <line x1="12" y1="17" x2="12" y2="21"/>
            </svg>
          </div>
          <h3 class="step__title">Deliver</h3>
          <p class="step__description">
            Dashboards and APIs make the data accessible for citizens, researchers and experts.
          </p>
          <div class="step__tech">
            <span>Vue 3</span>
            <span>REST API</span>
            <span>Charts</span>
          </div>
        </div>
      </div>

      <div class="architecture-note">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <circle cx="12" cy="12" r="10"/>
          <line x1="12" y1="16" x2="12" y2="12"/>
          <line x1="12" y1="8" x2="12.01" y2="8"/>
        </svg>
        <span>Built with design patterns: Factory, Strategy, Adapter, Builder & Prototype</span>
      </div>
    </div>
  </section>
</template>

<style scoped>
.how-section {
  padding: calc(var(--space-6) * 2) var(--space-5);
  background: linear-gradient(180deg, var(--color-bg-app) 0%, rgba(18, 24, 38, 0.8) 100%);
}

.container {
  max-width: 1400px;
  margin: 0 auto;
}

.section-header {
  text-align: center;
  margin-bottom: calc(var(--space-6) * 2);
}

.section-title {
  font-size: 40px;
  font-weight: 700;
  margin-bottom: var(--space-3);
  color: var(--color-text-primary);
}

.section-subtitle {
  font-size: 18px;
  color: var(--color-text-secondary);
}

.steps-container {
  display: grid;
  grid-template-columns: 1fr auto 1fr auto 1fr;
  gap: var(--space-4);
  align-items: center;
  margin-bottom: var(--space-6);
}

.step {
  background: var(--color-bg-surface);
  border: 1px solid var(--color-border-subtle);
  border-radius: var(--radius-lg);
  padding: var(--space-5);
  text-align: center;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.step::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, var(--color-primary-teal) 0%, var(--color-secondary-green) 100%);
  opacity: 0;
  transition: opacity 0.3s ease;
}

.step:hover::before {
  opacity: 1;
}

.step:hover {
  transform: translateY(-8px);
  box-shadow: 0 16px 48px rgba(0, 137, 123, 0.2);
  border-color: var(--color-primary-teal);
}

.step__number {
  position: absolute;
  top: var(--space-3);
  right: var(--space-3);
  font-size: 48px;
  font-weight: 800;
  color: rgba(0, 137, 123, 0.1);
  line-height: 1;
}

.step__icon {
  width: 80px;
  height: 80px;
  margin: 0 auto var(--space-4);
  background: rgba(0, 137, 123, 0.1);
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--color-primary-teal);
}

.step__title {
  font-size: 24px;
  font-weight: 700;
  margin-bottom: var(--space-3);
  color: var(--color-text-primary);
}

.step__description {
  color: var(--color-text-secondary);
  line-height: 1.6;
  margin-bottom: var(--space-4);
  min-height: 60px;
}

.step__tech {
  display: flex;
  gap: var(--space-2);
  justify-content: center;
  flex-wrap: wrap;
}

.step__tech span {
  background: rgba(0, 137, 123, 0.1);
  color: var(--color-primary-teal);
  padding: 4px 12px;
  border-radius: 999px;
  font-size: 12px;
  font-weight: 600;
  border: 1px solid rgba(0, 137, 123, 0.2);
}

.step-connector {
  width: 100px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.architecture-note {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--space-3);
  padding: var(--space-4);
  background: rgba(0, 137, 123, 0.05);
  border: 1px solid rgba(0, 137, 123, 0.2);
  border-radius: var(--radius-md);
  color: var(--color-text-secondary);
  font-size: 14px;
  margin-top: var(--space-6);
}

.architecture-note svg {
  color: var(--color-primary-teal);
  flex-shrink: 0;
}

@media (max-width: 1200px) {
  .steps-container {
    grid-template-columns: 1fr;
    gap: var(--space-5);
  }
  
  .step-connector {
    width: 100%;
    height: 60px;
  }
  
  .step-connector svg {
    transform: rotate(90deg);
  }
}

@media (max-width: 768px) {
  .section-title {
    font-size: 32px;
  }
  
  .step__description {
    min-height: auto;
  }
}
</style>
