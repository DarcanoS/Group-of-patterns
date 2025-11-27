import httpClient from './httpClient';

interface LoginResponse {
  access_token: string;
  token_type: string;
  user: {
    id: number;
    email: string;
    full_name: string;
    role: {
      id: number;
      name: string;
      description: string;
    };
    created_at: string;
    is_active: boolean;
  };
}

interface User {
  id: number;
  email: string;
  full_name: string;
  role: {
    id: number;
    name: string;
    description: string;
  };
  created_at: string;
  is_active: boolean;
}

export async function login(email: string, password: string): Promise<LoginResponse> {
  // El backend espera form-data con username (email) y password
  const formData = new URLSearchParams();
  formData.append('username', email);
  formData.append('password', password);

  const response = await httpClient.post<LoginResponse>(
    '/auth/login',
    formData,
    false, // No incluir auth en login
    true   // Es form-data
  );

  // Guardar token en localStorage
  localStorage.setItem('access_token', response.access_token);
  localStorage.setItem('user', JSON.stringify(response.user));

  return response;
}

export async function getCurrentUser(): Promise<User> {
  return await httpClient.get<User>('/auth/me');
}

export function logout(): void {
  localStorage.removeItem('access_token');
  localStorage.removeItem('user');
}

export function getStoredUser(): User | null {
  const userStr = localStorage.getItem('user');
  return userStr ? JSON.parse(userStr) : null;
}

export function isAuthenticated(): boolean {
  return !!localStorage.getItem('access_token');
}

export function getUserRole(): string | null {
  const user = getStoredUser();
  return user?.role?.name || null;
}

