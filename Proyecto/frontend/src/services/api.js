export async function getAirQuality() {
  return {
    city: "Bogotá",
    level: "moderado",
    aqi: 72,
    status: "Aceptable",
    updatedAt: new Date().toLocaleString(),

    history: [42, 55, 61, 70, 66, 73, 72],

    stations: [
      { name: "Chapinero", aqi: 68 },
      { name: "Kennedy", aqi: 81 },
      { name: "Suba", aqi: 59 }
    ],

    products: [
      { name: "N95 Mascara", description: "filtro de alta eficiencia " },
      { name: "purificador aire", description: "limpiador de interiores" },
      { name: "spray nasal", description: "Reduce irritacion" }
    ]
  };
}
