<template>
  <section class="api-section">
    <div class="container">
      <div class="section-header">
        <h2 class="section-title">Powerful REST API</h2>
        <p class="section-subtitle">
          Integrate air quality data into your applications with our comprehensive API
        </p>
      </div>

      <div class="api-grid">
        <div class="api-showcase">
          <div class="api-showcase__tabs">
            <button 
              v-for="endpoint in endpoints" 
              :key="endpoint.id"
              :class="['api-tab', { 'api-tab--active': activeEndpoint === endpoint.id }]"
              @click="activeEndpoint = endpoint.id"
            >
              <span class="api-tab__method" :class="`api-tab__method--${endpoint.method.toLowerCase()}`">
                {{ endpoint.method }}
              </span>
              <span class="api-tab__path">{{ endpoint.path }}</span>
            </button>
          </div>

          <div class="api-showcase__content">
            <div class="code-block">
              <div class="code-block__header">
                <span class="code-block__title">Request</span>
                <button class="code-block__copy">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <rect x="9" y="9" width="13" height="13" rx="2" ry="2"/>
                    <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/>
                  </svg>
                </button>
              </div>
              <pre class="code-block__code">{{ currentEndpoint?.request }}</pre>
            </div>

            <div class="code-block">
              <div class="code-block__header">
                <span class="code-block__title">Response</span>
                <span class="code-block__status">200 OK</span>
              </div>
              <pre class="code-block__code">{{ currentEndpoint?.response }}</pre>
            </div>
          </div>
        </div>

        <div class="api-features">
          <h3 class="api-features__title">API Features</h3>
          
          <div class="feature-card">
            <div class="feature-card__icon">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
              </svg>
            </div>
            <div class="feature-card__content">
              <h4>Authentication</h4>
              <p>Secure JWT-based authentication for all endpoints</p>
            </div>
          </div>

          <div class="feature-card">
            <div class="feature-card__icon">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/>
              </svg>
            </div>
            <div class="feature-card__content">
              <h4>Real-time Data</h4>
              <p>Access current air quality readings from all stations</p>
            </div>
          </div>

          <div class="feature-card">
            <div class="feature-card__icon">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <line x1="12" y1="1" x2="12" y2="23"/>
                <path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/>
              </svg>
            </div>
            <div class="feature-card__content">
              <h4>Historical Stats</h4>
              <p>Query daily aggregated data with flexible filters</p>
            </div>
          </div>

          <div class="feature-card">
            <div class="feature-card__icon">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
                <polyline points="7 10 12 15 17 10"/>
                <line x1="12" y1="15" x2="12" y2="3"/>
              </svg>
            </div>
            <div class="feature-card__content">
              <h4>Data Export</h4>
              <p>Export datasets in CSV format for analysis</p>
            </div>
          </div>

          <div class="api-docs-link">
            <a href="#" class="btn btn--outline">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                <polyline points="14 2 14 8 20 8"/>
                <line x1="16" y1="13" x2="8" y2="13"/>
                <line x1="16" y1="17" x2="8" y2="17"/>
                <polyline points="10 9 9 9 8 9"/>
              </svg>
              View Full API Documentation
            </a>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'

interface ApiEndpoint {
  id: string
  method: string
  path: string
  request: string
  response: string
}

const activeEndpoint = ref('current')

const endpoints: ApiEndpoint[] = [
  {
    id: 'current',
    method: 'GET',
    path: '/api/air-quality/current',
    request: `curl -X GET "https://api.airquality.com/api/air-quality/current?city=Bogota" \\
  -H "Authorization: Bearer YOUR_TOKEN"`,
    response: `{
  "city": "Bogotá",
  "current_aqi": 58,
  "status": "moderate",
  "readings": [
    {
      "pollutant": "PM2.5",
      "value": 18.5,
      "unit": "µg/m³",
      "aqi": 62
    },
    {
      "pollutant": "PM10",
      "value": 42.3,
      "unit": "µg/m³",
      "aqi": 55
    }
  ],
  "timestamp": "2025-11-27T10:30:00Z"
}`
  },
  {
    id: 'stations',
    method: 'GET',
    path: '/api/stations',
    request: `curl -X GET "https://api.airquality.com/api/stations?city=Bogota" \\
  -H "Authorization: Bearer YOUR_TOKEN"`,
    response: `{
  "stations": [
    {
      "id": 1,
      "name": "Kennedy Station",
      "latitude": 4.6285,
      "longitude": -74.1315,
      "city": "Bogotá",
      "country": "Colombia"
    },
    {
      "id": 2,
      "name": "Usaquén Station",
      "latitude": 4.7110,
      "longitude": -74.0301,
      "city": "Bogotá",
      "country": "Colombia"
    }
  ],
  "total": 2
}`
  },
  {
    id: 'daily-stats',
    method: 'GET',
    path: '/api/air-quality/daily-stats',
    request: `curl -X GET "https://api.airquality.com/api/air-quality/daily-stats?station_id=1&start_date=2025-11-01&end_date=2025-11-27" \\
  -H "Authorization: Bearer YOUR_TOKEN"`,
    response: `{
  "stats": [
    {
      "date": "2025-11-27",
      "station_id": 1,
      "pollutant": "PM2.5",
      "avg_value": 18.2,
      "avg_aqi": 61,
      "max_aqi": 78,
      "min_aqi": 45,
      "readings_count": 24
    }
  ],
  "total": 1
}`
  },
  {
    id: 'recommendations',
    method: 'GET',
    path: '/api/recommendations/current',
    request: `curl -X GET "https://api.airquality.com/api/recommendations/current" \\
  -H "Authorization: Bearer YOUR_TOKEN"`,
    response: `{
  "location": "Bogotá",
  "pollution_level": 58,
  "status": "moderate",
  "message": "Air quality is acceptable. Sensitive individuals should consider limiting prolonged outdoor activities.",
  "products": [
    {
      "name": "Basic Face Mask",
      "type": "mask",
      "url": "https://example.com/masks"
    }
  ],
  "created_at": "2025-11-27T10:30:00Z"
}`
  }
]

const currentEndpoint = computed(() => 
  endpoints.find(e => e.id === activeEndpoint.value)
)
</script>

<style scoped>
.api-section {
  padding: calc(var(--space-6) * 2) var(--space-5);
  background: var(--color-bg-surface);
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
  margin-bottom: var(--space-3);
  color: var(--color-text-primary);
}

.section-subtitle {
  font-size: 18px;
  color: var(--color-text-secondary);
}

.api-grid {
  display: grid;
  grid-template-columns: 1.5fr 1fr;
  gap: var(--space-6);
  align-items: start;
}

.api-showcase {
  background: var(--color-bg-app);
  border: 1px solid var(--color-border-subtle);
  border-radius: var(--radius-lg);
  overflow: hidden;
}

.api-showcase__tabs {
  display: flex;
  flex-direction: column;
  gap: 1px;
  background: var(--color-border-subtle);
  border-bottom: 1px solid var(--color-border-subtle);
}

.api-tab {
  background: var(--color-bg-app);
  border: none;
  padding: var(--space-3) var(--space-4);
  display: flex;
  align-items: center;
  gap: var(--space-3);
  cursor: pointer;
  transition: all 0.2s ease;
  font-family: 'Monaco', 'Courier New', monospace;
  font-size: 13px;
  text-align: left;
}

.api-tab:hover {
  background: rgba(0, 137, 123, 0.05);
}

.api-tab--active {
  background: rgba(0, 137, 123, 0.1);
  border-left: 3px solid var(--color-primary-teal);
}

.api-tab__method {
  font-weight: 700;
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 11px;
}

.api-tab__method--get {
  background: rgba(67, 160, 71, 0.2);
  color: var(--color-secondary-green);
}

.api-tab__method--post {
  background: rgba(30, 136, 229, 0.2);
  color: var(--color-info-blue);
}

.api-tab__path {
  color: var(--color-text-secondary);
  flex: 1;
}

.api-showcase__content {
  padding: var(--space-4);
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
}

.code-block {
  background: rgba(0, 0, 0, 0.3);
  border: 1px solid var(--color-border-subtle);
  border-radius: var(--radius-md);
  overflow: hidden;
}

.code-block__header {
  background: rgba(0, 0, 0, 0.2);
  padding: var(--space-2) var(--space-3);
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid var(--color-border-subtle);
}

.code-block__title {
  font-size: 12px;
  font-weight: 600;
  color: var(--color-text-secondary);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.code-block__status {
  font-size: 12px;
  color: var(--color-secondary-green);
  font-weight: 600;
}

.code-block__copy {
  background: none;
  border: none;
  color: var(--color-text-secondary);
  cursor: pointer;
  padding: 4px;
  display: flex;
  align-items: center;
  transition: color 0.2s ease;
}

.code-block__copy:hover {
  color: var(--color-primary-teal);
}

.code-block__code {
  padding: var(--space-3);
  margin: 0;
  font-family: 'Monaco', 'Courier New', monospace;
  font-size: 12px;
  line-height: 1.6;
  color: var(--color-text-primary);
  overflow-x: auto;
  white-space: pre;
}

.api-features {
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
}

.api-features__title {
  font-size: 24px;
  font-weight: 700;
  color: var(--color-text-primary);
  margin-bottom: var(--space-2);
}

.feature-card {
  display: flex;
  gap: var(--space-3);
  padding: var(--space-4);
  background: var(--color-bg-app);
  border: 1px solid var(--color-border-subtle);
  border-radius: var(--radius-md);
  transition: all 0.2s ease;
}

.feature-card:hover {
  border-color: var(--color-primary-teal);
  transform: translateX(4px);
}

.feature-card__icon {
  width: 48px;
  height: 48px;
  flex-shrink: 0;
  background: rgba(0, 137, 123, 0.1);
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--color-primary-teal);
}

.feature-card__content h4 {
  font-size: 16px;
  font-weight: 600;
  color: var(--color-text-primary);
  margin: 0 0 var(--space-1);
}

.feature-card__content p {
  font-size: 14px;
  color: var(--color-text-secondary);
  margin: 0;
  line-height: 1.5;
}

.api-docs-link {
  margin-top: var(--space-4);
}

.btn {
  display: inline-flex;
  align-items: center;
  gap: var(--space-2);
  padding: var(--space-3) var(--space-4);
  border-radius: var(--radius-md);
  font-weight: 600;
  text-decoration: none;
  transition: all 0.2s ease;
  border: 2px solid var(--color-primary-teal);
  color: var(--color-primary-teal);
  background: transparent;
  cursor: pointer;
  width: 100%;
  justify-content: center;
}

.btn:hover {
  background: var(--color-primary-teal);
  color: white;
  transform: translateY(-2px);
}

@media (max-width: 1024px) {
  .api-grid {
    grid-template-columns: 1fr;
  }
  
  .api-features {
    order: 2;
  }
}

@media (max-width: 768px) {
  .section-title {
    font-size: 32px;
  }
  
  .code-block__code {
    font-size: 11px;
  }
}
</style>
