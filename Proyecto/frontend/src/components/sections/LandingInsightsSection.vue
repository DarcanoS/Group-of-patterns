<template>
  <section class="insights-section">
    <div class="container">
      <div class="section-header">
        <h2 class="section-title">Data-Driven Insights</h2>
        <p class="section-subtitle">
          Preview of what researchers and admins can see in the dashboard
        </p>
      </div>

      <div class="insights-grid">
        <div class="insight-card insight-card--large">
          <div class="card-header">
            <h3>Daily AQI Trend</h3>
            <div class="card-controls">
              <button class="control-btn">Week</button>
              <button class="control-btn control-btn--active">Month</button>
              <button class="control-btn">Year</button>
            </div>
          </div>
          
          <div class="chart-container">
            <svg width="100%" height="240" viewBox="0 0 600 180" preserveAspectRatio="none">
              <defs>
                <linearGradient id="areaGradient" x1="0%" y1="0%" x2="0%" y2="100%">
                  <stop offset="0%" style="stop-color:var(--color-primary-teal);stop-opacity:0.3" />
                  <stop offset="100%" style="stop-color:var(--color-primary-teal);stop-opacity:0" />
                </linearGradient>
              </defs>
              
              <!-- Grid lines -->
              <line x1="0" y1="45" x2="600" y2="45" stroke="var(--color-border-subtle)" stroke-width="1" opacity="0.5"/>
              <line x1="0" y1="90" x2="600" y2="90" stroke="var(--color-border-subtle)" stroke-width="1" opacity="0.5"/>
              <line x1="0" y1="135" x2="600" y2="135" stroke="var(--color-border-subtle)" stroke-width="1" opacity="0.5"/>
              
              <!-- Area fill -->
              <path d="M0,120 L50,115 L100,110 L150,100 L200,85 L250,90 L300,95 L350,80 L400,85 L450,75 L500,80 L550,78 L600,85 L600,180 L0,180 Z" 
                    fill="url(#areaGradient)"/>
              
              <!-- Line -->
              <path d="M0,120 L50,115 L100,110 L150,100 L200,85 L250,90 L300,95 L350,80 L400,85 L450,75 L500,80 L550,78 L600,85" 
                    fill="none" stroke="var(--color-primary-teal)" stroke-width="3"/>
              
              <!-- Data points -->
              <circle cx="150" cy="100" r="4" fill="var(--color-secondary-green)"/>
              <circle cx="350" cy="80" r="4" fill="var(--color-accent-amber)"/>
              <circle cx="450" cy="75" r="4" fill="var(--color-accent-red)"/>
            </svg>
            
            <div class="chart-legend">
              <div class="legend-item">
                <span class="legend-color legend-color--good"></span>
                <span class="legend-label">Good (0-50)</span>
              </div>
              <div class="legend-item">
                <span class="legend-color legend-color--moderate"></span>
                <span class="legend-label">Moderate (51-100)</span>
              </div>
              <div class="legend-item">
                <span class="legend-color legend-color--unhealthy"></span>
                <span class="legend-label">Unhealthy (101+)</span>
              </div>
            </div>
          </div>
        </div>

        <div class="insight-card">
          <div class="card-header">
            <h3>Top Stations</h3>
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/>
              <circle cx="12" cy="10" r="3"/>
            </svg>
          </div>
          
          <div class="stations-list">
            <div class="station-item">
              <div class="station-info">
                <span class="station-name">Kennedy Station</span>
                <span class="station-location">Bogotá, Colombia</span>
              </div>
              <div class="station-aqi station-aqi--moderate">62</div>
            </div>
            
            <div class="station-item">
              <div class="station-info">
                <span class="station-name">Usaquén Station</span>
                <span class="station-location">Bogotá, Colombia</span>
              </div>
              <div class="station-aqi station-aqi--good">45</div>
            </div>
            
            <div class="station-item">
              <div class="station-info">
                <span class="station-name">Suba Station</span>
                <span class="station-location">Bogotá, Colombia</span>
              </div>
              <div class="station-aqi station-aqi--moderate">58</div>
            </div>
            
            <div class="station-item">
              <div class="station-info">
                <span class="station-name">Centro Station</span>
                <span class="station-location">Bogotá, Colombia</span>
              </div>
              <div class="station-aqi station-aqi--unhealthy">112</div>
            </div>
          </div>
        </div>

        <div class="insight-card">
          <div class="card-header">
            <h3>Pollutant Breakdown</h3>
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="12" cy="12" r="10"/>
              <line x1="12" y1="2" x2="12" y2="12"/>
              <line x1="12" y1="12" x2="17" y2="17"/>
            </svg>
          </div>
          
          <div class="pollutants-chart">
            <div class="pollutant-bar">
              <div class="pollutant-label">PM2.5</div>
              <div class="bar-track">
                <div class="bar-fill" style="width: 75%; background: var(--color-accent-amber)"></div>
              </div>
              <div class="pollutant-value">18 µg/m³</div>
            </div>
            
            <div class="pollutant-bar">
              <div class="pollutant-label">PM10</div>
              <div class="bar-track">
                <div class="bar-fill" style="width: 60%; background: var(--color-secondary-green)"></div>
              </div>
              <div class="pollutant-value">42 µg/m³</div>
            </div>
            
            <div class="pollutant-bar">
              <div class="pollutant-label">O₃</div>
              <div class="bar-track">
                <div class="bar-fill" style="width: 45%; background: var(--color-secondary-green)"></div>
              </div>
              <div class="pollutant-value">31 ppb</div>
            </div>
            
            <div class="pollutant-bar">
              <div class="pollutant-label">NO₂</div>
              <div class="bar-track">
                <div class="bar-fill" style="width: 35%; background: var(--color-secondary-green)"></div>
              </div>
              <div class="pollutant-value">24 ppb</div>
            </div>
            
            <div class="pollutant-bar">
              <div class="pollutant-label">SO₂</div>
              <div class="bar-track">
                <div class="bar-fill" style="width: 25%; background: var(--color-secondary-green)"></div>
              </div>
              <div class="pollutant-value">8 ppb</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
.insights-section {
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
  margin-bottom: var(--space-3);
  color: var(--color-text-primary);
}

.section-subtitle {
  font-size: 18px;
  color: var(--color-text-secondary);
}

.insights-grid {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: var(--space-5);
}

.insight-card {
  background: var(--color-bg-surface);
  border: 1px solid var(--color-border-subtle);
  border-radius: var(--radius-lg);
  padding: var(--space-5);
  transition: all 0.3s ease;
}

.insight-card:hover {
  border-color: var(--color-primary-teal);
  box-shadow: 0 8px 32px rgba(0, 137, 123, 0.15);
}

.insight-card--large {
  grid-column: 1;
  grid-row: 1 / 3;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--space-4);
}

.card-header h3 {
  font-size: 20px;
  font-weight: 700;
  color: var(--color-text-primary);
  margin: 0;
}

.card-header svg {
  color: var(--color-text-secondary);
}

.card-controls {
  display: flex;
  gap: var(--space-2);
  background: rgba(0, 0, 0, 0.2);
  padding: 4px;
  border-radius: var(--radius-md);
}

.control-btn {
  background: transparent;
  border: none;
  padding: 6px 12px;
  border-radius: var(--radius-sm);
  color: var(--color-text-secondary);
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.control-btn--active {
  background: var(--color-primary-teal);
  color: white;
}

.control-btn:hover:not(.control-btn--active) {
  background: rgba(255, 255, 255, 0.05);
}

.chart-container {
  margin-top: var(--space-4);
}

.chart-legend {
  display: flex;
  justify-content: center;
  gap: var(--space-5);
  margin-top: var(--space-4);
  padding-top: var(--space-4);
  border-top: 1px solid var(--color-border-subtle);
}

.legend-item {
  display: flex;
  align-items: center;
  gap: var(--space-2);
}

.legend-color {
  width: 12px;
  height: 12px;
  border-radius: 50%;
}

.legend-color--good {
  background: var(--color-secondary-green);
}

.legend-color--moderate {
  background: var(--color-accent-amber);
}

.legend-color--unhealthy {
  background: var(--color-accent-red);
}

.legend-label {
  font-size: 13px;
  color: var(--color-text-secondary);
}

.stations-list {
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
}

.station-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--space-3);
  background: rgba(0, 0, 0, 0.2);
  border-radius: var(--radius-md);
  transition: all 0.2s ease;
}

.station-item:hover {
  background: rgba(0, 137, 123, 0.05);
  transform: translateX(4px);
}

.station-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.station-name {
  font-weight: 600;
  color: var(--color-text-primary);
  font-size: 14px;
}

.station-location {
  font-size: 12px;
  color: var(--color-text-secondary);
}

.station-aqi {
  font-size: 24px;
  font-weight: 700;
  padding: var(--space-2) var(--space-3);
  border-radius: var(--radius-md);
  min-width: 60px;
  text-align: center;
}

.station-aqi--good {
  background: rgba(67, 160, 71, 0.2);
  color: var(--color-secondary-green);
}

.station-aqi--moderate {
  background: rgba(255, 179, 0, 0.2);
  color: var(--color-accent-amber);
}

.station-aqi--unhealthy {
  background: rgba(229, 57, 53, 0.2);
  color: var(--color-accent-red);
}

.pollutants-chart {
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
}

.pollutant-bar {
  display: grid;
  grid-template-columns: 60px 1fr 80px;
  align-items: center;
  gap: var(--space-3);
}

.pollutant-label {
  font-weight: 600;
  color: var(--color-text-primary);
  font-size: 14px;
}

.bar-track {
  height: 24px;
  background: rgba(0, 0, 0, 0.3);
  border-radius: 999px;
  overflow: hidden;
  position: relative;
}

.bar-fill {
  height: 100%;
  border-radius: 999px;
  transition: width 0.6s ease;
  position: relative;
}

.bar-fill::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(90deg, transparent 0%, rgba(255, 255, 255, 0.2) 50%, transparent 100%);
  animation: shimmer 2s infinite;
}

@keyframes shimmer {
  0% { transform: translateX(-100%); }
  100% { transform: translateX(100%); }
}

.pollutant-value {
  font-size: 13px;
  font-weight: 600;
  color: var(--color-text-secondary);
  text-align: right;
}

@media (max-width: 1024px) {
  .insights-grid {
    grid-template-columns: 1fr;
  }
  
  .insight-card--large {
    grid-column: 1;
    grid-row: auto;
  }
}

@media (max-width: 768px) {
  .section-title {
    font-size: 32px;
  }
  
  .pollutant-bar {
    grid-template-columns: 50px 1fr 70px;
    gap: var(--space-2);
  }
}
</style>
