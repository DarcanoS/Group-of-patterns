<template>
  <section class="hero">
    <div class="hero__content">
      <span class="hero__label">
        <svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor" style="display: inline; vertical-align: text-bottom; margin-right: 6px">
          <circle cx="8" cy="8" r="4"/>
          <circle cx="8" cy="8" r="6" opacity="0.3"/>
        </svg>
        Live air quality, made understandable
      </span>

      <h1 class="hero__title">
        Monitor, understand and act on air quality in your city
      </h1>

      <p class="hero__text">
        Air Quality Platform brings together real-time readings, daily statistics and simple health recommendations for citizens, researchers and city teams.
      </p>

      <div class="hero__actions">
        <router-link to="/login" class="btn btn--primary">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="vertical-align: text-bottom; margin-right: 8px">
            <path d="M15 3h4a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2h-4"/>
            <polyline points="10 17 15 12 10 7"/>
            <line x1="15" y1="12" x2="3" y2="12"/>
          </svg>
          Sign in to dashboard
        </router-link>

        <a href="#features" class="hero__link">
          Explore features
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="vertical-align: text-bottom; margin-left: 4px">
            <polyline points="6 9 12 15 18 9"/>
          </svg>
        </a>
      </div>

      <div class="hero__stats">
        <div class="stat">
          <div class="stat__value">50+</div>
          <div class="stat__label">Active Stations</div>
        </div>
        <div class="stat">
          <div class="stat__value">24/7</div>
          <div class="stat__label">Real-time Monitoring</div>
        </div>
        <div class="stat">
          <div class="stat__value">5</div>
          <div class="stat__label">Key Pollutants</div>
        </div>
      </div>
    </div>

    <div class="hero__card">
      <div class="card-header">
        <h3>Today in Bogotá</h3>
        <span class="card-live">
          <span class="pulse"></span>
          Live
        </span>
      </div>

      <div class="hero__aqi">
        <div class="aqi-value">
          <span class="aqi-number">58</span>
          <span class="aqi-label">AQI</span>
        </div>
        <span class="badge badge--amber">Moderate</span>
      </div>

      <ul class="hero__pollutants">
        <li>
          <span class="pollutant-name">PM2.5</span>
          <span class="pollutant-value">18 µg/m³</span>
        </li>
        <li>
          <span class="pollutant-name">PM10</span>
          <span class="pollutant-value">42 µg/m³</span>
        </li>
        <li>
          <span class="pollutant-name">O₃</span>
          <span class="pollutant-value">31 ppb</span>
        </li>
      </ul>

      <div class="hero__chart">
        <svg width="100%" height="100" viewBox="0 0 300 80" preserveAspectRatio="none">
          <defs>
            <linearGradient id="chartGradient" x1="0%" y1="0%" x2="0%" y2="100%">
              <stop offset="0%" style="stop-color:var(--color-primary-teal);stop-opacity:0.3" />
              <stop offset="100%" style="stop-color:var(--color-primary-teal);stop-opacity:0" />
            </linearGradient>
          </defs>
          <path d="M0,60 L25,55 L50,50 L75,45 L100,40 L125,42 L150,44 L175,38 L200,40 L225,35 L250,38 L275,36 L300,40" 
                fill="url(#chartGradient)" stroke="none"/>
          <path d="M0,60 L25,55 L50,50 L75,45 L100,40 L125,42 L150,44 L175,38 L200,40 L225,35 L250,38 L275,36 L300,40" 
                fill="none" stroke="var(--color-primary-teal)" stroke-width="2"/>
        </svg>
        <div class="chart-label">Last 24 hours</div>
      </div>
    </div>
  </section>
</template>

<style scoped>
.hero {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--space-6);
  padding: var(--space-6) var(--space-6) calc(var(--space-6) * 2);
  max-width: 1400px;
  margin: 0 auto;
}

.hero__label {
  color: var(--color-secondary-green);
  font-size: 14px;
  font-weight: 600;
  letter-spacing: 0.5px;
  display: flex;
  align-items: center;
}

.hero__title {
  font-size: 48px;
  margin: var(--space-4) 0;
  line-height: 1.1;
  font-weight: 700;
  background: linear-gradient(135deg, var(--color-text-primary) 0%, var(--color-primary-teal) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.hero__text {
  color: var(--color-text-secondary);
  max-width: 540px;
  font-size: 18px;
  line-height: 1.6;
}

.hero__actions {
  margin-top: var(--space-5);
  display: flex;
  gap: var(--space-4);
  align-items: center;
}

.btn {
  padding: var(--space-3) var(--space-5);
  border-radius: var(--radius-md);
  font-weight: 600;
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  transition: all 0.2s ease;
  border: none;
  cursor: pointer;
}

.btn--primary {
  background: var(--color-primary-teal);
  color: white;
  box-shadow: 0 4px 12px rgba(0, 137, 123, 0.3);
}

.btn--primary:hover {
  background: #00a589;
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(0, 137, 123, 0.4);
}

.hero__link {
  color: var(--color-text-secondary);
  text-decoration: none;
  font-weight: 500;
  display: inline-flex;
  align-items: center;
  transition: color 0.2s ease;
}

.hero__link:hover {
  color: var(--color-primary-teal);
}

.hero__stats {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: var(--space-4);
  margin-top: var(--space-6);
  padding-top: var(--space-5);
  border-top: 1px solid var(--color-border-subtle);
}

.stat {
  text-align: left;
}

.stat__value {
  font-size: 32px;
  font-weight: 700;
  color: var(--color-primary-teal);
  margin-bottom: var(--space-1);
}

.stat__label {
  font-size: 13px;
  color: var(--color-text-secondary);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.hero__card {
  background: var(--color-bg-surface);
  border-radius: var(--radius-lg);
  padding: var(--space-5);
  border: 1px solid var(--color-border-subtle);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.hero__card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 48px rgba(0, 0, 0, 0.4);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--space-4);
}

.card-header h3 {
  margin: 0;
  font-size: 20px;
}

.card-live {
  display: flex;
  align-items: center;
  gap: 6px;
  color: var(--color-secondary-green);
  font-size: 13px;
  font-weight: 600;
}

.pulse {
  width: 8px;
  height: 8px;
  background: var(--color-secondary-green);
  border-radius: 50%;
  animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.5; transform: scale(1.2); }
}

.hero__aqi {
  display: flex;
  align-items: center;
  gap: var(--space-4);
  margin: var(--space-4) 0;
  padding: var(--space-4);
  background: rgba(255, 179, 0, 0.05);
  border-radius: var(--radius-md);
  border-left: 4px solid var(--color-accent-amber);
}

.aqi-value {
  display: flex;
  align-items: baseline;
  gap: var(--space-2);
}

.aqi-number {
  font-size: 48px;
  font-weight: 700;
  color: var(--color-text-primary);
}

.aqi-label {
  font-size: 14px;
  color: var(--color-text-secondary);
  font-weight: 500;
}

.badge {
  padding: 6px 14px;
  border-radius: 999px;
  font-size: 13px;
  font-weight: 600;
}

.badge--amber {
  background: var(--color-accent-amber);
  color: #1a1a1a;
}

.hero__pollutants {
  list-style: none;
  padding: 0;
  margin: var(--space-4) 0;
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.hero__pollutants li {
  display: flex;
  justify-content: space-between;
  padding: var(--space-2);
  background: rgba(255, 255, 255, 0.02);
  border-radius: var(--radius-sm);
}

.pollutant-name {
  color: var(--color-text-secondary);
  font-weight: 500;
}

.pollutant-value {
  color: var(--color-text-primary);
  font-weight: 600;
}

.hero__chart {
  margin-top: var(--space-4);
  padding: var(--space-3);
  background: rgba(0, 0, 0, 0.2);
  border-radius: var(--radius-md);
  border: 1px solid var(--color-border-subtle);
}

.chart-label {
  text-align: center;
  color: var(--color-text-secondary);
  font-size: 12px;
  margin-top: var(--space-2);
}

@media (max-width: 968px) {
  .hero {
    grid-template-columns: 1fr;
  }
  
  .hero__title {
    font-size: 36px;
  }
  
  .hero__stats {
    grid-template-columns: repeat(3, 1fr);
  }
}
</style>
