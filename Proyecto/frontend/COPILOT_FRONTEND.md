# Air Quality Platform – Frontend Copilot Instructions

You are working **inside the `frontend/` folder** of a monorepo for the project **“Air Quality Platform”**.

Your job is to implement the **web UI** using **Vue 3** (Composition API preferred) and to follow the **global architecture and data model** described in `docs/copilot-global.md`.

All visible text in the UI **must be in English**.

---

## 1. Tech stack and project structure

Use **Vue 3** with the Composition API and Vue Router. TypeScript is preferred but not mandatory.

Recommended structure under `frontend/src`:

- `main.ts` (or `main.js`) → app bootstrap.
- `App.vue` → root layout shell (navbar + footer + `<router-view />`).
- `router/index.ts` → route definitions.
- `views/` → page-level components:
  - `LandingView.vue` (public home / marketing page).
  - `LoginView.vue`
  - `CitizenDashboardView.vue`
  - `ResearcherDashboardView.vue`
  - `AdminDashboardView.vue`
  - `SettingsView.vue`
- `components/` → shared components:
  - `components/layout/` (e.g., `AppNavbar.vue`, `AppFooter.vue`, `DashboardShell.vue`).
  - `components/ui/` (buttons, cards, badges, charts, inputs).
  - `components/sections/` (hero, role cards, “How it works” section, etc.).
- `services/` → HTTP clients and API abstractions (e.g., `apiClient.ts`, `authService.ts`, `airQualityService.ts`).
- `stores/` (if using Pinia) → global state (auth, user, preferences).
- `styles/` → global styling and design tokens:
  - `styles/tokens.css`
  - `styles/global.css` or `styles/base.css`

When generating code, **respect this structure** or extend it in a consistent way.

---

## 2. Design system and styling methodology

The frontend uses a **dark, dashboard-style theme** inspired by environmental data and city lights at night.

You must:

1. Use the **global color palette** as design tokens.
2. Use **CSS custom properties (variables)** in a central place.
3. Follow a **consistent CSS methodology** (BEM naming for custom classes).
4. Ensure **responsive layouts** (desktop-first, then adapt for tablet/mobile).

### 2.1. Color palette (tokens)

Always reference colors via CSS variables defined in `styles/tokens.css`. Use these base values:

```css
:root {
  /* Brand / status colors */
  --color-primary-teal: #00897B;
  --color-secondary-green: #43A047;
  --color-accent-amber: #FFB300;
  --color-accent-red: #E53935;
  --color-info-blue: #1E88E5;

  /* Neutrals */
  --color-bg-app: #0B1020;
  --color-bg-surface: #121826;
  --color-border-subtle: #273043;
  --color-text-primary: #F5F7FA;
  --color-text-secondary: #B0BEC5;
  --color-bg-light: #F4F6FB;

  /* Radius tokens */
  --radius-sm: 6px;
  --radius-md: 10px;
  --radius-lg: 16px;

  /* Spacing tokens */
  --space-1: 4px;
  --space-2: 8px;
  --space-3: 12px;
  --space-4: 16px;
  --space-5: 24px;
  --space-6: 32px;
}
```

Usage rules:

* Use **`--color-primary-teal`** for primary actions (main CTAs, primary buttons, active nav link).
* Use **green / amber / red** **only** for air quality status (badges, chips, chart segments, AQI indicators).
* Use **dark background** (`--color-bg-app`) for the app shell, and **surface** (`--color-bg-surface`) for cards and sections.
* Use **text-primary** and **text-secondary** for typography; avoid custom grays.

### 2.2. Typography

* Use a modern, geometric sans-serif such as **Inter** or **Roboto**.
* Define base typography in `styles/global.css`, for example:

```css
body {
  margin: 0;
  font-family: system-ui, -apple-system, BlinkMacSystemFont, "Inter", "Roboto", sans-serif;
  background-color: var(--color-bg-app);
  color: var(--color-text-primary);
}
```

* Use semantic headings (`<h1>`, `<h2>`, etc.) and keep text hierarchy clear.

### 2.3. CSS methodology

When generating classes:

* Use **BEM-style naming** for custom styles:

  * `landing-hero__title`
  * `role-card__icon`
  * `navbar__link--active`

* Avoid deep nested selectors; prefer single-class selectors when possible.

* Use **spacing tokens** instead of arbitrary pixel values:

  ```css
  .section {
    padding: var(--space-6) var(--space-5);
  }
  ```

* Reuse common layout patterns via utility classes where it makes sense (e.g. `.stack`, `.cluster`, `.grid-3`), but keep them simple and well documented.

### 2.4. Responsiveness and accessibility

* Layout is **desktop-first**, but must adapt cleanly to **tablet** and **mobile**:

  * Use media queries to stack columns vertically on small viewports.
  * Ensure navigation collapses into a simpler pattern (e.g., menu button) if needed.
* Always ensure:

  * Sufficient **color contrast** on dark background.
  * Clear **focus states** for interactive elements (buttons, links, inputs).
  * Proper `aria-labels` where icons are used without text.

---

## 3. Landing page (public home) – Layout and components

The main public entry point is the **Landing page**, implemented as `LandingView.vue` (or similar) and composed of smaller sections.

High-level goal:

> A clean, modern, dark-themed landing page that explains what the platform does, who it is for, and drives visitors to **sign in**.

### 3.1. Overall layout structure

The landing page should follow this section order:

1. **Top navigation bar**
2. **Hero section**
3. **“Built for different roles” section**
4. **“How it works” section**
5. **“Sample data insights” section**
6. **Footer**

Implement each section as either:

* Internal sections within `LandingView.vue`, or
* Reusable components in `components/sections/`, e.g.:

  * `LandingHeroSection.vue`
  * `LandingRolesSection.vue`
  * `LandingHowItWorksSection.vue`
  * `LandingInsightsSection.vue`

#### 3.1.1. Top navigation bar

Component: `AppNavbar.vue`.

* Background: `var(--color-bg-surface)`.
* Layout:

  * **Left**: logo + product name.

    * Logo: image placeholder (e.g. from `src/assets/logo-air-quality.svg`) with a simple circular icon hinting at city skyline and airflow.
    * Text: **“Air Quality Platform”**.
  * **Right**: navigation links:

    * “Overview”
    * “Features”
    * “For cities”
    * “Docs”
  * Far right: two buttons:

    * Secondary button: “Sign up”
    * Primary button: “Sign in” (uses `--color-primary-teal`).
* Use a slightly elevated effect (subtle border or shadow) to separate the navbar from the hero section.

#### 3.1.2. Hero section

Component: `LandingHeroSection.vue`.

* Background: dark full-width, using `--color-bg-app` with subtle visual accents (e.g., gradient overlay or simple abstract shapes via CSS, not heavy illustration).
* Layout: **two columns** on desktop, stacked on mobile.

**Left column (text content)**:

* Small label (in green):
  `Live air quality, made understandable`
* Main headline (`<h1>`):
  `Monitor, understand and act on air quality in your city.`
* Supporting paragraph (2–3 lines):

  > “Air Quality Platform brings together real-time readings, daily statistics and simple health recommendations for citizens, researchers and city teams.”
* Primary CTA button: **“Sign in to dashboard”** (primary teal).
* Secondary text button: **“Explore features”** (text-style link with subtle underline, no heavy button background).

**Right column (data card visual)**:

* Card with background `--color-bg-surface`, border `--color-border-subtle`, radius `--radius-lg`.
* Content:

  * Title: `Today in Bogotá` (city name is a placeholder).
  * Big AQI value, e.g. `AQI 58` with a status label `Moderate` as a pill/badge:

    * Use green/amber/red depending on the example state.
  * Small list of 3 pollutants:

    * `PM2.5`, `PM10`, `O3` with values and units.
  * Simple **mini line chart** (SVG or lightweight chart) showing AQI over last 24 hours.

Chart styling:

* Use teal (`--color-primary-teal`) for the main line.
* Use subtle grid lines with `--color-border-subtle`.
* Keep it minimal and “dashboard-like”.

#### 3.1.3. “Built for different roles” section

Component: `LandingRolesSection.vue`.

* Background: `--color-bg-app`.
* Centered title:
  `Designed for everyone who cares about air quality`
* Subtitle: one concise sentence explaining inclusiveness across citizens, researchers and city teams.

Layout:

* Three **cards** horizontally on desktop, stacked vertically on mobile.
* Card background: `--color-bg-surface`.
* Subtle teal accent (e.g., top border or small left border).

Each card:

* Has an icon placeholder (can be a simple circle or generic role icon).
* Title: `Citizen`, `Researcher`, `Admin`.
* Short description + bullet list:

**Citizen:**

* Description:

  > “Check current AQI, understand what it means and receive simple health recommendations.”
* Bullets:

  * “Current air quality in your city”
  * “Clear health guidance”
  * “Basic product suggestions”

**Researcher:**

* Description:

  > “Explore historical trends and export clean datasets for analysis.”
* Bullets:

  * “Daily statistics and trends”
  * “Filter by station and pollutant”
  * “Export CSV datasets”

**Admin:**

* Description:

  > “Manage stations, roles and alert thresholds across your network.”
* Bullets:

  * “Manage stations and coverage”
  * “Control user roles and permissions”
  * “Configure alert thresholds”

#### 3.1.4. “How it works” section

Component: `LandingHowItWorksSection.vue`.

* Title: `How the platform works`
* Layout: 3-step horizontally aligned cards (vertical on mobile).

Steps:

1. **Ingest**

   * Text: “We connect to external air quality APIs and validate incoming data.”
2. **Transform**

   * Text: “We normalize readings and compute daily statistics for each station.”
3. **Deliver**

   * Text: “Dashboards and APIs make the data accessible for citizens and experts.”

Each step:

* Uses an icon placeholder (could be a simple circle with a letter or minimal illustration).
* Has a short 1–2 line description.
* Card styling matches role cards (surface + subtle border).

#### 3.1.5. “Sample data insights” section

Component: `LandingInsightsSection.vue`.

* One medium-width card/panel centered in the page.
* Title: `Daily AQI trend example`.
* Simple line chart showing `avg_aqi` over several days (static sample data for now).
* Small legend or labels with the **green/amber/red** scale for air quality categories.

Clarify in small text that this is a **preview** of what researchers and admins can see in the dashboard.

#### 3.1.6. Footer

Component: `AppFooter.vue`.

* Background: `--color-bg-surface` or slightly darker variant.
* Layout:

  * Left: product name and short tagline, e.g.:

    * `Air Quality Platform`
    * `Helping cities monitor and act on air quality.`
  * Right: horizontal list of links:

    * “Privacy”
    * “Terms”
    * “API docs”
    * “Contact”
* Bottom row (tiny text):
  `Demo interface – not real-time data.`

---

## 4. Other core views

Beyond `LandingView.vue`, implement the following pages according to the global backend contracts:

### 4.1. LoginView

* Simple centered card with:

  * Title: `Sign in`.
  * Fields: **Email**, **Password**.
  * Primary button: `Sign in`.
* Use the primary teal color for the button.
* On submit, call the backend auth endpoint and, on success, redirect to the appropriate dashboard.

### 4.2. CitizenDashboardView

* Show:

  * Current AQI for user’s city.
  * Nearby stations list.
  * Health recommendation component.
  * Simple product suggestion component.
* Use cards with `--color-bg-surface` and consistent spacing.

### 4.3. ResearcherDashboardView

* Include:

  * Filters (city, station, date range, pollutant).
  * Data chart (e.g., line chart based on `AirQualityDailyStats`).
  * Button `Export CSV` for aggregated data.

### 4.4. AdminDashboardView

* Include:

  * Station management table (CRUD UI).
  * User list with role selector.
  * Basic alert threshold configuration.

### 4.5. SettingsView

* Allow editing:

  * Theme (`light` / `dark`).
  * Default city.
  * Notification channels.
* These settings interact with the backend APIs that use the NoSQL storage model for `user_preferences` and `dashboard_configs`.

---

## 5. API integration and services

When calling the backend:

* Use a single `apiClient` abstraction in `services/apiClient.ts` (or similar).
* Base URL must come from environment (e.g. `import.meta.env.VITE_API_BASE_URL`).
* Implement strongly typed service modules, for example:

  * `services/authService.ts`
  * `services/airQualityService.ts`
  * `services/userPreferencesService.ts`

Handle loading states, error states and empty states in the UI in a simple, clear way (spinners, messages, etc.).

---

## 6. General frontend rules

Whenever you generate or modify frontend code:

* Keep **all UI text in English**.
* Use **design tokens** (CSS variables) instead of hard-coded colors and spacing.
* Follow the **dark theme** and dashboard-like style described above.
* Keep components **small and focused**, and reuse shared components where possible.
* Make sure the page is **responsive**, readable and accessible.
