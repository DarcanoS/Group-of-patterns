import httpClient from './httpClient';

interface HealthStatus {
  status: string;
  database: string;
  message: string;
}

interface User {
  id: number;
  email: string;
  full_name: string;
  role: {
    id: number;
    name: string;
    description?: string;
  };
  created_at: string;
  is_active: boolean;
}

interface Station {
  id: number;
  name: string;
  latitude: number;
  longitude: number;
  city: string;
  country: string;
  is_active: boolean;
  created_at: string;
}

// Obtener estado del sistema
export async function getHealthStatus(): Promise<HealthStatus> {
  return await httpClient.get<HealthStatus>('/admin/health', false);
}

// Obtener lista de usuarios
export async function getUsers(skip: number = 0, limit: number = 100): Promise<User[]> {
  return await httpClient.get<User[]>(`/admin/users?skip=${skip}&limit=${limit}`);
}

// Obtener lista de estaciones
export async function getStations(skip: number = 0, limit: number = 100): Promise<Station[]> {
  return await httpClient.get<Station[]>(`/admin/stations?skip=${skip}&limit=${limit}`);
}

// Actualizar rol de usuario
export async function updateUserRole(userId: number, roleId: number): Promise<User> {
  return await httpClient.put<User>(`/admin/users/${userId}/role`, { role_id: roleId });
}


