<template>
  <footer class="footer">
    <div class="footer__container">
      <!-- Main Footer Content -->
      <div class="footer__content">
        <!-- Brand Section -->
        <div class="footer__section footer__section--brand">
          <div class="footer__brand">
            <div class="footer__logo">
              <svg width="32" height="32" viewBox="0 0 48 48" fill="none">
                <circle cx="24" cy="24" r="20" stroke="var(--color-primary-teal)" stroke-width="2" opacity="0.3"/>
                <circle cx="24" cy="24" r="14" stroke="var(--color-primary-teal)" stroke-width="2"/>
                <circle cx="24" cy="24" r="8" fill="var(--color-primary-teal)"/>
              </svg>
            </div>
            <div>
              <h3 class="footer__title">Air Quality Platform</h3>
              <p class="footer__tagline">Helping cities monitor and act on air quality</p>
            </div>
          </div>
          <p class="footer__description">
            Real-time air quality monitoring, historical data analysis, and actionable health recommendations 
            for citizens, researchers, and city administrators.
          </p>
          <div class="footer__social">
            <a href="#" class="footer__social-link" aria-label="GitHub">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
              </svg>
            </a>
            <a href="#" class="footer__social-link" aria-label="Twitter">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                <path d="M23 3a10.9 10.9 0 01-3.14 1.53 4.48 4.48 0 00-7.86 3v1A10.66 10.66 0 013 4s-4 9 5 13a11.64 11.64 0 01-7 2c9 5 20 0 20-11.5a4.5 4.5 0 00-.08-.83A7.72 7.72 0 0023 3z"/>
              </svg>
            </a>
            <a href="#" class="footer__social-link" aria-label="LinkedIn">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                <path d="M16 8a6 6 0 016 6v7h-4v-7a2 2 0 00-2-2 2 2 0 00-2 2v7h-4v-7a6 6 0 016-6zM2 9h4v12H2z"/>
                <circle cx="4" cy="4" r="2"/>
              </svg>
            </a>
          </div>
        </div>

        <!-- Product Links -->
        <div class="footer__section">
          <h4 class="footer__section-title">Product</h4>
          <ul class="footer__links">
            <li><a href="#features" class="footer__link">Features</a></li>
            <li><a href="#api" class="footer__link">API</a></li>
            <li><a href="#pricing" class="footer__link">Pricing</a></li>
            <li><a href="#integrations" class="footer__link">Integrations</a></li>
            <li><a href="#changelog" class="footer__link">Changelog</a></li>
          </ul>
        </div>

        <!-- Resources Links -->
        <div class="footer__section">
          <h4 class="footer__section-title">Resources</h4>
          <ul class="footer__links">
            <li><a href="#docs" class="footer__link">Documentation</a></li>
            <li><a href="#guides" class="footer__link">Guides</a></li>
            <li><a href="#blog" class="footer__link">Blog</a></li>
            <li><a href="#support" class="footer__link">Support</a></li>
            <li><a href="#status" class="footer__link">System Status</a></li>
          </ul>
        </div>

        <!-- Company Links -->
        <div class="footer__section">
          <h4 class="footer__section-title">Company</h4>
          <ul class="footer__links">
            <li><a href="#about" class="footer__link">About</a></li>
            <li><a href="#team" class="footer__link">Team</a></li>
            <li><a href="#careers" class="footer__link">Careers</a></li>
            <li><a href="#contact" class="footer__link">Contact</a></li>
            <li><a href="#press" class="footer__link">Press Kit</a></li>
          </ul>
        </div>

        <!-- Legal Links -->
        <div class="footer__section">
          <h4 class="footer__section-title">Legal</h4>
          <ul class="footer__links">
            <li><a href="#privacy" class="footer__link">Privacy Policy</a></li>
            <li><a href="#terms" class="footer__link">Terms of Service</a></li>
            <li><a href="#cookies" class="footer__link">Cookie Policy</a></li>
            <li><a href="#security" class="footer__link">Security</a></li>
            <li><a href="#compliance" class="footer__link">Compliance</a></li>
          </ul>
        </div>
      </div>

      <!-- Footer Bottom -->
      <div class="footer__bottom">
        <div class="footer__bottom-content">
          <p class="footer__copyright">
            © 2025 Air Quality Platform. All rights reserved.
          </p>
          <div class="footer__badges">
            <div class="footer__badge">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="10"/>
                <line x1="12" y1="16" x2="12" y2="12"/>
                <line x1="12" y1="8" x2="12.01" y2="8"/>
              </svg>
              <span>Demo Interface</span>
            </div>
            <div class="footer__badge">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
              </svg>
              <span>Educational Purpose</span>
            </div>
            <div class="footer__badge footer__badge--live">
              <span class="footer__badge-pulse"></span>
              <span>Built with Design Patterns</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </footer>
</template>

<style scoped>
.footer {
  background: var(--color-bg-surface);
  border-top: 1px solid var(--color-border-subtle);
  margin-top: auto;
}

.footer__container {
  max-width: 1400px;
  margin: 0 auto;
  padding: calc(var(--space-6) * 1.5) var(--space-5) var(--space-5);
}

.footer__content {
  display: grid;
  grid-template-columns: 2fr repeat(4, 1fr);
  gap: var(--space-6);
  margin-bottom: var(--space-6);
}

.footer__section--brand {
  grid-column: span 1;
}

.footer__brand {
  display: flex;
  align-items: flex-start;
  gap: var(--space-3);
  margin-bottom: var(--space-4);
}

.footer__logo {
  flex-shrink: 0;
}

.footer__title {
  font-size: 18px;
  font-weight: 700;
  color: var(--color-text-primary);
  margin: 0 0 var(--space-1);
}

.footer__tagline {
  font-size: 13px;
  color: var(--color-text-secondary);
  margin: 0;
}

.footer__description {
  color: var(--color-text-secondary);
  font-size: 14px;
  line-height: 1.6;
  margin-bottom: var(--space-4);
}

.footer__social {
  display: flex;
  gap: var(--space-2);
}

.footer__social-link {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--color-text-secondary);
  background: rgba(0, 137, 123, 0.05);
  border: 1px solid var(--color-border-subtle);
  border-radius: var(--radius-md);
  transition: all 0.2s ease;
}

.footer__social-link:hover {
  color: var(--color-primary-teal);
  background: rgba(0, 137, 123, 0.15);
  border-color: var(--color-primary-teal);
  transform: translateY(-2px);
}

.footer__section-title {
  font-size: 14px;
  font-weight: 700;
  color: var(--color-text-primary);
  margin: 0 0 var(--space-4);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.footer__links {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.footer__link {
  color: var(--color-text-secondary);
  text-decoration: none;
  font-size: 14px;
  transition: all 0.2s ease;
  display: inline-block;
}

.footer__link:hover {
  color: var(--color-primary-teal);
  padding-left: var(--space-1);
}

.footer__bottom {
  padding-top: var(--space-5);
  border-top: 1px solid var(--color-border-subtle);
}

.footer__bottom-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: var(--space-4);
  flex-wrap: wrap;
}

.footer__copyright {
  color: var(--color-text-secondary);
  font-size: 14px;
  margin: 0;
}

.footer__badges {
  display: flex;
  gap: var(--space-3);
  flex-wrap: wrap;
}

.footer__badge {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  padding: var(--space-2) var(--space-3);
  background: rgba(0, 0, 0, 0.2);
  border: 1px solid var(--color-border-subtle);
  border-radius: 999px;
  font-size: 12px;
  color: var(--color-text-secondary);
}

.footer__badge svg {
  flex-shrink: 0;
}

.footer__badge--live {
  border-color: var(--color-primary-teal);
  background: rgba(0, 137, 123, 0.1);
  color: var(--color-primary-teal);
}

.footer__badge-pulse {
  width: 8px;
  height: 8px;
  background: var(--color-primary-teal);
  border-radius: 50%;
  animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% { 
    opacity: 1; 
    transform: scale(1); 
  }
  50% { 
    opacity: 0.5; 
    transform: scale(1.2); 
  }
}

@media (max-width: 1200px) {
  .footer__content {
    grid-template-columns: 1fr 1fr;
  }
  
  .footer__section--brand {
    grid-column: span 2;
  }
}

@media (max-width: 768px) {
  .footer__content {
    grid-template-columns: 1fr;
  }
  
  .footer__section--brand {
    grid-column: span 1;
  }
  
  .footer__bottom-content {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .footer__badges {
    width: 100%;
  }
}

@media (max-width: 480px) {
  .footer__brand {
    flex-direction: column;
  }
  
  .footer__badges {
    flex-direction: column;
  }
  
  .footer__badge {
    justify-content: center;
  }
}
</style>
