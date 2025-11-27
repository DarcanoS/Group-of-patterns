import httpClient from './httpClient';

// Obtener configuración del usuario actual (requiere autenticación)
export async function getUserSettings() {
  try {
    return await httpClient.get('/settings', true);
  } catch (error) {
    console.error('Error fetching user settings:', error);
    throw error;
  }
}

// Actualizar configuración del usuario
export async function updateUserSettings(settings) {
  try {
    return await httpClient.put('/settings', settings, true);
  } catch (error) {
    console.error('Error updating user settings:', error);
    throw error;
  }
}

// Obtener preferencias locales del navegador (fallback si no está autenticado)
export function getLocalSettings() {
  const settings = localStorage.getItem('user_settings');
  return settings ? JSON.parse(settings) : {
    notifications: true,
    theme: 'light',
    language: 'es',
    location: 'Bogotá'
  };
}

// Guardar preferencias locales
export function saveLocalSettings(settings) {
  localStorage.setItem('user_settings', JSON.stringify(settings));
}
