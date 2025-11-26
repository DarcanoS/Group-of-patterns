// Air Quality Platform - MongoDB Initialization
// This script creates collections and validation schemas for MongoDB
// Database: air_quality_config
// Collections: user_preferences, dashboard_configs

// Switch to the air_quality_config database
db = db.getSiblingDB('air_quality_config');

print('========================================');
print('Air Quality Platform - MongoDB Setup');
print('Database: air_quality_config');
print('========================================\n');

// ============================================================================
// COLLECTION: user_preferences
// Purpose: Store user-specific preferences and settings
// ============================================================================

print('Creating collection: user_preferences');

db.createCollection('user_preferences', {
  validator: {
    $jsonSchema: {
      bsonType: 'object',
      required: ['user_id'],
      properties: {
        user_id: {
          bsonType: 'int',
          description: 'Required - References AppUser.id from PostgreSQL'
        },
        default_city: {
          bsonType: 'string',
          description: 'Default city for air quality data display'
        },
        favorite_pollutants: {
          bsonType: 'array',
          description: 'Array of pollutant names the user tracks',
          items: {
            bsonType: 'string'
          }
        },
        theme: {
          bsonType: 'string',
          enum: ['light', 'dark'],
          description: 'UI theme preference'
        },
        notifications: {
          bsonType: 'object',
          description: 'Notification preferences',
          properties: {
            email_enabled: {
              bsonType: 'bool',
              description: 'Enable email notifications'
            },
            sms_enabled: {
              bsonType: 'bool',
              description: 'Enable SMS notifications'
            },
            min_aqi_for_alert: {
              bsonType: 'int',
              description: 'Minimum AQI value to trigger alerts',
              minimum: 0,
              maximum: 500
            },
            frequency: {
              bsonType: 'string',
              enum: ['realtime', 'hourly', 'daily'],
              description: 'Notification frequency preference'
            }
          }
        },
        language: {
          bsonType: 'string',
          description: 'Preferred language (ISO 639-1 code)',
          pattern: '^[a-z]{2}$'
        },
        timezone: {
          bsonType: 'string',
          description: 'User timezone (IANA timezone format)'
        },
        updated_at: {
          bsonType: 'date',
          description: 'Last update timestamp'
        },
        created_at: {
          bsonType: 'date',
          description: 'Creation timestamp'
        }
      }
    }
  },
  validationLevel: 'moderate',
  validationAction: 'warn'
});

print('✓ Collection user_preferences created\n');

// ============================================================================
// COLLECTION: dashboard_configs
// Purpose: Store user dashboard layouts and widget configurations
// ============================================================================

print('Creating collection: dashboard_configs');

db.createCollection('dashboard_configs', {
  validator: {
    $jsonSchema: {
      bsonType: 'object',
      required: ['user_id', 'widgets'],
      properties: {
        user_id: {
          bsonType: 'int',
          description: 'Required - References AppUser.id from PostgreSQL'
        },
        layout_type: {
          bsonType: 'string',
          enum: ['grid', 'freeform', 'list'],
          description: 'Dashboard layout type'
        },
        widgets: {
          bsonType: 'array',
          description: 'Array of dashboard widgets',
          items: {
            bsonType: 'object',
            required: ['id', 'type', 'enabled'],
            properties: {
              id: {
                bsonType: 'string',
                description: 'Unique widget identifier'
              },
              type: {
                bsonType: 'string',
                enum: [
                  'current_aqi',
                  'pollutant_chart',
                  'station_map',
                  'health_recommendation',
                  'daily_stats',
                  'alerts_list',
                  'weather_widget',
                  'comparison_chart'
                ],
                description: 'Widget type/component name'
              },
              title: {
                bsonType: 'string',
                description: 'Custom widget title'
              },
              position: {
                bsonType: 'object',
                description: 'Widget position in grid/freeform layout',
                properties: {
                  x: { bsonType: 'int', minimum: 0 },
                  y: { bsonType: 'int', minimum: 0 },
                  w: { bsonType: 'int', minimum: 1 },
                  h: { bsonType: 'int', minimum: 1 }
                }
              },
              config: {
                bsonType: 'object',
                description: 'Widget-specific configuration',
                properties: {
                  pollutant: {
                    bsonType: 'string',
                    description: 'Pollutant to display (for pollutant-specific widgets)'
                  },
                  station_id: {
                    bsonType: 'int',
                    description: 'Specific station to monitor'
                  },
                  time_range: {
                    bsonType: 'string',
                    enum: ['24h', '7d', '30d', '90d', '1y'],
                    description: 'Time range for historical data'
                  },
                  chart_type: {
                    bsonType: 'string',
                    enum: ['line', 'bar', 'area', 'pie'],
                    description: 'Chart visualization type'
                  }
                }
              },
              enabled: {
                bsonType: 'bool',
                description: 'Whether widget is visible'
              },
              order: {
                bsonType: 'int',
                description: 'Display order for list layouts',
                minimum: 0
              }
            }
          }
        },
        last_updated: {
          bsonType: 'date',
          description: 'Last modification timestamp'
        },
        created_at: {
          bsonType: 'date',
          description: 'Creation timestamp'
        },
        version: {
          bsonType: 'int',
          description: 'Configuration version for migration compatibility',
          minimum: 1
        }
      }
    }
  },
  validationLevel: 'moderate',
  validationAction: 'warn'
});

print('✓ Collection dashboard_configs created\n');

// ============================================================================
// SUMMARY
// ============================================================================

print('========================================');
print('MongoDB initialization complete!');
print('Collections created:');
print('  - user_preferences');
print('  - dashboard_configs');
print('========================================');
print('\nNext steps:');
print('  1. Run mongo_indexes.js to create indexes');
print('  2. Configure backend to connect to MongoDB');
print('  3. No seed data needed - documents created at runtime');
