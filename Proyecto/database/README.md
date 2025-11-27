# Air Quality Platform - Database Setup

This folder contains database schema, setup scripts and configuration for the Air Quality Platform.

## Architecture

The platform uses a **hybrid database architecture**:


## Prerequisites

### Option 1: Using Containers (Recommended)

### Option 2: Local Installation

## 📁 Folder Structure

```
database/
├── README.md                          # This file - Setup guide
├── .env.example                       # Template for environment variables
├── .env                              # Your credentials (gitignored)
├── db_helper.sh                      # Helper script for database operations
│
├── postgresql/                        # PostgreSQL schema and scripts
│   ├── init_schema.sql               # Creates all tables, indexes, constraints
│   ├── setup_users_permissions.sql   # Grants permissions to app user
│   └── seed_data.sql                 # Initial reference data
│
├── mongodb/                          # MongoDB configuration
│   ├── mongo_init.js                 # Creates collections with validation
│   ├── mongo_indexes.js              # Creates performance indexes
│   └── mongo_docker_compose.yml      # Docker Compose for MongoDB
│
├── scripts/                          # Utility scripts
│   ├── load_seed_data.py             # Python loader for seed data
│   ├── verify_ingestion.py           # Verify data ingestion
│   └── mongo_python_examples.py      # MongoDB Python examples
│
├── docs/                             # Documentation
│   ├── INGESTION_SUMMARY.md          # Summary of data ingestion process
│   ├── MONGODB_SETUP.md              # Complete MongoDB setup guide
│   └── README.md                     # Documentation index
│
├── podman-compose.yml                # Container orchestration (Podman/Docker)
├── .env.containers                   # Container configuration template
├── containers.sh                     # Container management script
├── CONTAINERS.md                     # Container setup guide
│
└── .copilot_temp/                    # Temporary docs (gitignored)
    └── ...
```

## Quick Start


### 🚀 Fastest Way: Using Containers

```bash
cd Proyecto/database

# 1. Configure your credentials
cp .env.example .env
nano .env  # Edit with your secure passwords

# 2. Start containers
./containers.sh up podman

# 3. Verify everything works
./containers.sh health podman
```

**See detailed container documentation**: [CONTAINERS.md](CONTAINERS.md)

### 🟢 Database Initialization Flow (Recommended)

1. **Create schema (tables, indexes, etc.):**
  ```bash
  ./db_helper.sh run-admin postgresql/init_schema.sql
  ```
2. **Insert initial reference data (pollutants, roles, stations, etc.):**
  ```bash
  ./db_helper.sh run-admin postgresql/seed_data.sql
  ```
3. **Create users and assign permissions:**
  - If not created, connect as superuser and run:
    ```sql
    CREATE USER air_quality_admin WITH PASSWORD 'admin_secure_password';
    CREATE USER air_quality_app WITH PASSWORD 'app_secure_password';
    ```
  - Then assign permissions:
    ```bash
    ./db_helper.sh run-admin postgresql/setup_users_permissions.sql
    ```

**Important:** Si ejecutas el script de permisos antes de crear el usuario `air_quality_app`, verás errores de "role does not exist". Primero crea el usuario.

### 🔄 Need to Reset Everything?

If you need to recreate containers with new credentials:

```bash
# Option 1: Automated reset
./reset_containers.sh podman

# Option 2: Manual cleanup
./containers.sh clean podman
./containers.sh up podman
```

## Folder Structure

```text
.env                # Database environment variables (PostgreSQL, MongoDB)
.env.example        # Example env file for local setup
.env.containers     # Container environment variables (Podman/Docker)
README.md           # Main database documentation
CONTAINERS.md       # Container setup and usage guide (Podman & Docker)
db_helper.sh        # Helper script for DB operations
podman-compose.yml  # Podman Compose file for containers
docker-compose.yml  # Docker Compose file (NEW, see below)
containers.sh       # Container management script (Podman & Docker)

postgresql/         # PostgreSQL schema, seed, permissions
  init_schema.sql   # Main schema
  seed_data.sql     # Initial data
  setup_users_permissions.sql # User/role setup
  README.md         # PostgreSQL usage

mongodb/            # MongoDB initialization and indexes
  mongo_init.js     # Init script
  mongo_indexes.js  # Indexes
  README.md         # MongoDB usage

scripts/            # Python utilities
  load_seed_data.py # Seed loader
  verify_ingestion.py # Data verification
  mongo_python_examples.py # MongoDB Python usage
  README.md         # Scripts usage

docs/               # Documentation (only essentials)
  MONGODB_SETUP.md  # MongoDB setup guide
  README.md         # Docs index
```

> Only keep files strictly needed for DB structure, initialization, and container setup. Remove ingestion summaries and temporary files from repo.
> **🐳 Using Containers?** See [CONTAINERS.md](CONTAINERS.md) for Podman/Docker setup (recommended for development and production).

```bash
cd Proyecto/database/
cp .env.example .env

# Edit .env with your actual credentials
nano .env  # or use your preferred editor
```

**Important**: The `.env` file contains sensitive credentials and is already excluded from Git via `.gitignore`.

**Using the helper script (recommended)**:
```bash
# The db_helper.sh script automatically loads credentials from .env
./db_helper.sh info    # Show connection information
./db_helper.sh admin   # Connect as admin
./db_helper.sh app     # Connect as app user
```

### 1. Create Database and Users

```bash
# Using psql as postgres user
sudo -u postgres psql
```

```sql
-- Create database
CREATE DATABASE air_quality_db;

-- Create ADMIN user with full permissions
CREATE USER air_quality_admin WITH PASSWORD 'admin_secure_password';
GRANT ALL PRIVILEGES ON DATABASE air_quality_db TO air_quality_admin;

-- Create APPLICATION user with limited permissions
CREATE USER air_quality_app WITH PASSWORD 'app_secure_password';
GRANT CONNECT ON DATABASE air_quality_db TO air_quality_app;

-- Exit psql
\q
```

### 2. Run Schema Creation (as admin)

**Option 1: Using the helper script (recommended)**
```bash
./db_helper.sh run-admin postgresql/init_schema.sql
```

**Option 2: Direct connection**
```bash
# Navigate to the database folder
cd Proyecto/database/

# Run the schema creation script
podman exec -i postgis-db psql -U air_quality_admin -d air_quality_db < postgresql/init_schema.sql
```

**Option 3: With environment variable**
```bash
source .env
psql $DATABASE_URL_ADMIN -f postgresql/init_schema.sql
```

### 3. Grant Permissions to Application User

After creating the schema, grant specific permissions to the application user:

**Using the helper script:**
```bash
./db_helper.sh run-admin postgresql/setup_users_permissions.sql
```

**Or directly:**
```bash
# Connect as admin user and run the permissions script
podman exec -i postgis-db psql -U air_quality_admin -d air_quality_db < postgresql/setup_users_permissions.sql
```

**The script automatically grants:**
- **SELECT only** on reference tables (roles, permissions, pollutants, stations)
- **SELECT + INSERT** on data ingestion tables (readings, recommendations, reports)
- **SELECT + INSERT + UPDATE** on user management and statistics
- **Full CRUD** on alerts (users need to delete their own alerts)
- **USAGE on sequences** (required for INSERT operations with IDENTITY columns)

You can verify the permissions by checking the output of the verification queries at the end of the script.

**Summary of User Roles:**

| User | Purpose | Access Level |
|------|---------|-------------|
| `air_quality_admin` | Database administration, schema changes, migrations, seed data | ALL PRIVILEGES (full control) |
| `air_quality_app` | Application runtime (backend API, ingestion service) | Limited permissions (see below) |

**Detailed Permissions for `air_quality_app`:**

| Table | SELECT | INSERT | UPDATE | DELETE | Notes |
|-------|--------|--------|--------|--------|-------|
| `role` | ✅ | ❌ | ❌ | ❌ | Reference data only |
| `permission` | ✅ | ❌ | ❌ | ❌ | Reference data only |
| `role_permission` | ✅ | ❌ | ❌ | ❌ | Reference data only |
| `pollutant` | ✅ | ❌ | ❌ | ❌ | Reference data only |
| `map_region` | ✅ | ❌ | ❌ | ❌ | Geographical reference |
| `station` | ✅ | ❌ | ❌ | ❌ | Station catalog |
| `app_user` | ✅ | ✅ | ✅ | ❌ | User management |
| `air_quality_reading` | ✅ | ✅ | ❌ | ❌ | Ingestion writes, backend reads |
| `air_quality_daily_stats` | ✅ | ✅ | ✅ | ❌ | Aggregation service |
| `alert` | ✅ | ✅ | ✅ | ✅ | Full CRUD for user alerts |
| `recommendation` | ✅ | ✅ | ❌ | ❌ | Backend generates |
| `product_recommendation` | ✅ | ✅ | ❌ | ❌ | Linked to recommendations |
| `report` | ✅ | ✅ | ❌ | ❌ | Report generation |

### 4. Verify Installation

```bash
# Connect to database as application user
psql -U air_quality_app -d air_quality_db

# List tables (should see all tables)
\dt

# Check PostGIS version
SELECT PostGIS_Version();

# Check your permissions
SELECT table_name, privilege_type 
FROM information_schema.table_privileges 
WHERE grantee = 'air_quality_app' 
ORDER BY table_name, privilege_type;

# Exit
\q
```

## Database Schema Overview

### Core Tables

#### Geospatial & Monitoring
- `map_region` - Geographical regions with polygon boundaries
- `pollutant` - Catalog of air pollutants (PM2.5, PM10, O3, NO2, SO2, CO)
- `station` - Air quality monitoring stations
- `air_quality_reading` - Real-time sensor readings
- `air_quality_daily_stats` - Aggregated daily statistics

#### Users & Access Control
- `role` - User roles (Citizen, Researcher, Admin)
- `permission` - System permissions
- `role_permission` - Role-permission mappings
- `app_user` - Application users

#### Alerts & Personalization
- `alert` - User-configured pollution alerts
- `recommendation` - Health recommendations
- `product_recommendation` - Protection product suggestions

#### Reporting
- `report` - Report metadata and file paths

## Design Decisions

### Identity Columns
Uses modern `GENERATED ALWAYS AS IDENTITY` instead of `SERIAL` for better standards compliance.

### Timestamps
Uses `timestamp with time zone` (`timestamptz`) for proper timezone handling.

### Geometry Type
`map_region.geom` uses `geometry(MultiPolygon, 4326)` with SRID 4326 (WGS84) for geographic coordinates.

### Foreign Key Constraints
- **CASCADE**: Used where child records should be deleted with parent (e.g., `air_quality_reading` → `station`)
- **RESTRICT**: Used for reference data to prevent accidental deletion (e.g., `pollutant`)
- **SET NULL**: Used for optional relationships (e.g., `station` → `map_region`)

### Indexes
Comprehensive indexing strategy for:
- Foreign keys (all relationships)
- Time-based queries (`datetime`, `date`, `created_at`)
- Geospatial queries (GIST index on `geom`)
- Composite indexes for frequent multi-column queries

## Next Steps

After running `postgresql/init_schema.sql`, you should:

1. Run `postgresql/seed_data.sql` to populate initial reference data (or use `scripts/load_seed_data.py`)
2. Configure your backend application's `DATABASE_URL`
3. Verify connectivity from the backend service
4. (Optional) Set up MongoDB using `docs/MONGODB_SETUP.md`

## Troubleshooting


### Common Errors & Solutions

#### "role 'air_quality_app' does not exist"
Si ves este error al ejecutar el script de permisos, significa que el usuario no ha sido creado. Solución:

1. Conéctate como superusuario o admin y ejecuta:
   ```sql
   CREATE USER air_quality_app WITH PASSWORD 'app_secure_password';
   ```
2. Vuelve a ejecutar el script de permisos.

#### "column 'sequence_name' does not exist"
Este error ocurre si la consulta sobre secuencias en el script usa un nombre de columna incorrecto. Debes consultar así:

```sql
SELECT sequence_name FROM information_schema.sequences WHERE sequence_schema = 'public';
```
Corrige el script para usar el nombre y esquema correctos.

### PostGIS Not Available

```bash
# Install PostGIS (Ubuntu/Debian)
sudo apt-get install postgresql-14-postgis-3

# Then reconnect and enable extension
psql -U air_quality_user -d air_quality_db
CREATE EXTENSION postgis;
```

### Permission Issues

```bash
# If application user needs additional permissions, connect as admin
psql -U air_quality_admin -d air_quality_db

# Grant additional table permissions
GRANT SELECT, INSERT, UPDATE ON TABLE your_table TO air_quality_app;

# Grant sequence permissions (needed for INSERT with IDENTITY columns)
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO air_quality_app;
```

### Verify User Permissions

```sql
-- Check what permissions a user has
SELECT 
  grantee,
  table_schema,
  table_name,
  string_agg(privilege_type, ', ') as privileges
FROM information_schema.table_privileges 
WHERE grantee IN ('air_quality_admin', 'air_quality_app')
  AND table_schema = 'public'
GROUP BY grantee, table_schema, table_name
ORDER BY grantee, table_name;
```

### Check Table Creation

```sql
-- Verify all tables exist
SELECT 
  table_name,
  (SELECT COUNT(*) FROM information_schema.columns 
   WHERE table_name = t.table_name) as column_count
FROM information_schema.tables t
WHERE table_schema = 'public'
ORDER BY table_name;
```

## Docker Setup (Optional)

If using Docker for PostgreSQL:

```bash
# Run PostgreSQL with PostGIS
docker run --name air-quality-postgres \
  -e POSTGRES_DB=air_quality_db \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres_password \
  -p 5432:5432 \
  -d postgis/postgis:14-3.3

# Wait for container to be ready
docker logs air-quality-postgres

# Create users (connect as postgres superuser)
docker exec -i air-quality-postgres psql -U postgres -d air_quality_db <<EOF
-- Create admin user
CREATE USER air_quality_admin WITH PASSWORD 'admin_secure_password';
GRANT ALL PRIVILEGES ON DATABASE air_quality_db TO air_quality_admin;

-- Create application user
CREATE USER air_quality_app WITH PASSWORD 'app_secure_password';
GRANT CONNECT ON DATABASE air_quality_db TO air_quality_app;
EOF

# Run schema creation as admin
docker exec -i air-quality-postgres psql \
  -U air_quality_admin \
  -d air_quality_db \
  < postgresql/init_schema.sql

# Grant permissions to app user
docker exec -i air-quality-postgres psql -U air_quality_admin -d air_quality_db <<EOF
GRANT USAGE ON SCHEMA public TO air_quality_app;
GRANT SELECT ON TABLE role, permission, role_permission, pollutant, map_region, station TO air_quality_app;
GRANT SELECT, INSERT, UPDATE ON TABLE app_user, air_quality_reading, air_quality_daily_stats TO air_quality_app;
GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE alert TO air_quality_app;
GRANT SELECT, INSERT ON TABLE recommendation, product_recommendation, report TO air_quality_app;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO air_quality_app;
EOF
```

## Database Connection Strings

### For Admin Operations (migrations, schema changes)
```python
# Python (SQLAlchemy)
DATABASE_URL = "postgresql://air_quality_admin:admin_secure_password@localhost:5432/air_quality_db"
```

```javascript
// Node.js (pg)
const adminConnectionString = "postgresql://air_quality_admin:admin_secure_password@localhost:5432/air_quality_db"
```

### For Application Runtime (backend, ingestion)
```python
# Python (SQLAlchemy) - Use this in your backend/ingestion services
# Load from environment variables
import os
from dotenv import load_dotenv

load_dotenv()  # Load .env file
DATABASE_URL = os.getenv("DATABASE_URL")
```

```javascript
// Node.js (pg)
require('dotenv').config();
const appConnectionString = process.env.DATABASE_URL;
```

### Environment Variables
```bash
# Load variables from .env file
source .env

# Or use in Python with python-dotenv
pip install python-dotenv
```

**Example usage in backend/ingestion**:
```python
# backend/app/core/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    DATABASE_URL_ADMIN: str
    
    class Config:
        env_file = "../database/.env"  # Path to .env file
        
settings = Settings()
```

## Security Best Practices

1. **Never commit passwords** - Use `.env` file (already in `.gitignore`)
2. **Use strong passwords** - Generate random passwords for production
3. **Principle of least privilege** - Application user has only necessary permissions
4. **Separate credentials** - Different users for admin vs application operations
5. **Rotate passwords regularly** - Especially for production environments
6. **Use SSL/TLS** - For production database connections, add `?sslmode=require` to connection strings
7. **Keep .env.example updated** - Without actual credentials, as a template for team members
8. **Use different .env per environment** - `.env.dev`, `.env.staging`, `.env.prod`
