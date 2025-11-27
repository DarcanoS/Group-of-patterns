/**
 * TypeScript Type Definitions for Air Quality Monitoring API
 * Base URL: http://localhost:8000/api/v1
 * Version: 1.0.0
 * Generated: 2025-11-27
 */

// ============================================================================
// AUTH TYPES
// ============================================================================

export interface LoginRequest {
  username: string; // email
  password: string;
}

export interface LoginResponse {
  access_token: string;
  token_type: "bearer";
  user: User;
}

// ============================================================================
// USER & ROLE TYPES
// ============================================================================

export interface Role {
  id: number;
  name: "Citizen" | "Researcher" | "Admin";
  description: string;
}

export interface User {
  id: number;
  email: string;
  full_name: string;
  role: Role;
  created_at: string; // ISO 8601
  is_active: boolean;
}

export interface UserUpdateRole {
  role_id: number;
}

// ============================================================================
// STATION TYPES
// ============================================================================

export interface Region {
  id: number;
  name: string;
  description: string;
}

export interface Station {
  id: number;
  name: string;
  latitude: number;
  longitude: number;
  city: string;
  country: string;
  region: Region;
  is_active: boolean;
  created_at: string;
}

export interface StationCreate {
  name: string;
  latitude: number;
  longitude: number;
  city: string;
  country: string;
  region_id: number;
}

export interface StationUpdate {
  name?: string;
  latitude?: number;
  longitude?: number;
  city?: string;
  country?: string;
  region_id?: number;
  is_active?: boolean;
}

export interface StationListParams {
  skip?: number;
  limit?: number;
  city?: string;
  country?: string;
  region_id?: number;
}

// ============================================================================
// POLLUTANT & READING TYPES
// ============================================================================

export type PollutantName = "PM2.5" | "PM10" | "O3" | "NO2" | "SO2" | "CO";

export interface Pollutant {
  id: number;
  name: PollutantName;
  unit: string; // "µg/m³" | "ppm"
  description: string;
}

export interface Reading {
  pollutant: Pollutant;
  value: number;
  aqi: number;
  timestamp: string; // ISO 8601
}

export interface CurrentReadingsResponse {
  station: {
    id: number;
    name: string;
    city: string;
  };
  readings: Reading[];
  last_updated: string;
}

// ============================================================================
// AIR QUALITY TYPES
// ============================================================================

export type RiskLevel =
  | "Good"
  | "Moderate"
  | "Unhealthy for Sensitive Groups"
  | "Unhealthy"
  | "Very Unhealthy"
  | "Hazardous";

export interface RiskCategory {
  level: RiskLevel;
  color: string; // Hex color code
  health_implications: string;
  cautionary_statement: string;
}

export interface CurrentAQIResponse {
  city: string;
  aqi: number;
  primary_pollutant: PollutantName;
  risk_category: RiskCategory;
  timestamp: string;
  station: {
    id: number;
    name: string;
  };
}

export interface DailyStatsResponse {
  id: number;
  date: string; // YYYY-MM-DD
  station_id: number;
  pollutant_id: number;
  avg_value: number;
  max_value: number;
  min_value: number;
  avg_aqi: number;
  readings_count: number;
}

export interface DailyStatsParams {
  station_id?: number;
  pollutant_id?: number;
  start_date?: string; // YYYY-MM-DD
  end_date?: string; // YYYY-MM-DD
  skip?: number;
  limit?: number;
}

export interface DashboardResponse {
  station: {
    id: number;
    name: string;
    city: string;
    country: string;
    latitude: number;
    longitude: number;
  };
  current_readings: Reading[];
  daily_stats: {
    date: string;
    avg_aqi: number;
    max_aqi: number;
    min_aqi: number;
    dominant_pollutant: PollutantName;
  };
  risk_assessment: {
    level: RiskLevel;
    color: string;
    health_implications: string;
    recommended_actions: string[];
  };
  last_updated: string;
}

export interface DashboardParams {
  city?: string;
  station_id?: number;
}

// ============================================================================
// RECOMMENDATION TYPES
// ============================================================================

export type ProductType = "mask" | "air_purifier" | "monitor" | "medication";
export type ProductPriority = "low" | "medium" | "high";

export interface ProductRecommendation {
  type: ProductType;
  name: string;
  description: string;
  priority: ProductPriority;
}

export interface RecommendationResponse {
  id: number;
  user_id: number;
  location: string;
  aqi: number;
  risk_level: string;
  recommendation_text: string;
  health_advice: string[];
  actions: string[];
  products: ProductRecommendation[];
  created_at: string;
}

export interface RecommendationParams {
  location?: string;
  aqi?: number;
}

export interface RecommendationHistoryParams {
  skip?: number;
  limit?: number;
}

// ============================================================================
// SETTINGS TYPES
// ============================================================================

export type Theme = "light" | "dark";
export type Language = "en" | "es";
export type Units = "metric" | "imperial";

export interface UserPreferences {
  user_id: number;
  theme: Theme;
  language: Language;
  notifications_enabled: boolean;
  email_alerts: boolean;
  aqi_threshold: number;
  preferred_units: Units;
}

export interface SettingsUpdateRequest {
  theme?: Theme;
  language?: Language;
  notifications_enabled?: boolean;
  email_alerts?: boolean;
  aqi_threshold?: number;
  preferred_units?: Units;
}

export type WidgetType = "gauge" | "chart" | "map" | "table" | "alert";
export type LayoutType = "grid" | "flex" | "masonry";

export interface Widget {
  id: string;
  type: WidgetType;
  position: {
    x: number;
    y: number;
  };
  size: {
    width: number;
    height: number;
  };
  settings: Record<string, any>;
}

export interface DashboardConfig {
  user_id: number;
  widgets: Widget[];
  layout: LayoutType;
  refresh_interval: number; // seconds
}

// ============================================================================
// REPORT TYPES
// ============================================================================

export type ReportStatus = "pending" | "processing" | "completed" | "failed";

export interface ReportCreate {
  city: string;
  start_date: string; // YYYY-MM-DD
  end_date: string; // YYYY-MM-DD
  station_id?: number;
  pollutant_id?: number;
}

export interface ReportResponse {
  id: number;
  user_id: number;
  city: string;
  start_date: string;
  end_date: string;
  station_id: number | null;
  pollutant_id: number | null;
  file_path: string;
  status: ReportStatus;
  created_at: string;
}

export interface ReportListParams {
  skip?: number;
  limit?: number;
}

// ============================================================================
// ADMIN TYPES
// ============================================================================

export interface HealthCheckResponse {
  status: "healthy" | "unhealthy";
  database: "connected" | "error";
  message: string;
}

export interface MessageResponse {
  message: string;
}

// ============================================================================
// ERROR TYPES
// ============================================================================

export interface APIError {
  detail: string;
}

export interface ValidationError {
  detail: Array<{
    loc: string[];
    msg: string;
    type: string;
  }>;
}

// ============================================================================
// API CLIENT CONFIGURATION
// ============================================================================

export interface APIConfig {
  baseURL: string;
  timeout?: number;
  headers?: Record<string, string>;
}

export interface AuthHeaders {
  Authorization: string; // "Bearer {token}"
}

// ============================================================================
// UTILITY TYPES
// ============================================================================

export interface PaginationParams {
  skip?: number;
  limit?: number;
}

export interface DateRangeParams {
  start_date?: string; // YYYY-MM-DD
  end_date?: string; // YYYY-MM-DD
}

// ============================================================================
// API RESPONSE TYPES (Generic wrappers)
// ============================================================================

export type APIResponse<T> = T;
export type APIListResponse<T> = T[];

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  skip: number;
  limit: number;
}

// ============================================================================
// CONSTANTS
// ============================================================================

export const API_BASE_URL = "http://localhost:8000/api/v1";

export const ENDPOINTS = {
  // Auth
  LOGIN: "/auth/login",
  ME: "/auth/me",

  // Stations
  STATIONS: "/stations",
  STATION_BY_ID: (id: number) => `/stations/${id}`,
  STATION_READINGS: (id: number) => `/stations/${id}/readings/current`,

  // Air Quality
  CURRENT_AQI: "/air-quality/current",
  DASHBOARD: "/air-quality/dashboard",
  DAILY_STATS: "/air-quality/daily-stats",

  // Recommendations
  CURRENT_RECOMMENDATION: "/recommendations/current",
  RECOMMENDATION_HISTORY: "/recommendations/history",

  // Admin
  HEALTH: "/admin/health",
  ADMIN_STATIONS: "/admin/stations",
  ADMIN_STATION_BY_ID: (id: number) => `/admin/stations/${id}`,
  ADMIN_USERS: "/admin/users",
  ADMIN_USER_ROLE: (id: number) => `/admin/users/${id}/role`,

  // Settings
  PREFERENCES: "/settings/preferences",
  DASHBOARD_CONFIG: "/settings/dashboard",

  // Reports
  REPORTS: "/reports",
  REPORT_BY_ID: (id: number) => `/reports/${id}`,
} as const;

export const RISK_LEVEL_COLORS: Record<RiskLevel, string> = {
  "Good": "#4CAF50",
  "Moderate": "#FFEB3B",
  "Unhealthy for Sensitive Groups": "#FF9800",
  "Unhealthy": "#F44336",
  "Very Unhealthy": "#9C27B0",
  "Hazardous": "#8B0000",
};

export const AQI_RANGES = {
  GOOD: { min: 0, max: 50 },
  MODERATE: { min: 51, max: 100 },
  UNHEALTHY_SENSITIVE: { min: 101, max: 150 },
  UNHEALTHY: { min: 151, max: 200 },
  VERY_UNHEALTHY: { min: 201, max: 300 },
  HAZARDOUS: { min: 301, max: 500 },
} as const;

