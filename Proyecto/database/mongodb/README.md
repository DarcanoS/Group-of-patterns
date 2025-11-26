# MongoDB Configuration

This folder contains MongoDB setup scripts and configuration.

## Files

### `mongo_init.js`
Initializes MongoDB database and collections with validation schemas:
- `user_preferences` - User preferences (theme, default city, notifications)
- `dashboard_configs` - Dashboard layout configurations

**Usage**:
```bash
# If using Docker Compose
docker-compose -f mongo_docker_compose.yml up -d

# Or manually
mongosh admin -u root -p example --eval "$(cat mongo_init.js)"
```

### `mongo_indexes.js`
Creates performance indexes for MongoDB collections:
- Index on `user_id` for fast user lookups
- Index on `updated_at` for sorting

**Usage**:
```bash
mongosh air_quality_config -u air_quality_user -p secure_password --eval "$(cat mongo_indexes.js)"
```

### `mongo_docker_compose.yml`
Docker Compose configuration for running MongoDB locally.

**Usage**:
```bash
# Start MongoDB
docker-compose -f mongo_docker_compose.yml up -d

# Stop MongoDB
docker-compose -f mongo_docker_compose.yml down

# View logs
docker-compose -f mongo_docker_compose.yml logs -f
```

**Default credentials**:
- Root user: `root` / `example`
- App user: `air_quality_user` / `secure_password`
- Database: `air_quality_config`

## Collections Schema

### `user_preferences`
```json
{
  "user_id": 123,
  "theme": "dark",
  "default_city": "Bogotá",
  "default_pollutants": ["PM2.5", "PM10"],
  "notification_channels": ["email"],
  "updated_at": "2025-11-26T12:00:00Z"
}
```

### `dashboard_configs`
```json
{
  "user_id": 123,
  "layout": {
    "widgets": [
      {
        "id": "current_aqi",
        "position": {"x": 0, "y": 0},
        "size": {"w": 2, "h": 1}
      }
    ]
  },
  "visible_panels": ["aqi", "stations", "recommendations"],
  "updated_at": "2025-11-26T12:00:00Z"
}
```

## Setup Order

1. Start MongoDB container: `docker-compose -f mongo_docker_compose.yml up -d`
2. Initialize database and collections: Run `mongo_init.js`
3. Create indexes: Run `mongo_indexes.js`
4. Verify setup: Use `scripts/mongo_python_examples.py`

## Python Integration

See `scripts/mongo_python_examples.py` for examples of:
- Connecting to MongoDB
- Reading/writing user preferences
- Reading/writing dashboard configurations

## Documentation

For complete setup instructions and examples, see `docs/MONGODB_SETUP.md`.
