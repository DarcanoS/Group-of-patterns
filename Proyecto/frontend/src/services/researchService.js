// src/services/researchService.js
// Mock service for researcher dashboard (replace with real API calls later)

export async function fetchDailyStats({ city, station, pollutant, startDate, endDate }) {
  // Simulate network latency
  await new Promise((r) => setTimeout(r, 300));

  // Mock days between start and end (if provided) — otherwise 14 days
  const labels = ["2025-11-14","2025-11-15","2025-11-16","2025-11-17","2025-11-18","2025-11-19","2025-11-20","2025-11-21","2025-11-22","2025-11-23","2025-11-24","2025-11-25","2025-11-26","2025-11-27"];
  // Mock values (random-ish but deterministic for demo)
  const values = labels.map((d, i) => Math.round(40 + 30 * Math.abs(Math.sin(i * 0.6)) + (i % 3) * 5));

  // Also return tabular (per-day) records
  const records = labels.map((label, i) => ({
    date: label,
    city: city || "Bogotá",
    station: station || "Station Centro",
    pollutant: pollutant || "PM2.5",
    avg_aqi: values[i]
  }));

  return {
    labels,
    values,
    records
  };
}
