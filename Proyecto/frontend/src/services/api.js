import httpClient from './httpClient';

// Obtener calidad del aire actual por ciudad
export async function getAirQuality(city = 'Bogotá') {
  try {
    const currentAQI = await httpClient.get(`/air-quality/current?city=${encodeURIComponent(city)}`, false);

    // Obtener estaciones de la ciudad
    const stations = await httpClient.get(`/stations?city=${encodeURIComponent(city)}&limit=10`, false);

    // Obtener lecturas de cada estación con información completa
    const stationPromises = stations.slice(0, 3).map(async (station) => {
      try {
        const data = await httpClient.get(`/stations/${station.id}/readings/current`, false);
        return {
          id: station.id,
          name: data.station.name,
          city: data.station.city,
          country: data.station.country,
          latitude: data.station.latitude,
          longitude: data.station.longitude,
          readings: data.readings || [],
          maxAqi: Math.max(...data.readings.map(r => r.aqi || 0).filter(aqi => aqi > 0), 0)
        };
      } catch {
        return { 
          id: station.id,
          name: station.name, 
          city: station.city,
          readings: [],
          maxAqi: 0 
        };
      }
    });

    const stationsData = await Promise.all(stationPromises);

    return {
      city: currentAQI.city,
      level: currentAQI.category || 'Unknown',
      aqi: currentAQI.aqi,
      primaryPollutant: currentAQI.dominant_pollutant,
      riskCategory: {
        level: currentAQI.category || 'Unknown',
        color: currentAQI.color,
        health_implications: currentAQI.health_message || 'No data available',
        cautionary_statement: getCautionaryStatement(currentAQI.aqi)
      },
      updatedAt: new Date(currentAQI.timestamp).toLocaleString(),
      history: [currentAQI.aqi], // Simplificado, se puede expandir con datos históricos
      stations: stationsData,
      products: [] // Se llenará con recomendaciones
    };
  } catch (error) {
    console.error('Error fetching air quality:', error);
    throw error;
  }
}

// Función auxiliar para generar mensajes de precaución según el AQI
function getCautionaryStatement(aqi) {
  if (aqi <= 50) {
    return 'Air quality is good. Enjoy your outdoor activities!';
  } else if (aqi <= 100) {
    return 'Unusually sensitive people should consider reducing prolonged or heavy outdoor exertion.';
  } else if (aqi <= 150) {
    return 'People with respiratory disease should limit prolonged outdoor exertion.';
  } else if (aqi <= 200) {
    return 'Everyone should avoid prolonged outdoor exertion. People with respiratory disease should avoid all outdoor exertion.';
  } else if (aqi <= 300) {
    return 'Everyone should avoid all outdoor exertion.';
  } else {
    return 'Everyone should remain indoors and keep activity levels low.';
  }
}

// Obtener datos completos del dashboard
export async function getDashboardData(city = 'Bogotá') {
  try {
    return await httpClient.get(`/air-quality/dashboard?city=${encodeURIComponent(city)}`, false);
  } catch (error) {
    console.error('Error fetching dashboard data:', error);
    throw error;
  }
}

// Obtener recomendación personalizada (requiere autenticación)
export async function getCurrentRecommendation(location = 'Bogotá', aqi = null) {
  try {
    let endpoint = `/recommendations/current?location=${encodeURIComponent(location)}`;
    if (aqi !== null) {
      endpoint += `&aqi=${aqi}`;
    }
    return await httpClient.get(endpoint, true);
  } catch (error) {
    console.error('Error fetching recommendation:', error);
    throw error;
  }
}

// Obtener historial de recomendaciones (requiere autenticación)
export async function getRecommendationHistory(skip = 0, limit = 100) {
  try {
    return await httpClient.get(`/recommendations/history?skip=${skip}&limit=${limit}`, true);
  } catch (error) {
    console.error('Error fetching recommendation history:', error);
    throw error;
  }
}

// Obtener todas las estaciones
export async function getStations(city = null, country = null, skip = 0, limit = 100) {
  try {
    let endpoint = `/stations?skip=${skip}&limit=${limit}`;
    if (city) endpoint += `&city=${encodeURIComponent(city)}`;
    if (country) endpoint += `&country=${encodeURIComponent(country)}`;

    return await httpClient.get(endpoint, false);
  } catch (error) {
    console.error('Error fetching stations:', error);
    throw error;
  }
}

// Obtener una estación específica
export async function getStation(stationId) {
  try {
    return await httpClient.get(`/stations/${stationId}`, false);
  } catch (error) {
    console.error('Error fetching station:', error);
    throw error;
  }
}

// Obtener lecturas actuales de una estación
export async function getStationCurrentReadings(stationId) {
  try {
    return await httpClient.get(`/stations/${stationId}/readings/current`, false);
  } catch (error) {
    console.error('Error fetching station readings:', error);
    throw error;
  }
}

// Obtener datos históricos de 7 días por estación
export async function getHistoricalData(stationId) {
  try {
    return await httpClient.get(`/air-quality/historical/7-days?station_id=${stationId}`, false);
  } catch (error) {
    console.error('Error fetching historical data:', error);
    throw error;
  }
}

// Health check del sistema
export async function healthCheck() {
  try {
    return await httpClient.get('/admin/health', false);
  } catch (error) {
    console.error('Error checking health:', error);
    throw error;
  }
}
