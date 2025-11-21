# Air Quality Platform – Ingestion Service Copilot Instructions

You are working **inside the `ingestion/` folder** of a monorepo for the project **“Air Quality Platform”**.

Your job is to implement an **independent ingestion service** (no public HTTP API) that:

- Fetches air quality data from **external APIs**.
- Normalizes and validates the data.
- Inserts rows into the **PostgreSQL + PostGIS** database defined by the DBML schema.
- Optionally computes and updates **daily aggregates** in `AirQualityDailyStats`.

The ingestion service must **not** change the database schema.  
It must **only read and write** using the existing tables:

- Read: `Station`, `Pollutant` (and optionally `MapRegion`).
- Write: `AirQualityReading`, `AirQualityDailyStats` (and only these for core flow).

---

## 1. Tech stack and project structure

Use:

- **Python 3.11+** (or 3.12).
- A modern HTTP client (e.g. `httpx` or `requests`) to call external APIs.
- **SQLAlchemy** (or the same ORM stack used by the backend) to connect to PostgreSQL.
- Standard Python `logging` for logs.
- Optional: `Pydantic` models for normalized DTOs.
- Optional: `APScheduler` or similar for internal scheduling (or rely on external cron/Kubernetes jobs).

Recommended structure under `ingestion/`:

```text
ingestion/
  app/
    main.py                 # entry point for a single ingestion run
    config.py               # environment and provider configuration
    logging_config.py
    db/
      session.py            # connection to the same DB as backend
      models.py             # minimal ORM models or reuse backend models via import
    domain/
      dto.py                # Pydantic models for normalized readings
      normalization.py      # unit conversion, timezone normalization, AQI calc helpers
    providers/
      base_adapter.py       # BaseExternalApiAdapter (Adapter pattern)
      provider_a_adapter.py # e.g. generic external provider A
      provider_b_adapter.py # e.g. generic external provider B
      factory.py            # small factory to instantiate adapters based on config
    services/
      ingestion_service.py  # orchestration of ingestion flow
      aggregation_service.py# optional: computes AirQualityDailyStats
    __main__.py             # optional: makes `python -m ingestion.app` work
Dockerfile
````

You may adjust the exact file names, but keep these concepts:

* **`providers/`** → external API adapters (Adapter pattern).
* **`domain/`** → internal DTOs and normalization logic.
* **`services/`** → orchestration (fetch + normalize + persist).
* **`db/`** → DB connection and minimal models.

---

## 2. Configuration and environment

All runtime configuration must come from **environment variables** or simple config files.
Create `app/config.py` with a Pydantic `BaseSettings` class similar to:

* Database:

  * `DATABASE_URL` (preferred), or alternatively:

    * `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`.
* External providers:

  * `PROVIDER_A_BASE_URL`, `PROVIDER_A_API_KEY`, etc.
  * `PROVIDER_B_BASE_URL`, `PROVIDER_B_API_KEY`, etc.
* Ingestion behavior:

  * `INGESTION_DEFAULT_CITY` or list of cities/regions to ingest.
  * `INGESTION_TIME_WINDOW_MINUTES` (e.g., last 60 minutes).
  * `INGESTION_LOG_LEVEL`.

The ingestion service **must not** hard-code API keys or credentials.

---

## 3. Database integration (aligned with DBML)

The ingestion service uses the same PostgreSQL schema as the backend.
The DBML model is the **source of truth**:

```dbml
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
  geom geometry
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

In the ingestion service:

* **Read**:

  * `Station` → to map external station identifiers to internal `station_id`.
  * `Pollutant` → to map external pollutant names/codes and units to `pollutant_id`.
  * Optionally `MapRegion` or `Station` lat/long for geospatial checks.

* **Write**:

  * `AirQualityReading` → each new reading ingested from external APIs.
  * `AirQualityDailyStats` → aggregated stats (if the aggregation job runs in this service).

Do **not** alter tables, add columns, or create new tables from the ingestion service.
All schema creation and seeding is handled by database scripts / migrations.

---

## 4. Internal data model and normalization

To keep ingestion logic clean, define **internal DTOs** in `domain/dto.py` using Pydantic, e.g.:

```python
from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class NormalizedReading(BaseModel):
  external_station_id: str
  station_name: Optional[str]
  latitude: Optional[float]
  longitude: Optional[float]
  city: Optional[str]
  country: Optional[str]

  pollutant_code: str       # e.g. "PM2.5", "PM10"
  unit: str                 # e.g. "µg/m³", "ppm"
  value: float
  aqi: Optional[int]        # computed or provided by provider
  timestamp_utc: datetime
```

### 4.1. Normalization rules

In `domain/normalization.py`, implement helper functions to:

* Convert timestamps to **UTC**.
* Standardize pollutant names and codes.

  * Map provider-specific keys (e.g. `"pm25"`, `"pm10"`, `"o3"`) to canonical names `"PM2.5"`, `"PM10"`, `"O3"`, etc.
* Convert units if needed:

  * Ensure `value` corresponds to the unit stored in `Pollutant.unit`.
  * If the provider uses different units, apply the correct conversion factor.
* Compute AQI if the provider does not provide it:

  * Provide a simple, documented algorithm (approximate) or leave `aqi = None` and log a warning, depending on requirements.

The ingestion service must ensure:

* No obviously invalid values:

  * Discard or flag rows with negative concentrations or impossible AQI values.
  * Log validation errors.
* Normalize **station identity**:

  * Use external station ID + city + coordinates to match existing `Station` rows.
  * If a station is not found, log a warning and optionally skip or create it (creation is allowed only if agreed; by default prefer skipping and logging).

---

## 5. Adapter pattern for external providers (mandatory design pattern)

The ingestion service must implement the **Adapter** pattern for different external APIs.

### 5.1. Base adapter interface

In `providers/base_adapter.py`, define an abstract base class:

```python
from abc import ABC, abstractmethod
from typing import List
from ingestion.app.domain.dto import NormalizedReading

class BaseExternalApiAdapter(ABC):
    """Adapter pattern: unifies different external air quality APIs into a common model."""

    @abstractmethod
    async def fetch_readings(self) -> List[NormalizedReading]:
        """Fetch and normalize readings from the external API into NormalizedReading objects."""
        ...
```

Add a clear comment in the file that this is the **Adapter pattern implementation**.

### 5.2. Concrete adapters

Create one file per provider, e.g.:

* `providers/provider_a_adapter.py`
* `providers/provider_b_adapter.py`

Each must:

* Call the external API using `httpx` or `requests`.
* Handle authentication (API key, token, etc.) via environment variables.
* Parse provider-specific JSON responses.
* Build and return a `List[NormalizedReading]`.

Example pattern (simplified):

```python
class ProviderAAdapter(BaseExternalApiAdapter):
    async def fetch_readings(self) -> List[NormalizedReading]:
        # 1. Call external API (GET, including key, location parameters, etc.)
        # 2. Parse JSON payload
        # 3. For each measurement, create NormalizedReading using normalization helpers
        # 4. Return list of NormalizedReading
        ...
```

### 5.3. Adapter factory

In `providers/factory.py`, implement a small factory function to instantiate adapters based on config, for example:

```python
from typing import List
from .base_adapter import BaseExternalApiAdapter
from .provider_a_adapter import ProviderAAdapter
from .provider_b_adapter import ProviderBAdapter
from ingestion.app.config import settings

def get_active_adapters() -> List[BaseExternalApiAdapter]:
    adapters: List[BaseExternalApiAdapter] = []
    if settings.PROVIDER_A_ENABLED:
        adapters.append(ProviderAAdapter(...))
    if settings.PROVIDER_B_ENABLED:
        adapters.append(ProviderBAdapter(...))
    return adapters
```

This keeps `main.py` and `ingestion_service.py` independent from concrete provider implementations.

---

## 6. Ingestion flow (service orchestration)

Create `services/ingestion_service.py` to orchestrate the full ingestion run.

Steps for a single ingestion run:

1. **Load configuration** (DB URL, providers, regions/cities) from `config.py`.
2. **Create DB session** using `db/session.py`.
3. **Get active adapters** from `providers/factory.py`.
4. For each adapter:

   * Call `fetch_readings()` to obtain `List[NormalizedReading]`.
5. For all normalized readings:

   * **Map to internal IDs**:

     * Find or match `Station.id` based on city + coordinates + station name, or an external ID mapping table if one is added.
     * Look up `Pollutant.id` by canonical `pollutant_code` (e.g., `PM2.5`, `O3`).
   * Validate and filter:

     * Discard invalid readings (log them).
   * Insert into `AirQualityReading`:

     * Use bulk inserts when possible.
6. Commit DB transaction.
7. Optionally trigger **aggregation** (daily stats) in the same run or as a separate job.

In `app/main.py`:

* Implement a `run_ingestion()` function that executes these steps.
* Provide a CLI-friendly entry point (e.g., `if __name__ == "__main__": run_ingestion()`).
* Optionally allow CLI args or env flags (e.g., `--city=Bogotá`, `--once` vs `--loop`).

---

## 7. Daily aggregation to AirQualityDailyStats (optional but recommended)

Implement `services/aggregation_service.py` to populate `AirQualityDailyStats`:

* Reads from `AirQualityReading`.
* Groups by:

  * `station_id`
  * `pollutant_id`
  * `date` (based on `datetime` truncated to date).
* Computes:

  * `avg_value`
  * `avg_aqi`
  * `max_aqi`
  * `min_aqi`
  * `readings_count`

This can be done via:

* A direct SQL query (GROUP BY) and insert/update into `AirQualityDailyStats`.
* Or via an ORM query, depending on performance needs.

The aggregation job can be:

* A separate entry point (e.g., `run_daily_aggregation()`).
* Or part of the same script with a mode flag.

The ingestion service must only **write** into `AirQualityDailyStats`; it must not alter its schema.

---

## 8. Error handling and logging

Use Python’s `logging` module, configured in `logging_config.py`.

Log levels:

* Info:

  * Start and end of ingestion runs.
  * Number of readings fetched per provider.
  * Number of readings successfully inserted.
* Warning:

  * Missing station mappings.
  * Missing pollutant mappings.
  * Invalid or discarded readings.
* Error:

  * External API failures.
  * Database connection or transaction failures.
  * Unhandled exceptions.

Error handling:

* For each provider, catch network/API errors and:

  * Log the error.
  * Continue with other providers, unless explicitly configured to fail fast.
* For DB operations:

  * Use transactions; rollback on failure.
  * Ensure the process exits with a non-zero code if the ingestion failed completely.

---

## 9. Scheduling and running the ingestion

The ingestion service should be **stateless** between runs. Scheduling can be handled by:

* External tools: cron, systemd timers, Kubernetes CronJobs, etc.
* Or a simple internal loop with sleep (less recommended), clearly documented.

The container must be able to:

* Run a **single ingestion run** (one-shot mode) when executed.
* Optionally, accept a mode parameter (env or CLI) for:

  * `INGEST_ONCE`
  * `RUN_AGGREGATION`
  * `LOOP` (if a simple internal schedule is needed).

---

## 10. Dockerfile for the ingestion service

Create `ingestion/Dockerfile` that:

* Uses a slim Python base image (e.g. `python:3.12-slim`).
* Installs dependencies from `requirements.txt` or `pyproject.toml`.
* Sets `PYTHONUNBUFFERED=1`.
* Uses an entrypoint that runs `python -m ingestion.app.main` or similar.

The container should rely on environment variables for:

* DB connectivity.
* Provider base URLs and keys.
* Ingestion options (cities, time windows, etc.).

---

## 11. General ingestion rules

Whenever you generate or modify ingestion code:

* Keep names, comments and documentation **in English**.
* Do **not** change the DB schema; use the existing tables as defined in the DBML.
* Clearly implement and document the **Adapter pattern** in `providers/`.
* Keep the ingestion flow **idempotent-friendly**:

  * If the same data is ingested twice, it should not break the system:

    * Either detect duplicates, or allow harmless overwrites by using composite uniqueness if available (e.g. `(station_id, pollutant_id, datetime)`).
* Do not embed UI or HTTP server logic in this service; it is a **background data pipeline**.
* Prefer simple, readable code that students can understand and extend.

```