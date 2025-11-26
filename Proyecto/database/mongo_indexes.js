// Air Quality Platform - MongoDB Indexes
// This script creates performance indexes for MongoDB collections
// Run after mongo_init.js

// Switch to the air_quality_config database
db = db.getSiblingDB('air_quality_config');

print('========================================');
print('Creating MongoDB Indexes');
print('Database: air_quality_config');
print('========================================\n');

// ============================================================================
// INDEXES: user_preferences
// ============================================================================

print('Creating indexes for user_preferences...');

// Primary lookup index - user_id must be unique (one preference doc per user)
db.user_preferences.createIndex(
  { user_id: 1 },
  { 
    unique: true,
    name: 'idx_user_preferences_user_id'
  }
);
print('✓ Created unique index on user_id');

// Index for filtering by theme (if needed for analytics)
db.user_preferences.createIndex(
  { theme: 1 },
  { 
    sparse: true,
    name: 'idx_user_preferences_theme'
  }
);
print('✓ Created index on theme');

// Index for finding users with email notifications enabled
db.user_preferences.createIndex(
  { 'notifications.email_enabled': 1 },
  { 
    sparse: true,
    name: 'idx_user_preferences_email_enabled'
  }
);
print('✓ Created index on notifications.email_enabled');

// Compound index for finding users by city and notification preferences
db.user_preferences.createIndex(
  { default_city: 1, 'notifications.min_aqi_for_alert': 1 },
  { 
    sparse: true,
    name: 'idx_user_preferences_city_aqi_alert'
  }
);
print('✓ Created compound index on default_city + min_aqi_for_alert');

// Index for recent updates (useful for sync operations)
db.user_preferences.createIndex(
  { updated_at: -1 },
  { 
    sparse: true,
    name: 'idx_user_preferences_updated_at'
  }
);
print('✓ Created index on updated_at\n');

// ============================================================================
// INDEXES: dashboard_configs
// ============================================================================

print('Creating indexes for dashboard_configs...');

// Primary lookup index - user_id must be unique (one dashboard config per user)
db.dashboard_configs.createIndex(
  { user_id: 1 },
  { 
    unique: true,
    name: 'idx_dashboard_configs_user_id'
  }
);
print('✓ Created unique index on user_id');

// Index for finding specific widget types (for analytics/usage tracking)
db.dashboard_configs.createIndex(
  { 'widgets.type': 1 },
  { 
    sparse: true,
    name: 'idx_dashboard_configs_widget_type'
  }
);
print('✓ Created index on widgets.type');

// Index for finding enabled widgets
db.dashboard_configs.createIndex(
  { 'widgets.enabled': 1 },
  { 
    sparse: true,
    name: 'idx_dashboard_configs_widget_enabled'
  }
);
print('✓ Created index on widgets.enabled');

// Index for recent updates
db.dashboard_configs.createIndex(
  { last_updated: -1 },
  { 
    sparse: true,
    name: 'idx_dashboard_configs_last_updated'
  }
);
print('✓ Created index on last_updated');

// Index for version tracking (useful for migrations)
db.dashboard_configs.createIndex(
  { version: 1 },
  { 
    sparse: true,
    name: 'idx_dashboard_configs_version'
  }
);
print('✓ Created index on version\n');

// ============================================================================
// VERIFY INDEXES
// ============================================================================

print('========================================');
print('Index Verification');
print('========================================\n');

print('Indexes on user_preferences:');
db.user_preferences.getIndexes().forEach(function(index) {
  print('  - ' + index.name + ': ' + JSON.stringify(index.key));
});

print('\nIndexes on dashboard_configs:');
db.dashboard_configs.getIndexes().forEach(function(index) {
  print('  - ' + index.name + ': ' + JSON.stringify(index.key));
});

// ============================================================================
// SUMMARY
// ============================================================================

print('\n========================================');
print('MongoDB indexes created successfully!');
print('========================================');
print('\nPerformance Notes:');
print('  - user_id indexes are UNIQUE (one doc per user)');
print('  - Sparse indexes used where fields are optional');
print('  - Compound indexes optimize common query patterns');
print('\nQuery Examples:');
print('  db.user_preferences.find({ user_id: 123 })');
print('  db.dashboard_configs.find({ user_id: 123 })');
print('  db.user_preferences.find({ default_city: "Bogotá" })');
