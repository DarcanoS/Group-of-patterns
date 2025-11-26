# Database Utility Scripts

This folder contains Python scripts for database operations and verification.

## Files

### `load_seed_data.py`
Loads seed data into PostgreSQL using Python and SQLAlchemy.

**Purpose**:
- Alternative to running `postgresql/seed_data.sql` directly
- Demonstrates SQLAlchemy ORM usage
- Useful for programmatic data loading

**Usage**:
```bash
cd Proyecto/database
python scripts/load_seed_data.py
```

**Requirements**:
- Backend dependencies installed (`pip install -r ../backend/requirements.txt`)
- Environment variables set (reads from `../.env`)
- Database schema already created

**What it loads**:
- 6 pollutants
- 3 roles
- 9 permissions
- Role-permission mappings
- 1 region (Bogotá)
- 5 stations
- 3 demo users

### `verify_ingestion.py`
Verifies data ingestion and displays statistics.

**Purpose**:
- Check if ingestion service is working
- Display reading counts per station
- Verify data quality

**Usage**:
```bash
cd Proyecto/database
python scripts/verify_ingestion.py
```

**Output**:
- Total readings count
- Readings per station
- Date range of data
- Pollutant coverage

**Requirements**:
- Database with ingested data
- Environment variables configured

### `mongo_python_examples.py`
Examples of MongoDB operations using PyMongo.

**Purpose**:
- Demonstrate MongoDB connection
- Show CRUD operations for user preferences
- Show CRUD operations for dashboard configs

**Usage**:
```python
# Read the file for examples, then adapt to your needs
python scripts/mongo_python_examples.py
```

**Examples included**:
- Connecting to MongoDB
- Creating user preferences
- Reading user preferences
- Updating preferences
- Creating dashboard configurations
- Cloning dashboard configs (Prototype pattern)

**Requirements**:
- MongoDB running
- `pymongo` installed
- Environment variables set

## Environment Setup

All scripts read environment variables from `../database/.env`:

```bash
# PostgreSQL
DATABASE_URL=postgresql://user:password@host:port/dbname

# MongoDB
NOSQL_URI=mongodb://user:password@host:port/
NOSQL_DB_NAME=air_quality_config
```

## Common Workflows

### Initial Setup
```bash
# 1. Load seed data
python scripts/load_seed_data.py

# 2. Verify (should show 0 readings initially)
python scripts/verify_ingestion.py
```

### After Ingestion
```bash
# Verify ingestion results
python scripts/verify_ingestion.py
```

### MongoDB Testing
```bash
# Test MongoDB connection and operations
python scripts/mongo_python_examples.py
```

## Dependencies

Install required packages:
```bash
# From backend directory
cd ../backend
pip install -r requirements.txt

# Or install specific packages
pip install sqlalchemy psycopg2-binary pymongo python-dotenv
```

## Notes

- All scripts use environment variables for configuration
- No hardcoded credentials
- Scripts are idempotent where possible (can run multiple times safely)
- Error handling included for common issues
