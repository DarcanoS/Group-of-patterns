-- ============================================================================
-- Air Quality Platform - Seed Data
-- ============================================================================
-- This script inserts initial reference data required for the application
-- to work properly. It should be run after init_schema.sql.
--
-- Usage:
--   psql -U air_quality_admin -d air_quality_db -f seed_data.sql
--
-- Note: Uses ON CONFLICT DO NOTHING to make the script idempotent
-- ============================================================================

\echo '=========================================================================='
\echo 'AIR QUALITY PLATFORM - SEED DATA'
\echo '=========================================================================='

-- ============================================================================
-- 1. POLLUTANTS (Core Reference Data)
-- ============================================================================
\echo ''
\echo '[1/7] Inserting pollutants...'

INSERT INTO pollutant (name, unit, description) VALUES
  ('PM2.5', 'µg/m³', 'Fine particulate matter less than 2.5 micrometers in diameter. Can penetrate deep into lungs and bloodstream.'),
  ('PM10', 'µg/m³', 'Particulate matter less than 10 micrometers in diameter. Includes dust, pollen, and mold spores.'),
  ('O3', 'ppb', 'Ozone. Ground-level ozone is a harmful air pollutant formed by reactions between NOx and VOCs.'),
  ('NO2', 'ppb', 'Nitrogen dioxide. A reddish-brown gas produced by combustion processes.'),
  ('SO2', 'ppb', 'Sulfur dioxide. A colorless gas with a strong odor produced by burning fossil fuels.'),
  ('CO', 'ppm', 'Carbon monoxide. A colorless, odorless gas produced by incomplete combustion.')
ON CONFLICT (name) DO NOTHING;

\echo '✓ Pollutants inserted'

-- ============================================================================
-- 2. ROLES (Access Control)
-- ============================================================================
\echo ''
\echo '[2/7] Inserting roles...'

INSERT INTO role (name) VALUES
  ('Citizen'),
  ('Researcher'),
  ('Admin')
ON CONFLICT (name) DO NOTHING;

\echo '✓ Roles inserted'

-- ============================================================================
-- 3. PERMISSIONS (Access Control)
-- ============================================================================
\echo ''
\echo '[3/7] Inserting permissions...'

INSERT INTO permission (name) VALUES
  ('VIEW_CITIZEN_DASHBOARD'),
  ('VIEW_RESEARCHER_DASHBOARD'),
  ('VIEW_ADMIN_DASHBOARD'),
  ('MANAGE_STATIONS'),
  ('MANAGE_USERS'),
  ('MANAGE_ALERTS'),
  ('EXPORT_DATA'),
  ('VIEW_REPORTS'),
  ('CREATE_REPORTS')
ON CONFLICT (name) DO NOTHING;

\echo '✓ Permissions inserted'

-- ============================================================================
-- 4. ROLE-PERMISSION MAPPINGS
-- ============================================================================
\echo ''
\echo '[4/7] Mapping roles to permissions...'

-- Citizen permissions
INSERT INTO role_permission (role_id, permission_id)
SELECT r.id, p.id
FROM role r
CROSS JOIN permission p
WHERE r.name = 'Citizen'
  AND p.name IN ('VIEW_CITIZEN_DASHBOARD')
ON CONFLICT DO NOTHING;

-- Researcher permissions
INSERT INTO role_permission (role_id, permission_id)
SELECT r.id, p.id
FROM role r
CROSS JOIN permission p
WHERE r.name = 'Researcher'
  AND p.name IN (
    'VIEW_CITIZEN_DASHBOARD',
    'VIEW_RESEARCHER_DASHBOARD',
    'EXPORT_DATA',
    'VIEW_REPORTS',
    'CREATE_REPORTS'
  )
ON CONFLICT DO NOTHING;

-- Admin permissions (all permissions)
INSERT INTO role_permission (role_id, permission_id)
SELECT r.id, p.id
FROM role r
CROSS JOIN permission p
WHERE r.name = 'Admin'
ON CONFLICT DO NOTHING;

\echo '✓ Role-permission mappings created'

-- ============================================================================
-- 5. MAP REGIONS (Geographic Boundaries)
-- ============================================================================
\echo ''
\echo '[5/7] Inserting map regions...'

-- Bogotá Metropolitan Area (simplified polygon)
INSERT INTO map_region (name, geom) VALUES
  (
    'Bogotá Metropolitan Area',
    ST_GeomFromText('POLYGON((
      -74.22 4.50,
      -74.22 4.85,
      -73.98 4.85,
      -73.98 4.50,
      -74.22 4.50
    ))', 4326)
  )
ON CONFLICT DO NOTHING;

\echo '✓ Map regions inserted'

-- ============================================================================
-- 6. STATIONS (Air Quality Monitoring Stations)
-- ============================================================================
\echo ''
\echo '[6/7] Inserting stations...'

-- Get region_id for Bogotá and insert stations only if they don't exist
DO $$
DECLARE
  bogota_region_id integer;
BEGIN
  SELECT id INTO bogota_region_id FROM map_region WHERE name = 'Bogotá Metropolitan Area';

  -- Insert stations only if they don't already exist
  INSERT INTO station (name, latitude, longitude, city, country, region_id)
  SELECT 'Carvajal', 4.614728, -74.139465, 'Bogotá', 'Colombia', bogota_region_id
  WHERE NOT EXISTS (SELECT 1 FROM station WHERE name = 'Carvajal' AND city = 'Bogotá');

  INSERT INTO station (name, latitude, longitude, city, country, region_id)
  SELECT 'Centro de Alto Rendimiento', 4.632080, -74.138298, 'Bogotá', 'Colombia', bogota_region_id
  WHERE NOT EXISTS (SELECT 1 FROM station WHERE name = 'Centro de Alto Rendimiento' AND city = 'Bogotá');

  INSERT INTO station (name, latitude, longitude, city, country, region_id)
  SELECT 'Las Ferias', 4.692070, -74.093567, 'Bogotá', 'Colombia', bogota_region_id
  WHERE NOT EXISTS (SELECT 1 FROM station WHERE name = 'Las Ferias' AND city = 'Bogotá');

  INSERT INTO station (name, latitude, longitude, city, country, region_id)
  SELECT 'Puente Aranda', 4.616460, -74.117493, 'Bogotá', 'Colombia', bogota_region_id
  WHERE NOT EXISTS (SELECT 1 FROM station WHERE name = 'Puente Aranda' AND city = 'Bogotá');

  INSERT INTO station (name, latitude, longitude, city, country, region_id)
  SELECT 'Suba', 4.745110, -74.086090, 'Bogotá', 'Colombia', bogota_region_id
  WHERE NOT EXISTS (SELECT 1 FROM station WHERE name = 'Suba' AND city = 'Bogotá');
END $$;

\echo '✓ Stations inserted'

-- ============================================================================
-- 7. DEMO USERS (For Testing)
-- ============================================================================
\echo ''
\echo '[7/7] Inserting demo users...'

-- Note: Password hashes are bcrypt for "changeme123"
-- In production, use proper password hashing and require users to change password on first login

DO $$
DECLARE
  citizen_role_id integer;
  researcher_role_id integer;
  admin_role_id integer;
BEGIN
  SELECT id INTO citizen_role_id FROM role WHERE name = 'Citizen';
  SELECT id INTO researcher_role_id FROM role WHERE name = 'Researcher';
  SELECT id INTO admin_role_id FROM role WHERE name = 'Admin';

  INSERT INTO app_user (name, email, password_hash, location, role_id) VALUES
    (
      'Demo Citizen',
      'demo.citizen@airquality.local',
      '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYfQC7aY3gS',  -- changeme123
      'Bogotá',
      citizen_role_id
    ),
    (
      'Demo Researcher',
      'demo.researcher@airquality.local',
      '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYfQC7aY3gS',  -- changeme123
      'Bogotá',
      researcher_role_id
    ),
    (
      'Demo Admin',
      'demo.admin@airquality.local',
      '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYfQC7aY3gS',  -- changeme123
      'Bogotá',
      admin_role_id
    )
  ON CONFLICT (email) DO NOTHING;
END $$;

\echo '✓ Demo users inserted'

-- ============================================================================
-- VERIFICATION QUERIES
-- ============================================================================
\echo ''
\echo '=========================================================================='
\echo 'SEED DATA SUMMARY'
\echo '=========================================================================='

SELECT 
  (SELECT COUNT(*) FROM pollutant) as pollutants,
  (SELECT COUNT(*) FROM role) as roles,
  (SELECT COUNT(*) FROM permission) as permissions,
  (SELECT COUNT(*) FROM role_permission) as role_permissions,
  (SELECT COUNT(*) FROM map_region) as regions,
  (SELECT COUNT(*) FROM station) as stations,
  (SELECT COUNT(*) FROM app_user) as users;

\echo ''
\echo '✓ Seed data insertion completed successfully!'
\echo ''
