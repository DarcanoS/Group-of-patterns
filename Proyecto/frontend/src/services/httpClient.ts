// HTTP Client para comunicación con el backend
const API_BASE_URL = 'http://localhost:8000/api/v1';

class HttpClient {
  private baseURL: string;

  constructor(baseURL: string) {
    this.baseURL = baseURL;
  }

  private getHeaders(includeAuth: boolean = true): HeadersInit {
    const headers: HeadersInit = {
      'Content-Type': 'application/json',
    };

    if (includeAuth) {
      const token = localStorage.getItem('access_token');
      if (token) {
        headers['Authorization'] = `Bearer ${token}`;
      }
    }

    return headers;
  }

  async get<T>(endpoint: string, includeAuth: boolean = true): Promise<T> {
    const response = await fetch(`${this.baseURL}${endpoint}`, {
      method: 'GET',
      headers: this.getHeaders(includeAuth),
    });

    if (!response.ok) {
      throw new Error(`HTTP Error: ${response.status}`);
    }

    return response.json();
  }

  async post<T>(endpoint: string, data: any, includeAuth: boolean = true, isFormData: boolean = false): Promise<T> {
    const headers: HeadersInit = includeAuth
      ? { 'Authorization': `Bearer ${localStorage.getItem('access_token')}` }
      : {};

    if (!isFormData) {
      headers['Content-Type'] = 'application/json';
    }

    const response = await fetch(`${this.baseURL}${endpoint}`, {
      method: 'POST',
      headers,
      body: isFormData ? data : JSON.stringify(data),
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.detail || `HTTP Error: ${response.status}`);
    }

    return response.json();
  }

  async put<T>(endpoint: string, data: any, includeAuth: boolean = true): Promise<T> {
    const response = await fetch(`${this.baseURL}${endpoint}`, {
      method: 'PUT',
      headers: this.getHeaders(includeAuth),
      body: JSON.stringify(data),
    });

    if (!response.ok) {
      throw new Error(`HTTP Error: ${response.status}`);
    }

    return response.json();
  }

  async delete<T>(endpoint: string, includeAuth: boolean = true): Promise<T> {
    const response = await fetch(`${this.baseURL}${endpoint}`, {
      method: 'DELETE',
      headers: this.getHeaders(includeAuth),
    });

    if (!response.ok) {
      throw new Error(`HTTP Error: ${response.status}`);
    }

    return response.json();
  }
}

const httpClient = new HttpClient(API_BASE_URL);
export default httpClient;

