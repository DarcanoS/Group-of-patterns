# COMPLETED: Database Copilot Instructions V2

> **Status:** ✅ **COMPLETED**  
> **Date:** November 26, 2025  
> **Output:** `COPILOT_DATABASE.md` (Version 2)

---

## Overview

This document contained the instructions for updating the database Copilot guidelines for the project **"Air Quality Platform"**.

The task has been **successfully completed**. The updated instructions are now available in:

📄 **`COPILOT_DATABASE.md`** (Version 2 - Current)

✅ **Completed Tasks:**

1. ✅ **Version Note Added** - Clearly marked `COPILOT_DATABASE.md` as version 2 with reference to the original `COPILOT_DATABASE.txt`

2. ✅ **DBML Schema Updated** - Replaced the relational schema with the exact current DBML model including all 14 tables

3. ✅ **Seed Data Removed** - Completely removed all seed data responsibilities from the database Copilot flow

4. ✅ **PostgreSQL + PostGIS + REST-friendly** - Explicitly documented PostgreSQL 14+ with PostGIS and REST-friendly design

5. ✅ **MongoDB Section Added** - New comprehensive section for NoSQL configuration store with collections `user_preferences` and `dashboard_configs`

6. ✅ **Output Expectations Updated** - Modified to generate only schema/migration scripts without seed data

7. ✅ **Summary Section Added** - Included comparison summary between v1 and v2 at the end of the document

---

## Version Comparison

### Version 1 (`COPILOT_DATABASE.txt`)
- PostgreSQL schema with seed data responsibilities
- No explicit REST-friendly design mention
- No MongoDB integration
- Included detailed seed data instructions

### Version 2 (`COPILOT_DATABASE.md`) ✨
- **PostgreSQL 14+ with PostGIS** explicitly stated
- **REST-friendly schema design** (e.g., suitable for PostgREST)
- **MongoDB introduced** for user preferences and dashboard configurations
- **All seed data responsibilities removed** - data population delegated to ingestion pipeline and application services
- Updated DBML model as source of truth
- Clearer separation of concerns between schema definition and data population

---

## Files in Database Folder

```
database/
├── COPILOT_DATABASE.txt         # Version 1 (original, kept for reference)
├── COPILOT_DATABASE.md          # Version 2 (current, use this one) ✨
├── COPILOT_DATABASE_V2.md       # This completion report
├── README.md                    # User-facing setup documentation
├── init_schema.sql              # Schema creation script (to be generated)
└── .env.example                 # Environment variables template
```

---

## Next Steps

The database Copilot is now ready to:

1. Generate `init_schema.sql` based on the DBML schema
2. Create migration scripts if using Alembic or similar tools
3. Provide MongoDB connection helpers (optional)
4. **NOT** generate any seed data (delegated to ingestion service)

All future database-related Copilot work should reference **`COPILOT_DATABASE.md`** (Version 2).

---

## Original Instructions Archive

The complete instructions that were used to create Version 2 are preserved below for historical reference.

---



---

## ARCHIVED: Original V2 Update Instructions

<details>
<summary>Click to expand the original instructions used to create Version 2</summary>

### Step 1 – Add a versioning note referencing the original prompt

At the very top of `COPILOT_DATABASE.md`, before or right after the main title, add a short note that references the original prompt and states that this file is version 2. For example:

> _Note (v2): This document is an updated version of the original database Copilot instructions stored in `COPILOT_DATABASE.txt`. Version 1 described a PostgreSQL schema with seed data. Version 2 updates the relational model, explicitly uses PostgreSQL + PostGIS with a REST-friendly design, introduces MongoDB for configuration data, and removes all seed data responsibilities from this Copilot flow._

Keep the existing main title (e.g., “Air Quality Platform – Database Copilot Instructions”).

Do not delete or overwrite `COPILOT_DATABASE.txt`; just reference it in this note.

---

## Step 2 – Replace the relational DBML with the current schema

In `COPILOT_DATABASE.md`, find the section where the relational schema is defined in DBML or a similar format. Replace the existing DBML snippet with **exactly** the following DBML model, which is the current source of truth for the relational database:

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
````

Then, in the text around this DBML:

* State explicitly that the relational database is **PostgreSQL 14+ with PostGIS enabled**, and that:

  * The `geom geometry` column in `MapRegion` uses the PostGIS `geometry` type and is optional (only required for advanced geospatial visualizations).
* Mention that the schema is **REST-friendly**, for example:

  * “The schema is designed to be REST-friendly (e.g. suitable for tools such as PostgREST), so table and column names, primary keys and foreign keys should remain stable.”

Do not add JSON fields back into this schema and do not reintroduce tables that are not present in the DBML above.

---

## Step 3 – Remove seed data responsibilities

In the current version of `COPILOT_DATABASE.md`, there is (or was) a section about **seed data** (e.g. “Seed data – initial content for development”) and possibly references to:

* `seed_data.sql`
* Python scripts to insert demo data
* pre-populated pollutants, users, stations, alerts, etc.

For version 2:

1. Remove or fully rewrite this seed data section so that **this document no longer instructs Copilot to generate any seed data**.
2. In the “Output expectations” or similar section:

   * Delete any bullet that says Copilot must create seed scripts or insert demo/reference data.
   * Replace them with something like:

     > “Generate schema/migration scripts only (e.g., `init_schema.sql` or migration files) without inserting any demo or reference data. All data (reference and sample) will be created by the ingestion pipeline and application services.”

The database Copilot is now responsible only for **schema/migrations and configuration**, not for populating data.

---

## Step 4 – Clarify PostgreSQL + PostGIS + REST-friendly design

In the sections where you describe the target environment and schema creation:

* Explicitly state:

  * “Use PostgreSQL 14+ with the PostGIS extension enabled.”
  * “Primary keys, foreign keys and naming should remain consistent to keep the schema REST-friendly (e.g., for tools such as PostgREST).”

* If there was any mention of TimescaleDB or other engines as part of the baseline, rephrase them as **optional future enhancements**, for example:

  * “The project may adopt partitioning or TimescaleDB in future iterations if data volumes grow, but the baseline schema targets plain PostgreSQL + PostGIS.”

Do not require the Copilot flow to configure PostgREST itself; simply document that the schema should not break a potential REST layer.

---

## Step 5 – Add a new section for MongoDB (NoSQL configuration store)

Add a new section to `COPILOT_DATABASE.md`, for example:

```md
## MongoDB – configuration and personalization store
```

In this section, document the NoSQL side:

1. **Purpose**

   * MongoDB is used only for **user-specific configuration** and **dashboard layouts**, not for core business data.
   * Core entities (stations, readings, alerts, recommendations, reports, daily stats) live in PostgreSQL.

2. **Collections**

   Describe at least two collections:

   * `user_preferences`

     * Fields (examples):

       * `user_id` (string or UUID referencing `AppUser.id` externally)
       * `default_city` (string)
       * `favorite_pollutants` (array)
       * `notifications` (subdocument: `email_enabled`, `min_aqi_for_alert`, etc.)
       * `theme` (e.g. `"light"` / `"dark"`)

   * `dashboard_configs`

     * Fields (examples):

       * `user_id`
       * `widgets` (array of subdocuments with: `type`, `pollutant`, `position`, `enabled`, etc.)
       * `last_updated` (timestamp, optional)

3. **Indexes**

   Recommend basic indexes:

   * Index on `user_id` in both `user_preferences` and `dashboard_configs`.
   * Optionally, an index on `widgets.type` within `dashboard_configs` for common queries.

4. **No seeding**

   Clearly state that:

   * This document does **not** define any seed data for MongoDB.
   * Documents will be created and updated at runtime by the ingestion services and application code.

5. **Environment variables**

   * Reuse the same approach as for PostgreSQL:

     * Define a `MONGO_URI` or `MONGODB_URL` environment variable (in `.env.example`).
     * Do not hardcode credentials or real connection strings.

---

## Step 6 – Adjust output expectations and file organization

In the section that describes what Copilot should generate:

* Make sure it now says that Copilot is expected to produce only:

  * SQL schema/migration files for PostgreSQL + PostGIS, based on the updated DBML.
  * (Optionally) helper scripts or notes for connecting to MongoDB (e.g., sample connection code or JSON schema suggestions), but **not** data seeds.

* Update any reference to `.env` / `.env.example` and `.copilot_temp/` to remain valid, but ensure they no longer mention seed scripts or seed data.

---

## Step 7 – Final consistency check

After editing `COPILOT_DATABASE.md`, check that:

* The relational schema matches the DBML snippet exactly (same table names, columns, PKs and FKs).

* The document clearly references:

  * Version 1 (`COPILOT_DATABASE.txt`) as the original prompt.
  * Version 2 (`COPILOT_DATABASE.md`) as the updated instructions.

* It describes:

  * PostgreSQL + PostGIS as the relational core.
  * A REST-friendly schema design (e.g., for tools such as PostgREST).
  * MongoDB as a small NoSQL store for preferences and dashboard configuration.
  * No seed data tasks (everything is delegated to ingestion and application layers).

</details>

---

**📌 Note:** This is a historical/completion report document. For actual database Copilot instructions, always use **`COPILOT_DATABASE.md`** (Version 2).
