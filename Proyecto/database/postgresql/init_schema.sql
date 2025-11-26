-- Air Quality Platform - Database Schema
-- PostgreSQL 14+ with PostGIS
-- This script creates all tables based on the DBML model

-- Enable PostGIS extension for geospatial features
CREATE EXTENSION IF NOT EXISTS postgis;

-- ============================================================================
-- GEOSPATIAL & MONITORING (Operational)
-- ============================================================================

-- MapRegion: Represents geographical regions with polygon boundaries
CREATE TABLE IF NOT EXISTS map_region (
  id integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  name varchar(255) NOT NULL,
  -- Using MultiPolygon for complex regional boundaries (SRID 4326 = WGS84)
  geom geometry(MultiPolygon, 4326)
);

-- Pollutant: Catalog of air pollutants
CREATE TABLE IF NOT EXISTS pollutant (
  id integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  name varchar(100) NOT NULL UNIQUE,
  unit varchar(50) NOT NULL,
  description text
);

-- Station: Air quality monitoring stations
CREATE TABLE IF NOT EXISTS station (
  id integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  name varchar(255) NOT NULL,
  latitude double precision NOT NULL,
  longitude double precision NOT NULL,
  city varchar(255) NOT NULL,
  country varchar(255) NOT NULL,
  region_id integer REFERENCES map_region (id) ON DELETE SET NULL
);

-- AirQualityReading: Individual sensor readings from stations
CREATE TABLE IF NOT EXISTS air_quality_reading (
  id integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  station_id integer NOT NULL REFERENCES station (id) ON DELETE CASCADE,
  pollutant_id integer NOT NULL REFERENCES pollutant (id) ON DELETE RESTRICT,
  datetime timestamp with time zone NOT NULL,
  value double precision NOT NULL,
  aqi integer
);

-- AirQualityDailyStats: Aggregated daily statistics for analytics
CREATE TABLE IF NOT EXISTS air_quality_daily_stats (
  id integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  station_id integer NOT NULL REFERENCES station (id) ON DELETE CASCADE,
  pollutant_id integer NOT NULL REFERENCES pollutant (id) ON DELETE RESTRICT,
  date date NOT NULL,
  avg_value double precision,
  avg_aqi integer,
  max_aqi integer,
  min_aqi integer,
  readings_count integer DEFAULT 0
);

-- ============================================================================
-- USERS & ACCESS CONTROL (Operational)
-- ============================================================================

-- Role: User roles (Citizen, Researcher, Admin)
CREATE TABLE IF NOT EXISTS role (
  id integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  name varchar(100) NOT NULL UNIQUE
);

-- Permission: System permissions
CREATE TABLE IF NOT EXISTS permission (
  id integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  name varchar(100) NOT NULL UNIQUE
);

-- RolePermission: Many-to-many relationship between roles and permissions
CREATE TABLE IF NOT EXISTS role_permission (
  role_id integer NOT NULL REFERENCES role (id) ON DELETE CASCADE,
  permission_id integer NOT NULL REFERENCES permission (id) ON DELETE CASCADE,
  PRIMARY KEY (role_id, permission_id)
);

-- AppUser: Application users
CREATE TABLE IF NOT EXISTS app_user (
  id integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  name varchar(255) NOT NULL,
  email varchar(255) NOT NULL UNIQUE,
  password_hash varchar(255) NOT NULL,
  location varchar(255),
  role_id integer NOT NULL REFERENCES role (id) ON DELETE RESTRICT
);

-- ============================================================================
-- ALERTS & PERSONALIZATION (Operational)
-- ============================================================================

-- Alert: User-configured pollution alerts
CREATE TABLE IF NOT EXISTS alert (
  id integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  user_id integer NOT NULL REFERENCES app_user (id) ON DELETE CASCADE,
  pollutant_id integer NOT NULL REFERENCES pollutant (id) ON DELETE CASCADE,
  threshold double precision NOT NULL,
  method varchar(50) NOT NULL, -- 'email', 'sms', etc.
  triggered_at timestamp with time zone
);

-- Recommendation: Health recommendations based on pollution levels
CREATE TABLE IF NOT EXISTS recommendation (
  id integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  user_id integer NOT NULL REFERENCES app_user (id) ON DELETE CASCADE,
  location varchar(255) NOT NULL,
  pollution_level integer NOT NULL, -- AQI value
  message text NOT NULL,
  created_at timestamp with time zone NOT NULL DEFAULT NOW()
);

-- ProductRecommendation: Suggested protection products linked to recommendations
CREATE TABLE IF NOT EXISTS product_recommendation (
  id integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  recommendation_id integer NOT NULL REFERENCES recommendation (id) ON DELETE CASCADE,
  product_name varchar(255) NOT NULL,
  product_type varchar(100) NOT NULL, -- 'mask', 'respirator', etc.
  product_url varchar(500)
);

-- ============================================================================
-- REPORTING & ANALYTICS
-- ============================================================================

-- Report: Metadata for generated reports
CREATE TABLE IF NOT EXISTS report (
  id integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  user_id integer NOT NULL REFERENCES app_user (id) ON DELETE CASCADE,
  created_at timestamp with time zone NOT NULL DEFAULT NOW(),
  city varchar(255) NOT NULL,
  start_date date NOT NULL,
  end_date date NOT NULL,
  station_id integer REFERENCES station (id) ON DELETE SET NULL,
  pollutant_id integer REFERENCES pollutant (id) ON DELETE SET NULL,
  file_path varchar(500)
);

-- ============================================================================
-- INDEXES for Performance Optimization
-- ============================================================================

-- Geospatial index
CREATE INDEX IF NOT EXISTS idx_map_region_geom ON map_region USING GIST (geom);

-- Station indexes
CREATE INDEX IF NOT EXISTS idx_station_region_id ON station (region_id);
CREATE INDEX IF NOT EXISTS idx_station_city ON station (city);
CREATE INDEX IF NOT EXISTS idx_station_location ON station (latitude, longitude);

-- AirQualityReading indexes
CREATE INDEX IF NOT EXISTS idx_air_quality_reading_station_id ON air_quality_reading (station_id);
CREATE INDEX IF NOT EXISTS idx_air_quality_reading_pollutant_id ON air_quality_reading (pollutant_id);
CREATE INDEX IF NOT EXISTS idx_air_quality_reading_datetime ON air_quality_reading (datetime DESC);
-- Composite index for frequent queries
CREATE INDEX IF NOT EXISTS idx_air_quality_reading_composite ON air_quality_reading (station_id, pollutant_id, datetime DESC);

-- AirQualityDailyStats indexes
CREATE INDEX IF NOT EXISTS idx_air_quality_daily_stats_station_id ON air_quality_daily_stats (station_id);
CREATE INDEX IF NOT EXISTS idx_air_quality_daily_stats_pollutant_id ON air_quality_daily_stats (pollutant_id);
CREATE INDEX IF NOT EXISTS idx_air_quality_daily_stats_date ON air_quality_daily_stats (date DESC);
-- Composite index for analytics queries
CREATE INDEX IF NOT EXISTS idx_air_quality_daily_stats_composite ON air_quality_daily_stats (station_id, pollutant_id, date DESC);

-- AppUser indexes
CREATE INDEX IF NOT EXISTS idx_app_user_email ON app_user (email);
CREATE INDEX IF NOT EXISTS idx_app_user_role_id ON app_user (role_id);

-- Alert indexes
CREATE INDEX IF NOT EXISTS idx_alert_user_id ON alert (user_id);
CREATE INDEX IF NOT EXISTS idx_alert_pollutant_id ON alert (pollutant_id);

-- Recommendation indexes
CREATE INDEX IF NOT EXISTS idx_recommendation_user_id ON recommendation (user_id);
CREATE INDEX IF NOT EXISTS idx_recommendation_created_at ON recommendation (created_at DESC);

-- ProductRecommendation indexes
CREATE INDEX IF NOT EXISTS idx_product_recommendation_recommendation_id ON product_recommendation (recommendation_id);

-- Report indexes
CREATE INDEX IF NOT EXISTS idx_report_user_id ON report (user_id);
CREATE INDEX IF NOT EXISTS idx_report_created_at ON report (created_at DESC);
CREATE INDEX IF NOT EXISTS idx_report_station_id ON report (station_id);
CREATE INDEX IF NOT EXISTS idx_report_pollutant_id ON report (pollutant_id);

-- ============================================================================
-- Comments for Documentation
-- ============================================================================

COMMENT ON TABLE map_region IS 'Geographical regions with polygon boundaries for visualization';
COMMENT ON TABLE pollutant IS 'Catalog of air pollutants (PM2.5, PM10, O3, etc.)';
COMMENT ON TABLE station IS 'Air quality monitoring stations with geolocation';
COMMENT ON TABLE air_quality_reading IS 'Individual sensor readings from monitoring stations';
COMMENT ON TABLE air_quality_daily_stats IS 'Aggregated daily statistics for analytics and reporting';
COMMENT ON TABLE role IS 'User roles: Citizen, Researcher, Admin';
COMMENT ON TABLE permission IS 'System permissions for role-based access control';
COMMENT ON TABLE role_permission IS 'Maps permissions to roles';
COMMENT ON TABLE app_user IS 'Application users with authentication credentials';
COMMENT ON TABLE alert IS 'User-configured pollution threshold alerts';
COMMENT ON TABLE recommendation IS 'Health recommendations based on pollution levels';
COMMENT ON TABLE product_recommendation IS 'Protection products suggested with recommendations';
COMMENT ON TABLE report IS 'Metadata for generated analytical reports';
