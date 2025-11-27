<template>
  <section id="features" class="roles-section">
    <div class="container">
      <div class="section-header">
        <h2 class="section-title">Designed for everyone who cares about air quality</h2>
        <p class="section-subtitle">
          Whether you're a concerned citizen, a data researcher, or managing a city's air quality network, 
          we provide the tools you need.
        </p>
      </div>

      <div class="roles-grid">
        <div class="role-card">
          <div class="role-card__icon role-card__icon--citizen">
            <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
              <circle cx="12" cy="7" r="4"/>
            </svg>
          </div>
          <h3 class="role-card__title">Citizen</h3>
          <p class="role-card__description">
            Check current AQI, understand what it means and receive simple health recommendations.
          </p>
          <ul class="role-card__features">
            <li>
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="20 6 9 17 4 12"/>
              </svg>
              Current air quality in your city
            </li>
            <li>
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="20 6 9 17 4 12"/>
              </svg>
              Clear health guidance
            </li>
            <li>
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="20 6 9 17 4 12"/>
              </svg>
              Basic product suggestions
            </li>
          </ul>
        </div>

        <div class="role-card role-card--featured">
          <div class="role-card__badge">Most Popular</div>
          <div class="role-card__icon role-card__icon--researcher">
            <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/>
              <polyline points="3.27 6.96 12 12.01 20.73 6.96"/>
              <line x1="12" y1="22.08" x2="12" y2="12"/>
            </svg>
          </div>
          <h3 class="role-card__title">Researcher</h3>
          <p class="role-card__description">
            Explore historical trends and export clean datasets for analysis.
          </p>
          <ul class="role-card__features">
            <li>
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="20 6 9 17 4 12"/>
              </svg>
              Daily statistics and trends
            </li>
            <li>
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="20 6 9 17 4 12"/>
              </svg>
              Filter by station and pollutant
            </li>
            <li>
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="20 6 9 17 4 12"/>
              </svg>
              Export CSV datasets
            </li>
          </ul>
        </div>

        <div class="role-card">
          <div class="role-card__icon role-card__icon--admin">
            <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <rect x="3" y="3" width="18" height="18" rx="2" ry="2"/>
              <line x1="9" y1="9" x2="15" y2="9"/>
              <line x1="9" y1="15" x2="15" y2="15"/>
            </svg>
          </div>
          <h3 class="role-card__title">Admin</h3>
          <p class="role-card__description">
            Manage stations, roles and alert thresholds across your network.
          </p>
          <ul class="role-card__features">
            <li>
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="20 6 9 17 4 12"/>
              </svg>
              Manage stations and coverage
            </li>
            <li>
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="20 6 9 17 4 12"/>
              </svg>
              Control user roles and permissions
            </li>
            <li>
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="20 6 9 17 4 12"/>
              </svg>
              Configure alert thresholds
            </li>
          </ul>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
.roles-section {
  padding: calc(var(--space-6) * 2) var(--space-5);
  background: var(--color-bg-app);
}

.container {
  max-width: 1400px;
  margin: 0 auto;
}

.section-header {
  text-align: center;
  margin-bottom: calc(var(--space-6) * 1.5);
}

.section-title {
  font-size: 40px;
  font-weight: 700;
  margin-bottom: var(--space-4);
  color: var(--color-text-primary);
}

.section-subtitle {
  font-size: 18px;
  color: var(--color-text-secondary);
  max-width: 720px;
  margin: 0 auto;
  line-height: 1.6;
}

.roles-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: var(--space-5);
}

.role-card {
  background: var(--color-bg-surface);
  border: 1px solid var(--color-border-subtle);
  border-radius: var(--radius-lg);
  padding: var(--space-5);
  transition: all 0.3s ease;
  position: relative;
}

.role-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 12px 40px rgba(0, 137, 123, 0.15);
  border-color: var(--color-primary-teal);
}

.role-card--featured {
  border: 2px solid var(--color-primary-teal);
  background: linear-gradient(135deg, var(--color-bg-surface) 0%, rgba(0, 137, 123, 0.05) 100%);
}

.role-card__badge {
  position: absolute;
  top: -12px;
  right: var(--space-4);
  background: var(--color-primary-teal);
  color: white;
  padding: 4px 12px;
  border-radius: 999px;
  font-size: 12px;
  font-weight: 600;
}

.role-card__icon {
  width: 64px;
  height: 64px;
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: var(--space-4);
}

.role-card__icon--citizen {
  background: rgba(67, 160, 71, 0.1);
  color: var(--color-secondary-green);
}

.role-card__icon--researcher {
  background: rgba(0, 137, 123, 0.1);
  color: var(--color-primary-teal);
}

.role-card__icon--admin {
  background: rgba(30, 136, 229, 0.1);
  color: var(--color-info-blue);
}

.role-card__title {
  font-size: 24px;
  font-weight: 700;
  margin-bottom: var(--space-3);
  color: var(--color-text-primary);
}

.role-card__description {
  color: var(--color-text-secondary);
  margin-bottom: var(--space-4);
  line-height: 1.6;
}

.role-card__features {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
}

.role-card__features li {
  display: flex;
  align-items: flex-start;
  gap: var(--space-2);
  color: var(--color-text-secondary);
  font-size: 14px;
  line-height: 1.5;
}

.role-card__features li svg {
  flex-shrink: 0;
  margin-top: 2px;
  color: var(--color-primary-teal);
}

@media (max-width: 768px) {
  .section-title {
    font-size: 32px;
  }
  
  .roles-grid {
    grid-template-columns: 1fr;
  }
}
</style>
