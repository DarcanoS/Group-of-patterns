# Air Quality Platform – Database Copilot Instructions

You are setting up the **relational database schema and seed data** for the project **“Air Quality Platform”**.

The database engine is **PostgreSQL** with **PostGIS** enabled for geospatial features.

Your tasks:

1. Create SQL scripts (or migrations) to define the **database schema** based on the DBML model below.
2. Create SQL scripts (or a small seed script in Python) to insert **initial reference data** required for the app to work and be testable (roles, basic permissions, pollutants, a couple of regions, stations, users, and sample readings).

All table and column names must match the DBML exactly.

---

## 1. Target environment and conventions

- Use **PostgreSQL 14+** with **PostGIS**.
- Use a single schema (e.g. `public`).
- Use modern identity columns instead of old-style `SERIAL`, for example:

  ```sql
  id integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY
````

* Enable PostGIS in the database:

  ```sql
  CREATE EXTENSION IF NOT EXISTS postgis;
  ```

* Use `timestamp with time zone` (`timestamptz`) for timestamps unless there is a clear reason to use `timestamp without time zone`.

* Use `varchar` lengths where appropriate (e.g. `varchar(255)`), or just `text` when the length is not constrained and the DBML specifies `varchar` generically.

---

## 2. DBML model (source of truth)

Base the schema directly on this DBML:

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

// Generic recommendation to the user based on pollution level,
// e.g. "use a basic mask" or "avoid outdoor exercise".
Table Recommendation {
  id int [pk]
  user_id int [ref: > AppUser.id]
  location varchar       // city or area name
  pollution_level int    // e.g. AQI value used to choose the advice
  message text           // human-readable recommendation
  created_at timestamp
}

// Simple mapping from a recommendation to a suggested protection product,
// for example: normal mask vs specialized mask.
Table ProductRecommendation {
  id int [pk]
  recommendation_id int [ref: > Recommendation.id]
  product_name varchar       // e.g. 'Basic Face Mask'
  product_type varchar       // e.g. 'mask', 'respirator'
  product_url varchar        // optional: informational link
}

//// REPORTING & ANALYTICS

// Operational report metadata (no JSON).
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

// Analytical aggregated data for BI (analytical domain).
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

---

## 3. Schema creation – SQL script

Create a SQL script (for example `backend/db/init_schema.sql` or a first migration file) that:

1. **Creates the PostGIS extension**:

   ```sql
   CREATE EXTENSION IF NOT EXISTS postgis;
   ```

2. **Creates all tables** in a sensible dependency order (e.g., `MapRegion` and `Pollutant` before `Station`; `Station` before `AirQualityReading`; `Role` and `Permission` before `RolePermission`; etc.).

3. Uses proper PostgreSQL types:

   * `int` → `integer` (with `GENERATED ALWAYS AS IDENTITY` for primary keys).
   * `float` → `double precision` (or `real` if preferred, but choose consistently).
   * `timestamp` → `timestamp with time zone`.
   * `varchar` → `varchar(255)` unless there is a clear reason to use a different length. For free-form long text, use `text`.

4. Implements the `geom` field on `MapRegion` as a geospatial column, for example:

   ```sql
   geom geometry(MultiPolygon, 4326)
   ```

   or

   ```sql
   geom geometry(Polygon, 4326)
   ```

   (Choose one consistently and document it in a comment.)

5. Declares all **primary keys** and **foreign keys** exactly as in the DBML.

6. Adds **NOT NULL** constraints where it makes sense for core fields (e.g., names, foreign keys, timestamps), while allowing `NULL` on fields that are truly optional.

7. Enforces **uniqueness** where specified in DBML:

   * `Role.name` unique.
   * `Permission.name` unique.
   * Optionally consider `AppUser.email` as unique.

8. Creates helpful indexes:

   * Indexes on foreign key columns: `station_id`, `pollutant_id`, `user_id`, `role_id`, etc.
   * Indexes on time-related columns:

     * `AirQualityReading.datetime`
     * `AirQualityDailyStats.date`
   * Optional composite indexes frequently used by queries (e.g., `(station_id, pollutant_id, datetime)`).

9. Uses **ON DELETE** behavior explicitly for foreign keys (e.g., `ON DELETE CASCADE` or `ON DELETE RESTRICT`) where appropriate, and document choices with comments.

Example structure for one table (for guidance):

```sql
CREATE TABLE station (
  id integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  name varchar(255) NOT NULL,
  latitude double precision NOT NULL,
  longitude double precision NOT NULL,
  city varchar(255) NOT NULL,
  country varchar(255) NOT NULL,
  region_id integer REFERENCES map_region (id)
);

CREATE INDEX idx_station_region_id ON station (region_id);
```

---

## 4. Seed data – initial content for development

Create a **separate script** (for example `backend/db/seed_data.sql`) or a **Python script** (`backend/app/db/seed_data.py`) that inserts **initial data** that is useful for development and demos.

The goal is **not** to create a huge dataset, but to have realistic starting data.

### 4.1. Roles

Insert at least these roles into `Role`:

* `Citizen`
* `Researcher`
* `Admin`

Example:

```sql
INSERT INTO role (name)
VALUES ('Citizen'), ('Researcher'), ('Admin')
ON CONFLICT (name) DO NOTHING;
```

### 4.2. Permissions

Define a minimal set of permissions in `Permission`, for example:

* `VIEW_CITIZEN_DASHBOARD`
* `VIEW_RESEARCHER_DASHBOARD`
* `VIEW_ADMIN_DASHBOARD`
* `MANAGE_STATIONS`
* `MANAGE_USERS`
* `MANAGE_ALERTS`

Map roles to permissions in `RolePermission`, e.g.:

* `Citizen` → `VIEW_CITIZEN_DASHBOARD`
* `Researcher` → `VIEW_RESEARCHER_DASHBOARD`
* `Admin` → all permissions

You may use subqueries or placeholders to look up IDs by name.

### 4.3. Pollutants

Insert a small catalog of common pollutants into `Pollutant`, e.g.:

* `PM2.5` – µg/m³
* `PM10` – µg/m³
* `O3` – ppb
* `NO2` – ppb
* `SO2` – ppb
* `CO` – ppm

Example:

```sql
INSERT INTO pollutant (name, unit, description) VALUES
  ('PM2.5', 'µg/m³', 'Fine particulate matter less than 2.5 micrometers'),
  ('PM10', 'µg/m³', 'Particulate matter less than 10 micrometers'),
  ('O3', 'ppb', 'Ozone'),
  ('NO2', 'ppb', 'Nitrogen dioxide'),
  ('SO2', 'ppb', 'Sulfur dioxide'),
  ('CO', 'ppm', 'Carbon monoxide')
ON CONFLICT (name) DO NOTHING;
```

### 4.4. Regions and stations

Insert at least one `MapRegion` and a few `Station` rows.

* Example region: `Bogotá Metropolitan Area` with a simple placeholder geometry (e.g., a sample polygon).
* Example stations (enable easy testing):

  * `Bogotá Downtown Station`
  * `Bogotá North Station`

Use realistic latitude/longitude values (not necessarily precise, but plausible).

### 4.5. Users

Insert a few `AppUser` rows, one per role:

* Citizen test user (`demo.citizen@example.com`)
* Researcher test user (`demo.researcher@example.com`)
* Admin test user (`demo.admin@example.com`)

For `password_hash`, you can:

* Use a precomputed bcrypt hash for a known password (e.g., `"changeme"`).
* Or use placeholder hashes and document them in comments.

Example (pseudo):

```sql
INSERT INTO app_user (name, email, password_hash, location, role_id)
VALUES
  ('Demo Citizen', 'demo.citizen@example.com', '<bcrypt_hash_here>', 'Bogotá', <citizen_role_id>),
  ('Demo Researcher', 'demo.researcher@example.com', '<bcrypt_hash_here>', 'Bogotá', <researcher_role_id>),
  ('Demo Admin', 'demo.admin@example.com', '<bcrypt_hash_here>', 'Bogotá', <admin_role_id>);
```

If using a Python seeding script, generate the hashes programmatically using `passlib` or similar.

### 4.6. Sample readings and daily stats

Insert sample data into `AirQualityReading` and `AirQualityDailyStats` for at least one station and a couple of days:

* A few rows for today and previous days.
* Use consistent station IDs and pollutant IDs.
* Use reasonable AQI and value ranges.

Example ideas:

* AQI values: 40–160.
* `readings_count` in `AirQualityDailyStats`: 24 for hourly aggregated data.

### 4.7. Sample alerts and recommendations

Insert a small number of rows into:

* `Alert` (e.g., an alert for high PM2.5 for the demo citizen).
* `Recommendation` and `ProductRecommendation` to illustrate a mapping between an AQI-based advice and a product suggestion.

Example:

```sql
INSERT INTO recommendation (user_id, location, pollution_level, message, created_at)
VALUES
  (<citizen_user_id>, 'Bogotá', 120, 'AQI is unhealthy for sensitive groups. Consider limiting outdoor exercise.', NOW());

INSERT INTO product_recommendation (recommendation_id, product_name, product_type, product_url)
VALUES
  (<recommendation_id>, 'Basic Face Mask', 'mask', 'https://example.com/basic-mask');
```

### 4.8. Sample reports

Insert 1–2 rows into `Report` to show how metadata is stored (file_path can be a placeholder):

```sql
INSERT INTO report (user_id, created_at, city, start_date, end_date, station_id, pollutant_id, file_path)
VALUES
  (<researcher_user_id>, NOW(), 'Bogotá', CURRENT_DATE - INTERVAL '7 days', CURRENT_DATE, <station_id>, <pollutant_id>, '/reports/sample-report-1.csv');
```

---

## 5. Integration with backend code

When generating backend code (e.g., SQLAlchemy models or Alembic migrations):

* Ensure that the model definitions **match this schema** exactly.
* If both raw SQL and ORM models are present, keep them consistent in naming and types.
* The backend should read and write data to these tables without requiring manual changes to the schema.

---

## 6. Output expectations

When prompted to generate DB scripts or migrations, you should:

1. Produce a **schema creation script** that is idempotent enough for local development (e.g., using `IF NOT EXISTS` where appropriate).
2. Produce a **seed data script** that can be run safely multiple times (using `ON CONFLICT DO NOTHING` or equivalent).
3. Ensure that the scripts are clearly separated and easy for students to run (e.g., documented commands such as `psql -f backend/db/init_schema.sql` then `psql -f backend/db/seed_data.sql`).

Keep everything aligned with the DBML model and with the rest of the Air Quality Platform architecture.

```