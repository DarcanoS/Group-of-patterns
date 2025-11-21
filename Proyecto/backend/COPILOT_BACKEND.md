# Air Quality Platform – Backend Copilot Instructions

You are working **inside the `backend/` folder** of a monorepo for the project **“Air Quality Platform”**.

Your job is to implement the **REST API** using **Python + FastAPI**, connected to **PostgreSQL with PostGIS**, and following:

- The global architecture and data model in `docs/copilot-global.md`.
- The **database schema and seed instructions** in `COPILOT_DATABASE.md` (or equivalent).

> **Important:**  
> The **DBML model and database scripts** are the source of truth for the relational schema.  
> ORM models and migrations must **match that schema exactly** (table names, column names, types and relationships).

All API field names, endpoints and documentation must be in **English**.

---

## 1. Tech stack and project structure

Use:

- **Python 3.11+** (or 3.12).
- **FastAPI** for the web framework.
- **Uvicorn** as the ASGI server.
- **SQLAlchemy** (or SQLModel / similar) for ORM.
- **Alembic** (optional, recommended) for migrations.
- **Pydantic** models for request/response schemas.
- Standard Python `logging` for logs.

Recommended project structure under `backend/`:

```text
backend/
  app/
    main.py
    core/
      config.py
      logging_config.py
      security.py
    db/
      base.py
      session.py
      init_db.py   # optional helper to run seed / migrations
    models/
      station.py
      region.py
      pollutant.py
      air_quality_reading.py
      user.py
      role.py
      permission.py
      alert.py
      recommendation.py
      product_recommendation.py
      report.py
      daily_stats.py
      __init__.py
    schemas/
      station.py
      region.py
      pollutant.py
      air_quality.py
      user.py
      auth.py
      alert.py
      recommendation.py
      report.py
      settings.py
      common.py
      __init__.py
    repositories/
      station_repository.py
      user_repository.py
      air_quality_repository.py
      report_repository.py
      alert_repository.py
      __init__.py
    services/
      auth_service.py
      air_quality_service.py
      recommendation_service/
        factory.py
        models.py
      dashboard_service/
        builder.py
        prototype.py
      risk_category/
        strategies.py
        interfaces.py
      reporting/
        report_service.py
      settings_service.py
      __init__.py
    api/
      deps.py
      v1/
        router.py
        endpoints/
          auth.py
          stations.py
          air_quality.py
          recommendations.py
          admin.py
          settings.py
          reports.py
    tests/
      ...
```

You may adjust file names as needed, but keep this layered structure:

* **`models/`** → ORM models (mirror DBML schema).
* **`schemas/`** → Pydantic schemas.
* **`repositories/`** → DB access logic.
* **`services/`** → business logic and design patterns.
* **`api/v1/endpoints/`** → FastAPI routers for each domain.

---

## 2. Configuration and environment

Create a central configuration module, e.g. `app/core/config.py`, using Pydantic `BaseSettings`:

Environment variables to support (at least):

* `API_V1_STR` (e.g. `/api`)
* `BACKEND_CORS_ORIGINS`
* `DATABASE_URL` (PostgreSQL + PostGIS connection string)
* `JWT_SECRET_KEY`, `JWT_ALGORITHM`, `ACCESS_TOKEN_EXPIRE_MINUTES` (if using JWT)
* Optional: `NOSQL_URI`, `NOSQL_DB_NAME` (for future NoSQL integration)

In `app/db/session.py`:

* Create the SQLAlchemy engine and sessionmaker using `DATABASE_URL`.
* Do **not** create or modify tables directly here; schema is defined by migrations / SQL scripts.

---

## 3. Database modeling (PostgreSQL + PostGIS, DBML-aligned)

The relational schema is defined by the **DBML model** and the database instructions. ORM models must reflect the following tables **exactly**:

### 3.1. Tables (from DBML)

```dbml
//// GEOSPATIAL & MONITORING (Operational)

Table Station {
  id int [pk]
  name varchar
  latitude float
  longitude float
  city varchar
  country varchar
  region_id int [ref: > MapRegion.id]
}

Table AirQualityReading {
  id int [pk]
  station_id int [ref: > Station.id]
  pollutant_id int [ref: > Pollutant.id]
  datetime timestamp
  value float
  aqi int
}

Table Pollutant {
  id int [pk]
  name varchar
  unit varchar
  description text
}

Table MapRegion {
  id int [pk]
  name varchar
  geom geometry // optional: for advanced geospatial visualizations (PostGIS)
}

//// USERS & ACCESS CONTROL (Operational)

Table AppUser {
  id int [pk]
  name varchar
  email varchar
  password_hash varchar
  location varchar
  role_id int [ref: > Role.id]
}

Table Role {
  id int [pk]
  name varchar [unique]
}

Table Permission {
  id int [pk]
  name varchar [unique]
}

Table RolePermission {
  role_id int [ref: > Role.id]
  permission_id int [ref: > Permission.id]
  primary key (role_id, permission_id)
}

//// ALERTS & PERSONALIZATION (Operational)

Table Alert {
  id int [pk]
  user_id int [ref: > AppUser.id]
  pollutant_id int [ref: > Pollutant.id]
  threshold float
  method varchar        // e.g. 'email', 'sms'
  triggered_at timestamp
}

Table Recommendation {
  id int [pk]
  user_id int [ref: > AppUser.id]
  location varchar       // city or area name
  pollution_level int    // e.g. AQI value used to choose the advice
  message text           // human-readable recommendation
  created_at timestamp
}

Table ProductRecommendation {
  id int [pk]
  recommendation_id int [ref: > Recommendation.id]
  product_name varchar       // e.g. 'Basic Face Mask'
  product_type varchar       // e.g. 'mask', 'respirator'
  product_url varchar        // optional: informational link
}

//// REPORTING & ANALYTICS

Table Report {
  id int [pk]
  user_id int [ref: > AppUser.id]
  created_at timestamp
  city varchar
  start_date date
  end_date date
  station_id int [ref: > Station.id]
  pollutant_id int [ref: > Pollutant.id]
  file_path varchar
}

Table AirQualityDailyStats {
  id int [pk]
  station_id int [ref: > Station.id]
  pollutant_id int [ref: > Pollutant.id]
  date date
  avg_value float
  avg_aqi int
  max_aqi int
  min_aqi int
  readings_count int
}
```

### 3.2. ORM model requirements

When generating SQLAlchemy (or similar) models:

* **Table names** must match the DBML names exactly:

  * `station`, `air_quality_reading`, `pollutant`, `map_region`, `app_user`, `role`, `permission`, `role_permission`, `alert`, `recommendation`, `product_recommendation`, `report`, `air_quality_daily_stats`.
* **Column names** must match: `pollution_level`, `password_hash`, `geom`, etc.
* Use appropriate PostgreSQL types:

  * `int` → `Integer`
  * `float` → `Float` or `Double` (consistent with the schema script)
  * `timestamp` → `TIMESTAMP(timezone=True)` (i.e. `timestamptz`) where possible
  * `date` → `Date`
  * `geometry` → PostGIS geometry type via SQLAlchemy-GeoAlchemy2 (or similar)
* Add relationships using `relationship()` where convenient, but **do not** introduce extra columns.

**Uniqueness & indices:**

* Honor uniqueness from DBML:

  * `Role.name` unique
  * `Permission.name` unique
* Recommendation:

  * Enforce `AppUser.email` as unique at the ORM or DB level (even if DBML does not explicitly say so, it is safe and useful).
* Add indexes in migrations or schema scripts according to `COPILOT_DATABASE.md`:

  * Foreign key columns (`station_id`, `pollutant_id`, `user_id`, `role_id`, etc.).
  * Time columns like `AirQualityReading.datetime` and `AirQualityDailyStats.date`.

**PostGIS:**

* `MapRegion.geom` must be mapped as a geometry field compatible with PostGIS, e.g. using `Geometry('MULTIPOLYGON', 4326)` or similar.

> Do **not** change the schema shape from what the DB scripts define.
> If you need extra derived data, compute it in queries/services, not as new columns.

---

## 4. API design (FastAPI routers)

Use **versioned routing** under `/api/v1`. Define routers in `app/api/v1/endpoints/` and include them in `app/api/v1/router.py`.

### 4.1. Authentication

Endpoints:

* `POST /api/auth/login`

  * Accepts email + password.
  * Returns an access token (JWT or stub) and user info, or an appropriate error.
* `GET /api/auth/me`

  * Returns the current authenticated user (using `AppUser`).

You may implement a **simple auth** (not production-grade) but keep it ready for real JWT.

### 4.2. Air quality data

Endpoints:

* `GET /api/stations`

  * List stations (with optional filters by city, country, region, etc.).
* `GET /api/stations/{id}/readings/current`

  * Get the most recent reading per pollutant for a station from `AirQualityReading`.
* `GET /api/air-quality/current`

  * Returns AQI for a given city or location.
* `GET /api/air-quality/daily-stats`

  * Reads from `AirQualityDailyStats` with filters (`station_id`, `pollutant_id`, date range).

### 4.3. Recommendations

Endpoints:

* `GET /api/recommendations/current`

  * Uses current AQI data + design patterns (Factory, Strategy) to generate one recommendation for the current user, and may store it in `Recommendation` and `ProductRecommendation`.
* `GET /api/recommendations/history`

  * Returns a paginated list of previous recommendations for the current user.

### 4.4. Admin functionality

Endpoints under an admin router (e.g. `/api/admin/...`):

* `GET /api/admin/stations`

* `POST /api/admin/stations`

* `PUT /api/admin/stations/{id}`

* `DELETE /api/admin/stations/{id}`

* `GET /api/admin/users`

* `PUT /api/admin/users/{id}/role`

Admin endpoints must require **Admin role**, using role/permission checks based on `Role`, `Permission` and `RolePermission`.

### 4.5. Settings (NoSQL-backed)

These endpoints assume a NoSQL layer for flexible configurations:

* `GET /api/settings/preferences`
* `PUT /api/settings/preferences`
* `GET /api/settings/dashboard`
* `PUT /api/settings/dashboard`

At first, the implementation may:

* Use in-memory mocks or relational tables.
* Maintain the API contract as if it were using NoSQL collections `user_preferences` and `dashboard_configs`.

### 4.6. Reports

Endpoints:

* `POST /api/reports`

  * Creates a report metadata record in `Report` pointing to a file path (placeholder or real).
* `GET /api/reports`

  * Lists existing reports for the current user.

---

## 5. Services, repositories and layering

Follow a clear separation of concerns:

* **Repositories** (`app/repositories/`):

  * Raw DB access using SQLAlchemy sessions.
  * CRUD + specific queries for each table (`Station`, `AirQualityReading`, `AirQualityDailyStats`, etc.).
* **Services** (`app/services/`):

  * Business logic on top of repositories.
  * Use design patterns (Factory, Builder, Strategy, Prototype) as described below.
* **Routers** (`app/api/v1/endpoints/`):

  * HTTP layer (parameters, auth, status codes).
  * Use Pydantic schemas for inputs and outputs.
  * Delegate to services.

Use FastAPI dependencies (`Depends`) for:

* DB session (`get_db`).
* Current user (`get_current_user`).
* Current admin (`get_current_admin` with role check).

---

## 6. Required design patterns in the backend

> **Important:**
>
> * Do **not** use Singleton.
> * **Factory** and **Abstract Factory** together count as **one pattern**.
> * Add clear comments in code indicating where each pattern is implemented.

### 6.1. Factory / Abstract Factory – RecommendationFactory

Location suggestion: `app/services/recommendation_service/factory.py`

Goal:

* Given AQI and context (pollutant, maybe user role), create the appropriate recommendation object/DTO that maps naturally to the `Recommendation` and `ProductRecommendation` tables.

Example:

* Interface: `BaseRecommendation` (fields like `pollution_level`, `message`, optional product info).
* `RecommendationFactory`:

  * `create_for_aqi(aqi: int, user_role: str) -> BaseRecommendation`
* Internally:

  * Chooses among different concrete recommendation classes based on AQI ranges (good, moderate, unhealthy, etc.).

Usage:

* `GET /api/recommendations/current` endpoint calls a service that uses this factory.
* The service may persist the result into `Recommendation` / `ProductRecommendation`.

### 6.2. Builder – DashboardResponseBuilder

Location suggestion: `app/services/dashboard_service/builder.py`

Goal:

* Centralize construction of complex dashboard responses from multiple sources:

  * `Station`
  * `AirQualityReading`
  * `AirQualityDailyStats`
  * Recommendations (via factory)
  * Risk categories (via strategy)

Pattern:

* `DashboardResponseBuilder` with fluent/chained methods:

  * `.with_current_readings(...)`
  * `.with_daily_stats(...)`
  * `.with_recommendation(...)`
  * `.with_risk_category(...)`
  * `.build() -> DashboardResponseSchema`

Usage:

* `GET /api/air-quality/current` receives parameters, fetches data via repositories, and then uses the builder to assemble the response.

### 6.3. Strategy – RiskCategoryStrategy

Location suggestion: `app/services/risk_category/`

Goal:

* Provide interchangeable algorithms to classify AQI values into categories.

Example:

* Strategy interface: `RiskCategoryStrategy`:

  * `get_category(aqi: int) -> RiskCategory`
    (`RiskCategory` can be an enum or Pydantic model with fields like `name`, `label`, `color_hint`).

* Implementations:

  * `SimpleRiskCategoryStrategy` (basic ranges).
  * `WhoRiskCategoryStrategy` (ranges based on WHO guidance).

Usage:

* The RecommendationFactory and/or DashboardResponseBuilder call the active strategy to determine human-readable risk level and color hints (e.g., mapping to green/amber/red).

### 6.4. Prototype – DefaultDashboardConfig

Location suggestion: `app/services/dashboard_service/prototype.py`

Goal:

* Provide a reusable prototype for default dashboard configurations that is easy to clone for new users.

Pattern:

* Define a `DashboardConfigPrototype` or similar that holds a base configuration (e.g., widget layout).
* Provide a `clone()` method that returns a deep copy which can then be customized (e.g., set user’s default city).

Usage:

* When a user first accesses settings or dashboard endpoints, the backend clones the prototype and persists it via the NoSQL (or mock) model for `dashboard_configs`.

---

## 7. Logging and error handling

Logging:

* Configure Python logging in `app/core/logging_config.py`.
* Log:

  * Startup/shutdown.
  * Database connection issues.
  * Repository/service errors.
  * Key business events (report created, alert triggered, recommendation generated).

Error handling:

* Use `HTTPException` for predictable client errors (400, 401, 403, 404).
* Wrap lower-level errors with meaningful messages.
* Do not expose raw stack traces in responses.

---

## 8. Interaction with ingestion service and database scripts

The **ingestion service**:

* Runs independently and writes into `AirQualityReading` and `AirQualityDailyStats`.
* Uses the same schema defined by the DBML and DB scripts.

The **database scripts** (see `COPILOT_DATABASE.md`):

* Create all tables according to the DBML.
* Seed initial data:

  * Roles, permissions.
  * Core pollutants.
  * Example regions and stations.
  * Demo users per role.
  * Sample readings, daily stats, alerts, recommendations and reports.

Backend assumptions:

* You can assume the schema and seed data exist and are up-to-date.
* Do **not** create or alter tables in backend code.
* Do **not** reseed core data in normal API flows; use seeds only for initialization or local dev utilities.

Optionally:

* Expose a simple health/diagnostic endpoint (e.g. `/api/admin/health`) that:

  * Checks DB connectivity.
  * Confirms at least one station and pollutant exist.

---

## 9. Dockerfile for the backend

Create `backend/Dockerfile` that:

* Uses a slim Python base image (e.g. `python:3.12-slim`).
* Installs dependencies from `requirements.txt` or `pyproject.toml`.
* Sets `PYTHONUNBUFFERED=1`.
* Starts the app with something like:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Reads configuration from environment variables (including `DATABASE_URL`).

---

## 10. General backend rules

Whenever you generate or modify backend code:

* Keep names, comments and documentation **in English**.
* Respect the **DBML/DB schema** — do not rename or add columns without updating the central schema first.
* Use **type hints** and **Pydantic schemas** consistently.
* Keep business logic in **services**, not in routers or models.
* Implement and **document** where each design pattern lives (Factory, Builder, Strategy, Prototype).
* Avoid the Singleton pattern.
* Keep code simple enough for students while still reflecting modern FastAPI architecture.