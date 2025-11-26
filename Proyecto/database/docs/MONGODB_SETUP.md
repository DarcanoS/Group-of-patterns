# MongoDB Setup - Air Quality Platform

This document describes the MongoDB configuration for the **Air Quality Platform**.

## Purpose

MongoDB is used **exclusively** for user-specific configuration and dashboard layouts, **not** for core business data.

### What goes in MongoDB:
- ✅ User preferences (theme, default city, notification settings)
- ✅ Dashboard widget configurations and layouts
- ✅ Personalization data

### What stays in PostgreSQL:
- ❌ Stations, pollutants, readings (core operational data)
- ❌ Users, roles, permissions (authentication/authorization)
- ❌ Alerts, recommendations, reports (business logic data)
- ❌ Daily statistics (analytical data)

---

## Database and Collections

**Database name:** `air_quality_config`

### Collections:

#### 1. `user_preferences`
Stores user-specific settings and preferences.

**Schema:**
```javascript
{
  user_id: int,              // References AppUser.id (PostgreSQL)
  default_city: string,      // Default city for display
  favorite_pollutants: [],   // Array of pollutant names
  theme: string,             // "light" or "dark"
  notifications: {
    email_enabled: bool,
    sms_enabled: bool,
    min_aqi_for_alert: int,
    frequency: string        // "realtime", "hourly", "daily"
  },
  language: string,          // ISO 639-1 code (e.g., "en", "es")
  timezone: string,          // IANA timezone (e.g., "America/Bogota")
  updated_at: date,
  created_at: date
}
```

**Indexes:**
- `user_id` (unique)
- `theme` (sparse)
- `notifications.email_enabled` (sparse)
- `default_city, notifications.min_aqi_for_alert` (compound, sparse)
- `updated_at` (descending, sparse)

#### 2. `dashboard_configs`
Stores user dashboard layouts and widget configurations.

**Schema:**
```javascript
{
  user_id: int,              // References AppUser.id (PostgreSQL)
  layout_type: string,       // "grid", "freeform", "list"
  widgets: [
    {
      id: string,            // Unique widget ID
      type: string,          // Widget type (e.g., "current_aqi", "pollutant_chart")
      title: string,         // Custom title
      position: {
        x: int, y: int,
        w: int, h: int
      },
      config: {
        pollutant: string,
        station_id: int,
        time_range: string,  // "24h", "7d", "30d", etc.
        chart_type: string   // "line", "bar", "area", "pie"
      },
      enabled: bool,
      order: int
    }
  ],
  last_updated: date,
  created_at: date,
  version: int               // For migration compatibility
}
```

**Indexes:**
- `user_id` (unique)
- `widgets.type` (sparse)
- `widgets.enabled` (sparse)
- `last_updated` (descending, sparse)
- `version` (sparse)

---

## Setup Instructions

### 1. Start MongoDB with Podman/Docker

```bash
# Create a volume for data persistence
podman volume create mongodb-data

# Run MongoDB container
podman run -d \
  --name mongodb \
  -p 27017:27017 \
  -e MONGO_INITDB_DATABASE=air_quality_config \
  -v mongodb-data:/data/db \
  mongo:7

# Verify it's running
podman ps | grep mongodb
```

### 2. Initialize Collections and Schemas

```bash
# Copy initialization script to container
podman cp mongo_init.js mongodb:/tmp/

# Execute initialization
podman exec -i mongodb mongosh /tmp/mongo_init.js

# Expected output:
# ========================================
# Air Quality Platform - MongoDB Setup
# Database: air_quality_config
# ========================================
# 
# Creating collection: user_preferences
# ✓ Collection user_preferences created
# 
# Creating collection: dashboard_configs
# ✓ Collection dashboard_configs created
```

### 3. Create Indexes

```bash
# Copy index script to container
podman cp mongo_indexes.js mongodb:/tmp/

# Execute index creation
podman exec -i mongodb mongosh /tmp/mongo_indexes.js

# Verify indexes
podman exec -i mongodb mongosh --eval "
  db.getSiblingDB('air_quality_config').user_preferences.getIndexes()
"
```

### 4. Configure Environment Variables

Add to your `.env` file:

```bash
# MongoDB Configuration
MONGO_URI=mongodb://localhost:27017/air_quality_config
MONGO_DB_NAME=air_quality_config
MONGO_HOST=localhost
MONGO_PORT=27017
```

**Security note:** In production, use authentication:
```bash
MONGO_URI=mongodb://username:password@host:27017/air_quality_config?authSource=admin
```

---

## Usage Examples

### From MongoDB Shell (mongosh)

```javascript
// Connect to database
use air_quality_config

// Insert user preferences
db.user_preferences.insertOne({
  user_id: 1,
  default_city: "Bogotá",
  favorite_pollutants: ["PM2.5", "O3"],
  theme: "dark",
  notifications: {
    email_enabled: true,
    min_aqi_for_alert: 100,
    frequency: "daily"
  },
  language: "es",
  timezone: "America/Bogota",
  created_at: new Date(),
  updated_at: new Date()
})

// Find user preferences
db.user_preferences.findOne({ user_id: 1 })

// Update preferences
db.user_preferences.updateOne(
  { user_id: 1 },
  { 
    $set: { 
      theme: "light",
      updated_at: new Date()
    }
  }
)

// Insert dashboard config
db.dashboard_configs.insertOne({
  user_id: 1,
  layout_type: "grid",
  widgets: [
    {
      id: "widget-1",
      type: "current_aqi",
      title: "Current AQI",
      position: { x: 0, y: 0, w: 2, h: 2 },
      config: { pollutant: "PM2.5" },
      enabled: true,
      order: 0
    }
  ],
  created_at: new Date(),
  last_updated: new Date(),
  version: 1
})
```

### From Python (Backend)

```python
from pymongo import MongoClient
import os

# Connect to MongoDB
client = MongoClient(os.getenv('MONGO_URI'))
db = client[os.getenv('MONGO_DB_NAME')]

# Get user preferences
def get_user_preferences(user_id: int):
    return db.user_preferences.find_one({'user_id': user_id})

# Update user preferences
def update_user_preferences(user_id: int, preferences: dict):
    from datetime import datetime
    preferences['updated_at'] = datetime.utcnow()
    
    return db.user_preferences.update_one(
        {'user_id': user_id},
        {'$set': preferences},
        upsert=True
    )

# Get dashboard config
def get_dashboard_config(user_id: int):
    return db.dashboard_configs.find_one({'user_id': user_id})
```

---

## Data Management

### No Seed Data

Unlike PostgreSQL, MongoDB collections are **NOT seeded** with initial data. Documents are created:

- **At user registration** (default preferences)
- **On first dashboard access** (default layout)
- **At runtime** by the application

### Backup and Restore

```bash
# Backup
podman exec mongodb mongodump \
  --db=air_quality_config \
  --out=/tmp/backup

podman cp mongodb:/tmp/backup ./mongodb-backup

# Restore
podman cp ./mongodb-backup mongodb:/tmp/backup

podman exec mongodb mongorestore \
  --db=air_quality_config \
  /tmp/backup/air_quality_config
```

### Clear Collections (Development)

```bash
# Drop all documents (keeps schema validation)
podman exec -i mongodb mongosh --eval "
  use air_quality_config
  db.user_preferences.deleteMany({})
  db.dashboard_configs.deleteMany({})
"
```

---

## Monitoring and Performance

### Check Collection Stats

```javascript
use air_quality_config

// Collection statistics
db.user_preferences.stats()
db.dashboard_configs.stats()

// Index usage
db.user_preferences.aggregate([
  { $indexStats: {} }
])
```

### Common Queries Performance

```javascript
// Should use idx_user_preferences_user_id (fast)
db.user_preferences.find({ user_id: 1 }).explain("executionStats")

// Should use idx_user_preferences_city_aqi_alert (fast)
db.user_preferences.find({
  default_city: "Bogotá",
  "notifications.min_aqi_for_alert": { $gte: 100 }
}).explain("executionStats")
```

---

## Troubleshooting

### Connection Issues

```bash
# Check if MongoDB is running
podman ps | grep mongodb

# Check logs
podman logs mongodb

# Test connection
podman exec -i mongodb mongosh --eval "db.serverStatus()"
```

### Validation Errors

If documents fail validation:

```javascript
// Check validation errors
db.getCollectionInfos({ name: "user_preferences" })[0].options.validator

// Temporarily disable validation (NOT recommended for production)
db.runCommand({
  collMod: "user_preferences",
  validationLevel: "off"
})
```

---

## Security Best Practices

1. **Enable authentication in production:**
   ```bash
   podman run -d \
     --name mongodb \
     -p 27017:27017 \
     -e MONGO_INITDB_ROOT_USERNAME=admin \
     -e MONGO_INITDB_ROOT_PASSWORD=secure_password \
     -v mongodb-data:/data/db \
     mongo:7 --auth
   ```

2. **Use separate users for app access:**
   ```javascript
   use air_quality_config
   db.createUser({
     user: "air_quality_app",
     pwd: "app_password",
     roles: [
       { role: "readWrite", db: "air_quality_config" }
     ]
   })
   ```

3. **Limit network exposure:**
   - Only bind to localhost in development
   - Use firewall rules in production
   - Consider TLS/SSL for connections

---

## References

- [MongoDB Documentation](https://www.mongodb.com/docs/)
- [Schema Validation](https://www.mongodb.com/docs/manual/core/schema-validation/)
- [Index Strategies](https://www.mongodb.com/docs/manual/indexes/)
- [PyMongo Driver](https://pymongo.readthedocs.io/)
