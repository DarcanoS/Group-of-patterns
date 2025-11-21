# Air Quality Platform – Global Copilot Instructions

You are helping to develop a web application called **“Air Quality Platform”**.

The goal is to build a **web platform (not a mobile app)** that allows:
- **Citizens** to check current air quality, see basic statistics and receive simple health recommendations.
- **Researchers** to explore historical air quality data and download aggregated datasets.
- **Admins** to manage stations, users and basic alert thresholds.

All **user-facing text** (UI labels, messages, etc.) must be in **English**.

---

## 1. Repository structure and technologies

The project is a **monorepo** with at least these folders:

- `frontend/` → Web application in **Vue 3** (TypeScript preferred, but not mandatory).
- `backend/` → REST API in **Python** using **FastAPI**.
- `ingestion/` → Independent service in **Python** for ingesting data from external air quality APIs.
- `infra/` or similar (optional) → Docker, docker-compose, deployment scripts, etc.
- `docs/` → Documentation (including this file).

### 1.1. Docker

All application code (frontend, backend, ingestion) must be runnable using **Docker**:

- `frontend/Dockerfile` → Node-based image that builds the Vue app and serves it (e.g., via nginx or `npm run preview`).
- `backend/Dockerfile` → Python-based image (e.g., `python:3.12-slim`) running FastAPI with Uvicorn.
- `ingestion/Dockerfile` → Python-based image running the ingestion service (script, worker, or scheduler).

You may optionally provide a `docker-compose.yml` that:
- Starts **backend** and **frontend**.
- Uses environment variables to connect to:
  - **PostgreSQL + PostGIS** (main relational DB).
  - A remote **NoSQL** store for configurations (e.g., MongoDB).

For development, you may document or include an optional local PostGIS service (commented in compose).

---

## 2. Data model and storage

The main relational database is **PostgreSQL** with **PostGIS enabled**.

- Do **not** store arbitrary JSON blobs in relational tables for core domain data.
- Use proper relational modeling; JSON is acceptable only for flexible configurations where explicitly stated.

### 2.1. Core relational entities (PostgreSQL)

Model at least the following tables with English names:

- `Station`
  - Fields: `id`, `name`, `latitude`, `longitude`, `city`, `country`, `region_id`.

- `MapRegion`
  - Fields: `id`, `name`, `geom` (PostGIS `geometry` type).

- `Pollutant`
  - Fields: `id`, `name`, `unit`, `description`.

- `AirQualityReading`
  - Fields: `id`, `station_id`, `pollutant_id`, `datetime`, `value`, `aqi`.

- `AppUser`
  - Fields: `id`, `name`, `email`, `password_hash`, `location`, `role_id`.

- `Role`
  - Fields: `id`, `name`.

- `Permission`
  - Fields: `id`, `name`.

- `RolePermission`
  - Fields: `role_id`, `permission_id` (composite PK).

- `Alert`
  - Fields: `id`, `user_id`, `pollutant_id`, `threshold`, `method`, `triggered_at`.

- `Recommendation`
  - Fields: `id`, `user_id`, `location`, `pollution_level`, `message`, `created_at`.

- `ProductRecommendation`
  - Fields: `id`, `recommendation_id`, `product_name`, `product_type`, `product_url`.

- `Report`
  - Fields: `id`, `user_id`, `created_at`, `city`, `start_date`, `end_date`, `station_id`, `pollutant_id`, `file_path`.

- `AirQualityDailyStats` (analytics table)
  - Fields: `id`, `station_id`, `pollutant_id`, `date`, `avg_value`, `avg_aqi`, `max_aqi`, `min_aqi`, `readings_count`.

### 2.2. NoSQL for flexible configurations

In addition to PostgreSQL, prepare an optional **NoSQL** store (e.g. MongoDB) for dynamic configuration and preferences.

Conceptual collections:

- `user_preferences`
  - Key: `user_id` (linked to `AppUser.id`).
  - Content: `theme`, `default_city`, `default_pollutants`, `notification_channels`, `updated_at`.

- `dashboard_configs`
  - Key: `user_id`.
  - Content: layout configuration for each user’s dashboard (widgets, positions, visible panels, etc.).

The backend must provide services/endpoints to read and write these configurations. Initial implementations can mock the NoSQL access if necessary.

---

## 3. Logical architecture and roles

### 3.1. Frontend (Vue 3)

- Single-page application named **“Air Quality Platform”**.
- UI language: **English only**.
- Main roles:
  - **Citizen** → Current air quality, basic stats, health recommendations, simple product suggestions.
  - **Researcher** → Historical statistics, filters by station/pollutant/date, data exports.
  - **Admin** → Station, user and alerts management.

### 3.2. Backend (FastAPI)

- Expose REST endpoints grouped conceptually as:
  - **Public REST API** → endpoints for citizen and researcher workflows.
  - **Admin REST API** → endpoints for administrative tasks (stations, users, permissions, etc.).

- All responses must be JSON with English field names.

### 3.3. Ingestion service (`ingestion/`)

- Independent Python process/service that:
  - Consumes **external air quality APIs**.
  - Normalizes units, pollutant names and timestamps.
  - Inserts data into PostgreSQL (`AirQualityReading`) and triggers updates for analytics tables such as `AirQualityDailyStats`.

- Configured entirely with environment variables (e.g., `DB_HOST`, `DB_USER`, `DB_PASSWORD`, API keys, etc.).

### 3.4. Data processing flow

- Periodic ingestion (e.g., every 10–60 minutes) from external APIs.
- Validation & normalization before persisting into `AirQualityReading`.
- A scheduled job (daily) computes aggregates and populates `AirQualityDailyStats`.
- Backend endpoints read both current readings and aggregated stats.

### 3.5. Logging

Backend and ingestion services must log at least:

- External API calls (success and failures).
- Validation errors.
- Database errors.
- Important HTTP requests (method, path, status).

---

## 4. Global frontend design system and styles

The frontend should use a **dark, data-dashboard-inspired style**, with city-at-night and environmental-data vibes.

### 4.1. Color palette (design tokens)

Define reusable design tokens (preferably via CSS custom properties) with the following values:

- **Brand / Status colors**
  - Primary / Brand Teal: `#00897B`
  - Secondary / Fresh Green: `#43A047`
  - Accent / Warning Amber: `#FFB300`
  - Accent / Danger Red: `#E53935`
  - Info Blue (optional): `#1E88E5`

- **Neutrals**
  - App Background (dark): `#0B1020`
  - Card / Surface: `#121826`
  - Border / Divider: `#273043`
  - Text Primary: `#F5F7FA`
  - Text Secondary: `#B0BEC5`
  - Light Background (small areas only): `#F4F6FB`

When generating Vue components or CSS:

- **Always use tokens**, not raw hex codes, inside application styles.
- Introduce a global file (e.g., `frontend/src/styles/tokens.css`) that defines variables like:

  ```css
  :root {
    --color-primary-teal: #00897B;
    --color-secondary-green: #43A047;
    --color-accent-amber: #FFB300;
    --color-accent-red: #E53935;
    --color-info-blue: #1E88E5;

    --color-bg-app: #0B1020;
    --color-bg-surface: #121826;
    --color-border-subtle: #273043;
    --color-text-primary: #F5F7FA;
    --color-text-secondary: #B0BEC5;
    --color-bg-light: #F4F6FB;

    --radius-sm: 6px;
    --radius-md: 10px;
    --radius-lg: 16px;

    --space-1: 4px;
    --space-2: 8px;
    --space-3: 12px;
    --space-4: 16px;
    --space-5: 24px;
    --space-6: 32px;
  }
    ```

### 4.2. Typography and layout style

* Use a modern geometric sans-serif such as **Inter** or **Roboto**.
* Styling:

  * Flat, minimal, avoid heavy gradients or noisy shadows.
  * Use **subtle rounded corners** (e.g., `--radius-md` or `--radius-lg`).
  * Soft, low-elevation shadows for cards (optional).
  * Dark background (`--color-bg-app`) with lighter surfaces for cards (`--color-bg-surface`).

### 4.3. Color usage rules

* Use **Primary Teal** for main actions (primary buttons, active navigation, key highlights).
* Use **Green / Amber / Red** primarily for **air-quality status** (badges, chips, chart segments).
* Ensure sufficient **contrast** for accessibility on dark backgrounds.
* Reserve **Info Blue** for secondary informational accents (links, info badges).

### 4.4. CSS methodology and code organization

When generating frontend code:

* Use **design tokens + CSS custom properties** instead of hard-coded values.
* Use a **consistent class naming methodology**, e.g. **BEM** (`block__element--modifier`) for custom CSS.
* Prefer **component-scoped styles** in Vue SFCs, but extract shared utilities into global styles or a design system layer.
* Keep spacing consistent by relying on spacing tokens (`--space-*`).
* Make layouts **responsive** (desktop-first with proper collapse for tablet and mobile).

---

## 5. Key frontend views and features

The frontend routing and views should include at least:

* `LoginView`

  * Simple login form: “Email”, “Password”, “Sign in”.
* `CitizenDashboardView`

  * Current AQI in user’s city.
  * Nearby stations list.
  * Health recommendation based on AQI.
  * Simple product suggestion (e.g., “Basic mask”, “Specialized respirator”).
* `ResearcherDashboardView`

  * Filters by city, station, date range, pollutant.
  * Charts based on `AirQualityDailyStats` (e.g., line chart for `avg_aqi`).
  * Button to export aggregated data as CSV.
* `AdminDashboardView`

  * CRUD for `Station`.
  * User list (`AppUser`) & role assignment.
  * Basic configuration of alert thresholds.
* `SettingsView`

  * User preferences: theme (light/dark), default city, notification channels.
  * These connect to the NoSQL-based `user_preferences` and `dashboard_configs` APIs.

Organize Vue code in folders such as `views/`, `components/`, `services/` (for API calls), and `store/` or equivalent state management.

---

## 6. Backend (FastAPI) – Required endpoints

Implement REST endpoints in English, for example:

* **Authentication**

  * `POST /api/auth/login`
  * `GET /api/auth/me` (returns current logged-in user)

* **Air quality data**

  * `GET /api/stations`
  * `GET /api/stations/{id}/readings/current`
  * `GET /api/air-quality/current` (by city or user location)
  * `GET /api/air-quality/daily-stats` (filters by station, pollutant, date range)

* **Recommendations**

  * `GET /api/recommendations/current`
  * `GET /api/recommendations/history`

* **Admin**

  * `GET /api/admin/stations`
  * `POST /api/admin/stations`
  * `PUT /api/admin/stations/{id}`
  * `DELETE /api/admin/stations/{id}`
  * `GET /api/admin/users`
  * `PUT /api/admin/users/{id}/role`

* **Settings (NoSQL-backed)**

  * `GET /api/settings/preferences`
  * `PUT /api/settings/preferences`
  * `GET /api/settings/dashboard`
  * `PUT /api/settings/dashboard`

* **Reports**

  * `POST /api/reports`
  * `GET /api/reports`

---

## 7. Design patterns (mandatory)

The project must implement at least **5 distinct design patterns** in frontend or backend (or both). Do **not** use Singleton. **Factory** and **Abstract Factory** count as a single pattern.

When generating code, clearly mark where each pattern is used with comments.

Suggested patterns:

1. **Factory / Abstract Factory**

   * Backend: e.g., `RecommendationFactory` creating different recommendation objects or responses depending on AQI ranges.

2. **Builder**

   * Backend: e.g., `DashboardResponseBuilder` assembling complex responses for `GET /api/air-quality/current` by combining readings, aggregates and recommendations.

3. **Strategy**

   * Backend: e.g., `RiskCategoryStrategy` interface with multiple implementations (simple AQI categorization, WHO-based categorization, custom rules).

4. **Adapter**

   * Ingestion service: e.g., `ExternalApiAdapter` classes adapting different external provider responses into a common internal format (DTO) before saving to DB.

5. **Prototype**

   * Backend or frontend: e.g., cloning a default dashboard configuration (`DefaultDashboardConfig`) or recommendation template and customizing it per user.

**Important:** Each pattern must have a clear, well-documented role and not be a disguised duplicate of another.

---

## 8. General coding guidelines

When generating code for this repository:

* Keep **names, comments and documentation in English**.
* Respect the **repository structure** and do not introduce new top-level folders without clear justification.
* Use **type hints** in Python and prefer explicit Pydantic models for request/response bodies.
* In Vue, prefer **composition API** and strongly typed interfaces (if using TypeScript).
* Reuse **design tokens and utilities** instead of hard-coding style values.
* Avoid including heavy or unnecessary libraries; prefer simple, well-known, lightweight tools.

Whenever you generate or modify code, ensure it:

* Aligns with the architecture and data model described above.
* Uses the color palette and styling methodology for any UI-related pieces.
* Keeps endpoints and data contracts consistent across frontend, backend and ingestion code.