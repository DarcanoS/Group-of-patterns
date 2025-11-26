# PostgreSQL Schema and Scripts

This folder contains all PostgreSQL database schema files and setup scripts.

## Files

### `init_schema.sql`
Creates the complete database schema including:
- All tables with proper data types
- Foreign key constraints
- Indexes for performance
- PostGIS geometry columns

**Run order**: First (before any other script)

**Usage**:
```bash
cd Proyecto/database
./db_helper.sh run-admin postgresql/init_schema.sql
```

### `setup_users_permissions.sql`
Grants appropriate permissions to the application user (`air_quality_app`).

**Run order**: Second (after init_schema.sql)

**Permissions granted**:
- SELECT only on reference tables (roles, permissions, pollutants, stations)
- SELECT + INSERT on data ingestion tables (readings, recommendations, reports)
- SELECT + INSERT + UPDATE on user management and statistics
- Full CRUD on alerts

**Usage**:
```bash
./db_helper.sh run-admin postgresql/setup_users_permissions.sql
```

### `seed_data.sql`
Populates initial reference data:
- Pollutants (PM2.5, PM10, O3, NO2, SO2, CO)
- Roles (Citizen, Researcher, Admin)
- Permissions and role-permission mappings
- Map regions (Bogotá Metropolitan Area)
- Stations (5 monitoring stations in Bogotá)
- Demo users (one per role)

**Run order**: Third (after schema and permissions)

**Usage**:
```bash
./db_helper.sh run-admin postgresql/seed_data.sql
```

Or use the Python loader:
```bash
cd Proyecto/database
python scripts/load_seed_data.py
```

## Execution Order

Always run scripts in this order:

1. `init_schema.sql` - Creates schema
2. `setup_users_permissions.sql` - Grants permissions
3. `seed_data.sql` - Loads initial data

## Schema Overview

The schema follows the DBML model defined in `docs/COPILOT_DATABASE_V2.md` and includes:

### Geospatial & Monitoring
- `map_region` - Geographical regions with PostGIS polygons
- `pollutant` - Air pollutant catalog
- `station` - Monitoring stations
- `air_quality_reading` - Sensor readings
- `air_quality_daily_stats` - Aggregated statistics

### Users & Access Control
- `role` - User roles
- `permission` - System permissions
- `role_permission` - Role-permission mappings
- `app_user` - Application users

### Alerts & Personalization
- `alert` - User pollution alerts
- `recommendation` - Health recommendations
- `product_recommendation` - Product suggestions

### Reporting
- `report` - Report metadata

## Verification

After running all scripts, verify the setup:

```bash
# Connect as admin
./db_helper.sh admin

# Inside psql:
\dt              -- List all tables
\du              -- List all users
SELECT COUNT(*) FROM pollutant;  -- Should return 6
SELECT COUNT(*) FROM station;    -- Should return 5
SELECT COUNT(*) FROM role;       -- Should return 3
```

## Notes

- All scripts use `GENERATED ALWAYS AS IDENTITY` for primary keys (modern standard)
- Timestamps use `timestamp with time zone` for proper timezone handling
- Foreign key constraints use CASCADE, RESTRICT, or SET NULL appropriately
- Comprehensive indexing for performance
