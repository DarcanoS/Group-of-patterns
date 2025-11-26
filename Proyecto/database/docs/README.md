# Database Documentation

This folder contains comprehensive documentation for the database setup and operations.

## Files

### `COPILOT_DATABASE_V2.md`
GitHub Copilot instructions for database development.

**Purpose**:
- Guide AI assistants in generating database code
- Define schema standards and conventions
- Document design patterns and best practices

**Contents**:
- Complete DBML schema definition
- PostgreSQL + PostGIS setup guidelines
- MongoDB configuration instructions
- Design decisions and rationale

**Audience**: GitHub Copilot, developers extending the database

### `MONGODB_SETUP.md`
Complete MongoDB setup and usage guide.

**Purpose**:
- Step-by-step MongoDB installation
- Collection schema documentation
- Python integration examples

**Contents**:
- Docker setup instructions
- Database and user creation
- Collection validation schemas
- Index creation
- Python examples with PyMongo

**Audience**: Developers setting up MongoDB for the first time


## How to Use This Documentation

### For Initial Setup
1. Read parent `README.md` for overview
2. Follow `COPILOT_DATABASE_V2.md` for schema understanding
3. Use `MONGODB_SETUP.md` for NoSQL setup

### For Development
1. Reference `COPILOT_DATABASE_V2.md` for schema changes
2. Follow documented patterns and conventions
3. Update documentation when making schema changes

### For Troubleshooting
1. Verify setup followed `MONGODB_SETUP.md` steps
2. Review parent `README.md` for common issues

## Documentation Standards

When updating documentation:
- Keep DBML schema in sync across all files
- Document design decisions and rationale
- Include practical examples
- Use clear, concise English
- Update version notes when making changes

## Related Documentation

- Parent folder: `../README.md` - Main database setup guide
- Backend: `../../backend/COPILOT_BACKEND.md` - Backend integration
- Ingestion: `../../ingestion/README.md` - Ingestion service docs
