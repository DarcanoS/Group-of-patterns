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
**Run order**: Third (after schema and permissions)

**Usage**:
```bash
./db_helper.sh run-admin postgresql/seed_data.sql
```

Or use the Python loader:

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


# PostgreSQL + PostGIS - Air Quality Platform

This folder contains scripts to create and populate the main relational database for the project.

## Files

- `init_schema.sql`: Creates all tables, indexes, and constraints
- `setup_users_permissions.sql`: Sets up users and permissions
- `seed_data.sql`: Inserts initial data (pollutants, roles, stations, demo users)

## Usage

1. Start the PostgreSQL container (see `../CONTAINERS.md`)
2. Connect to the container:
	```bash
	podman exec -it air_quality_postgres psql -U air_quality_admin -d air_quality_db
	# o
	docker exec -it air_quality_postgres psql -U air_quality_admin -d air_quality_db
	```
3. Scripts are executed automatically on container creation. To run manually:
	```sql
	\i /docker-entrypoint-initdb.d/01_init_schema.sql
	\i /docker-entrypoint-initdb.d/02_setup_users_permissions.sql
	\i /docker-entrypoint-initdb.d/03_seed_data.sql
	```

## Notes

- Scripts are prepared for automatic execution when the container is created.
- To reinitialize, remove the volume and restart the container.
- Do not include ingestion or temporary files in this folder.
\du              -- List all users
