import httpClient from './httpClient';

// Obtener estadísticas diarias con filtros
export async function fetchDailyStats({ city, station, pollutant, startDate, endDate }) {
  try {
    // Primero obtener la estación si se proporciona ciudad
    let stationId = null;
    if (city && !station) {
      const stations = await httpClient.get(`/stations?city=${encodeURIComponent(city)}&limit=1`, false);
      if (stations && stations.length > 0) {
        stationId = stations[0].id;
      }
    } else if (station) {
      stationId = station;
    }

    // Construir query para estadísticas diarias
    let endpoint = '/air-quality/daily-stats?limit=365';
    if (stationId) endpoint += `&station_id=${stationId}`;
    if (pollutant) endpoint += `&pollutant_id=${pollutant}`;
    if (startDate) endpoint += `&start_date=${startDate}`;
    if (endDate) endpoint += `&end_date=${endDate}`;

    const dailyStats = await httpClient.get(endpoint, false);

    // Transformar datos para el formato esperado por el frontend
    const labels = dailyStats.map(stat => stat.date);
    const values = dailyStats.map(stat => Math.round(stat.avg_aqi));

    // Crear registros tabulares
    const records = dailyStats.map(stat => ({
      date: stat.date,
      city: city || 'N/A',
      station: station || `Station ${stat.station_id}`,
      pollutant: pollutant || `Pollutant ${stat.pollutant_id}`,
      avg_aqi: Math.round(stat.avg_aqi),
      max_value: stat.max_value,
      min_value: stat.min_value,
      readings_count: stat.readings_count
    }));

    return {
      labels,
      values,
      records
    };
  } catch (error) {
    console.error('Error fetching daily stats:', error);
    throw error;
  }
}

// Obtener lista de contaminantes disponibles
export async function getPollutants() {
  try {
    // Este endpoint puede que necesite ser agregado al backend
    // Por ahora retornamos una estructura básica
    return [
      { id: 1, name: 'PM2.5', unit: 'µg/m³' },
      { id: 2, name: 'PM10', unit: 'µg/m³' },
      { id: 3, name: 'O3', unit: 'ppb' },
      { id: 4, name: 'NO2', unit: 'ppb' },
      { id: 5, name: 'SO2', unit: 'ppb' },
      { id: 6, name: 'CO', unit: 'ppm' }
    ];
  } catch (error) {
    console.error('Error fetching pollutants:', error);
    throw error;
  }
}

// Obtener estadísticas agregadas por estación
export async function getStationStats(stationId, startDate, endDate) {
  try {
    let endpoint = `/air-quality/daily-stats?station_id=${stationId}&limit=365`;
    if (startDate) endpoint += `&start_date=${startDate}`;
    if (endDate) endpoint += `&end_date=${endDate}`;

    return await httpClient.get(endpoint, false);
  } catch (error) {
    console.error('Error fetching station stats:', error);
    throw error;
  }
}
