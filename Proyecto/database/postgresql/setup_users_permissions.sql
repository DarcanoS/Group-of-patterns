-- Air Quality Platform - User Setup and Permissions
-- Run this script AFTER creating the schema with init_schema.sql
-- Must be executed by a superuser or the air_quality_admin user

-- ============================================================================
-- GRANT PERMISSIONS TO APPLICATION USER
-- ============================================================================

-- Grant schema usage
GRANT USAGE ON SCHEMA public TO air_quality_app;

-- ============================================================================
-- READ-ONLY TABLES (Reference/Lookup data)
-- ============================================================================

-- Security and access control (reference data)
GRANT SELECT ON TABLE role TO air_quality_app;
GRANT SELECT ON TABLE permission TO air_quality_app;
GRANT SELECT ON TABLE role_permission TO air_quality_app;

-- Pollutant catalog (reference data)
GRANT SELECT ON TABLE pollutant TO air_quality_app;

-- Geographical data (mostly read-only)
GRANT SELECT ON TABLE map_region TO air_quality_app;
GRANT SELECT ON TABLE station TO air_quality_app;

-- ============================================================================
-- OPERATIONAL TABLES (Read, Insert, Update)
-- ============================================================================

-- User management (app needs to create and update users)
GRANT SELECT, INSERT, UPDATE ON TABLE app_user TO air_quality_app;

-- Air quality data (ingestion service writes, backend reads)
GRANT SELECT, INSERT ON TABLE air_quality_reading TO air_quality_app;

-- Daily statistics (aggregation service writes, backend reads)
GRANT SELECT, INSERT, UPDATE ON TABLE air_quality_daily_stats TO air_quality_app;

-- User alerts (full CRUD needed)
GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE alert TO air_quality_app;

-- Recommendations (backend creates, users read)
GRANT SELECT, INSERT ON TABLE recommendation TO air_quality_app;

-- Product recommendations (linked to recommendations)
GRANT SELECT, INSERT ON TABLE product_recommendation TO air_quality_app;

-- Reports (users generate reports)
GRANT SELECT, INSERT ON TABLE report TO air_quality_app;

-- ============================================================================
-- SEQUENCE PERMISSIONS (Required for INSERT with IDENTITY columns)
-- ============================================================================

-- Grant usage on all existing sequences
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO air_quality_app;

-- Ensure future sequences are also accessible
ALTER DEFAULT PRIVILEGES IN SCHEMA public 
  GRANT USAGE, SELECT ON SEQUENCES TO air_quality_app;

-- ============================================================================
-- VERIFICATION QUERIES
-- ============================================================================

-- Verify permissions granted
SELECT 
  grantee,
  table_name,
  string_agg(privilege_type, ', ' ORDER BY privilege_type) as privileges
FROM information_schema.table_privileges 
WHERE grantee = 'air_quality_app'
  AND table_schema = 'public'
GROUP BY grantee, table_name
ORDER BY table_name;

SELECT 
  sequence_name,
  privilege_type
 FROM information_schema.sequences
 WHERE sequence_schema = 'public';

-- ============================================================================
-- NOTES
-- ============================================================================

-- Permissions Summary for air_quality_app:
--
-- READ ONLY (SELECT):
--   - role, permission, role_permission
--   - pollutant
--   - map_region, station
--
-- READ + WRITE (SELECT, INSERT, UPDATE):
--   - app_user
--   - air_quality_reading (SELECT, INSERT only)
--   - air_quality_daily_stats
--   - recommendation, product_recommendation (SELECT, INSERT only)
--   - report (SELECT, INSERT only)
--
-- FULL CRUD (SELECT, INSERT, UPDATE, DELETE):
--   - alert
--
-- SEQUENCES:
--   - All sequences: USAGE, SELECT (required for INSERT operations)
