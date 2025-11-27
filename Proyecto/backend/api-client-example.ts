/**
 * Example API Client for Air Quality Monitoring System
 *
 * This is a ready-to-use API client that frontend can integrate.
 * Supports TypeScript and includes error handling, authentication, and all endpoints.
 *
 * Usage:
 * ```typescript
 * import { AirQualityAPI } from './api-client';
 *
 * const api = new AirQualityAPI('http://localhost:8000/api/v1');
 *
 * // Login
 * const { access_token, user } = await api.auth.login('user@example.com', 'password');
 *
 * // Set token for authenticated requests
 * api.setToken(access_token);
 *
 * // Get dashboard data
 * const dashboard = await api.airQuality.getDashboard({ city: 'New York' });
 * ```
 */

// ============================================================================
// BASE API CLIENT
// ============================================================================

class APIClient {
  private baseURL: string;
  private token: string | null = null;

  constructor(baseURL: string) {
    this.baseURL = baseURL;
  }

  setToken(token: string) {
    this.token = token;
  }

  clearToken() {
    this.token = null;
  }

  private getHeaders(includeAuth: boolean = true): HeadersInit {
    const headers: HeadersInit = {
      'Content-Type': 'application/json',
    };

    if (includeAuth && this.token) {
      headers['Authorization'] = `Bearer ${this.token}`;
    }

    return headers;
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {},
    requireAuth: boolean = false
  ): Promise<T> {
    const url = `${this.baseURL}${endpoint}`;

    const config: RequestInit = {
      ...options,
      headers: this.getHeaders(requireAuth),
    };

    try {
      const response = await fetch(url, config);

      if (!response.ok) {
        const error = await response.json().catch(() => ({ detail: 'Unknown error' }));
        throw new APIError(response.status, error.detail || 'Request failed');
      }

      return await response.json();
    } catch (error) {
      if (error instanceof APIError) {
        throw error;
      }
      throw new APIError(0, 'Network error or server unavailable');
    }
  }

  protected async get<T>(endpoint: string, params?: Record<string, any>, requireAuth: boolean = false): Promise<T> {
    const queryString = params ? '?' + new URLSearchParams(this.cleanParams(params)).toString() : '';
    return this.request<T>(`${endpoint}${queryString}`, { method: 'GET' }, requireAuth);
  }

  protected async post<T>(endpoint: string, data?: any, requireAuth: boolean = false): Promise<T> {
    return this.request<T>(endpoint, {
      method: 'POST',
      body: JSON.stringify(data),
    }, requireAuth);
  }

  protected async postForm<T>(endpoint: string, data: Record<string, string>, requireAuth: boolean = false): Promise<T> {
    const formData = new URLSearchParams(data);
    const url = `${this.baseURL}${endpoint}`;

    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: formData,
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'Unknown error' }));
      throw new APIError(response.status, error.detail || 'Request failed');
    }

    return await response.json();
  }

  protected async put<T>(endpoint: string, data?: any, requireAuth: boolean = false): Promise<T> {
    return this.request<T>(endpoint, {
      method: 'PUT',
      body: JSON.stringify(data),
    }, requireAuth);
  }

  protected async delete<T>(endpoint: string, requireAuth: boolean = false): Promise<T> {
    return this.request<T>(endpoint, { method: 'DELETE' }, requireAuth);
  }

  private cleanParams(params: Record<string, any>): Record<string, string> {
    const cleaned: Record<string, string> = {};
    for (const [key, value] of Object.entries(params)) {
      if (value !== undefined && value !== null) {
        cleaned[key] = String(value);
      }
    }
    return cleaned;
  }
}

// ============================================================================
// CUSTOM ERROR CLASS
// ============================================================================

class APIError extends Error {
  constructor(public statusCode: number, message: string) {
    super(message);
    this.name = 'APIError';
  }
}

// ============================================================================
// AUTH SERVICE
// ============================================================================

class AuthService extends APIClient {
  async login(email: string, password: string) {
    return this.postForm<any>('/auth/login', {
      username: email,
      password: password,
    });
  }

  async getCurrentUser() {
    return this.get<any>('/auth/me', undefined, true);
  }
}

// ============================================================================
// STATIONS SERVICE
// ============================================================================

class StationsService extends APIClient {
  async list(params?: {
    skip?: number;
    limit?: number;
    city?: string;
    country?: string;
    region_id?: number;
  }) {
    return this.get<any[]>('/stations', params);
  }

  async getById(stationId: number) {
    return this.get<any>(`/stations/${stationId}`);
  }

  async getCurrentReadings(stationId: number) {
    return this.get<any>(`/stations/${stationId}/readings/current`);
  }
}

// ============================================================================
// AIR QUALITY SERVICE
// ============================================================================

class AirQualityService extends APIClient {
  async getCurrentAQI(city: string) {
    return this.get<any>('/air-quality/current', { city });
  }

  async getDashboard(params: { city?: string; station_id?: number }) {
    return this.get<any>('/air-quality/dashboard', params);
  }

  async getDailyStats(params?: {
    station_id?: number;
    pollutant_id?: number;
    start_date?: string;
    end_date?: string;
    skip?: number;
    limit?: number;
  }) {
    return this.get<any[]>('/air-quality/daily-stats', params);
  }
}

// ============================================================================
// RECOMMENDATIONS SERVICE
// ============================================================================

class RecommendationsService extends APIClient {
  async getCurrent(params?: { location?: string; aqi?: number }) {
    return this.get<any>('/recommendations/current', params, true);
  }

  async getHistory(params?: { skip?: number; limit?: number }) {
    return this.get<any[]>('/recommendations/history', params, true);
  }
}

// ============================================================================
// ADMIN SERVICE
// ============================================================================

class AdminService extends APIClient {
  async healthCheck() {
    return this.get<any>('/admin/health');
  }

  // Station Management
  async listStations(params?: { skip?: number; limit?: number }) {
    return this.get<any[]>('/admin/stations', params, true);
  }

  async createStation(data: {
    name: string;
    latitude: number;
    longitude: number;
    city: string;
    country: string;
    region_id: number;
  }) {
    return this.post<any>('/admin/stations', data, true);
  }

  async updateStation(stationId: number, data: any) {
    return this.put<any>(`/admin/stations/${stationId}`, data, true);
  }

  async deleteStation(stationId: number) {
    return this.delete<any>(`/admin/stations/${stationId}`, true);
  }

  // User Management
  async listUsers(params?: { skip?: number; limit?: number }) {
    return this.get<any[]>('/admin/users', params, true);
  }

  async updateUserRole(userId: number, roleId: number) {
    return this.put<any>(`/admin/users/${userId}/role`, { role_id: roleId }, true);
  }
}

// ============================================================================
// SETTINGS SERVICE
// ============================================================================

class SettingsService extends APIClient {
  async getPreferences() {
    return this.get<any>('/settings/preferences', undefined, true);
  }

  async updatePreferences(data: {
    theme?: string;
    language?: string;
    notifications_enabled?: boolean;
    email_alerts?: boolean;
    aqi_threshold?: number;
    preferred_units?: string;
  }) {
    return this.put<any>('/settings/preferences', data, true);
  }

  async getDashboardConfig() {
    return this.get<any>('/settings/dashboard', undefined, true);
  }

  async updateDashboardConfig(data: any) {
    return this.put<any>('/settings/dashboard', data, true);
  }
}

// ============================================================================
// REPORTS SERVICE
// ============================================================================

class ReportsService extends APIClient {
  async create(data: {
    city: string;
    start_date: string;
    end_date: string;
    station_id?: number;
    pollutant_id?: number;
  }) {
    return this.post<any>('/reports', data, true);
  }

  async list(params?: { skip?: number; limit?: number }) {
    return this.get<any[]>('/reports', params, true);
  }

  async getById(reportId: number) {
    return this.get<any>(`/reports/${reportId}`, undefined, true);
  }
}

// ============================================================================
// MAIN API CLASS
// ============================================================================

export class AirQualityAPI {
  public auth: AuthService;
  public stations: StationsService;
  public airQuality: AirQualityService;
  public recommendations: RecommendationsService;
  public admin: AdminService;
  public settings: SettingsService;
  public reports: ReportsService;

  constructor(baseURL: string = 'http://localhost:8000/api/v1') {
    this.auth = new AuthService(baseURL);
    this.stations = new StationsService(baseURL);
    this.airQuality = new AirQualityService(baseURL);
    this.recommendations = new RecommendationsService(baseURL);
    this.admin = new AdminService(baseURL);
    this.settings = new SettingsService(baseURL);
    this.reports = new ReportsService(baseURL);
  }

  setToken(token: string) {
    this.auth.setToken(token);
    this.stations.setToken(token);
    this.airQuality.setToken(token);
    this.recommendations.setToken(token);
    this.admin.setToken(token);
    this.settings.setToken(token);
    this.reports.setToken(token);
  }

  clearToken() {
    this.auth.clearToken();
    this.stations.clearToken();
    this.airQuality.clearToken();
    this.recommendations.clearToken();
    this.admin.clearToken();
    this.settings.clearToken();
    this.reports.clearToken();
  }
}

// ============================================================================
// USAGE EXAMPLES
// ============================================================================

/**
 * Example 1: Login and get current user
 */
async function example1() {
  const api = new AirQualityAPI();

  try {
    // Login
    const loginResponse = await api.auth.login('user@example.com', 'password123');
    console.log('Logged in:', loginResponse.user);

    // Set token for future requests
    api.setToken(loginResponse.access_token);

    // Get current user info
    const user = await api.auth.getCurrentUser();
    console.log('Current user:', user);
  } catch (error) {
    if (error instanceof APIError) {
      console.error(`API Error ${error.statusCode}:`, error.message);
    }
  }
}

/**
 * Example 2: Get dashboard data for a city
 */
async function example2() {
  const api = new AirQualityAPI();

  try {
    const dashboard = await api.airQuality.getDashboard({ city: 'New York' });
    console.log('Dashboard data:', dashboard);
    console.log('Current AQI:', dashboard.daily_stats.avg_aqi);
    console.log('Risk level:', dashboard.risk_assessment.level);
  } catch (error) {
    console.error('Error fetching dashboard:', error);
  }
}

/**
 * Example 3: Get personalized recommendation
 */
async function example3(token: string) {
  const api = new AirQualityAPI();
  api.setToken(token);

  try {
    const recommendation = await api.recommendations.getCurrent({
      location: 'New York'
    });

    console.log('Recommendation:', recommendation.recommendation_text);
    console.log('Health advice:', recommendation.health_advice);
    console.log('Recommended products:', recommendation.products);
  } catch (error) {
    console.error('Error fetching recommendation:', error);
  }
}

/**
 * Example 4: List all stations
 */
async function example4() {
  const api = new AirQualityAPI();

  try {
    const stations = await api.stations.list({
      city: 'New York',
      limit: 10
    });

    console.log(`Found ${stations.length} stations`);
    stations.forEach(station => {
      console.log(`- ${station.name} (${station.city})`);
    });
  } catch (error) {
    console.error('Error fetching stations:', error);
  }
}

/**
 * Example 5: Admin - Create new station
 */
async function example5(adminToken: string) {
  const api = new AirQualityAPI();
  api.setToken(adminToken);

  try {
    const newStation = await api.admin.createStation({
      name: 'Central Park Station',
      latitude: 40.7829,
      longitude: -73.9654,
      city: 'New York',
      country: 'USA',
      region_id: 1
    });

    console.log('Station created:', newStation);
  } catch (error) {
    if (error instanceof APIError && error.statusCode === 403) {
      console.error('Permission denied: Admin role required');
    } else {
      console.error('Error creating station:', error);
    }
  }
}

/**
 * Example 6: Update user preferences
 */
async function example6(token: string) {
  const api = new AirQualityAPI();
  api.setToken(token);

  try {
    const preferences = await api.settings.updatePreferences({
      theme: 'dark',
      language: 'es',
      notifications_enabled: true,
      aqi_threshold: 100
    });

    console.log('Preferences updated:', preferences);
  } catch (error) {
    console.error('Error updating preferences:', error);
  }
}

/**
 * Example 7: Generate and download report
 */
async function example7(token: string) {
  const api = new AirQualityAPI();
  api.setToken(token);

  try {
    const report = await api.reports.create({
      city: 'New York',
      start_date: '2025-11-01',
      end_date: '2025-11-27',
      station_id: 1,
      pollutant_id: 1
    });

    console.log('Report created:', report);
    console.log('File path:', report.file_path);
  } catch (error) {
    console.error('Error creating report:', error);
  }
}

// Export for use in other modules
export { APIError };

// Export as default
export default AirQualityAPI;

