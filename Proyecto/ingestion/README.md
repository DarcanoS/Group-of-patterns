# Air Quality Platform - Ingestion Service

Servicio de ingestion de datos para la plataforma Air Quality Platform.

## 📋 Descripción

Este servicio implementa:

1. **Ingestion Histórica** (one-time, repeatable):
   - Lee datos de archivos CSV históricos
   - Lee metadata de estaciones desde archivos GeoJSON
   - Normaliza y valida los datos
   - Inserta en PostgreSQL

2. **Ingestion en Tiempo Real** (futuro):
   - Consume API de AQICN
   - Ejecución periódica configurable
   - (Pendiente de implementación)

## 🎨 Patrones de Diseño

### Adapter Pattern ⭐

El patrón **Adapter** está implementado en `app/providers/`:

- **`BaseExternalApiAdapter`**: Interfaz base para adaptadores
- **`HistoricalCsvAdapter`**: Adapta archivos CSV al formato común
- **`AqicnAdapter`**: (Futuro) Adapta API de AQICN

Esto permite:
- Unificar diferentes fuentes de datos (CSV, APIs)
- Desacoplar la lógica de ingestion de las fuentes específicas
- Facilitar la adición de nuevas fuentes sin modificar el core

**📚 Documentación Completa**:
- **[DESIGN_PATTERNS.md](./DESIGN_PATTERNS.md)**: Teoría, ejemplos de código, referencias
- **[ARCHITECTURE.md](./ARCHITECTURE.md)**: Diagramas visuales, flujos de datos, casos de uso

## 📁 Estructura

```
ingestion/
├── app/
│   ├── config.py              # Configuración (env vars)
│   ├── logging_config.py      # Logging setup
│   ├── main.py                # Entry point
│   │
│   ├── db/
│   │   ├── session.py         # DB connection
│   │   └── models.py          # ORM models
│   │
│   ├── domain/
│   │   ├── dto.py             # Pydantic DTOs
│   │   └── normalization.py  # Data normalization
│   │
│   ├── providers/
│   │   ├── base_adapter.py           # Adapter pattern base
│   │   └── historical_csv_adapter.py # CSV adapter
│   │
│   └── services/
│       └── ingestion_service.py      # Orchestration
│
├── data/
│   └── station_mapping.yaml   # Mapeo CSV → Station metadata
│
├── requirements.txt
├── Dockerfile
└── .env.example
```

## ⚙️ Configuración

### 1. Variables de Entorno

Copia `.env.example` a `.env` y configura:

```bash
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/air_quality_db

# Paths
HISTORICAL_DATA_PATH=../data_air
STATION_MAPPING_PATH=data/station_mapping.yaml

# Logging
INGESTION_LOG_LEVEL=INFO
```

### 2. Station Mapping

Edita `data/station_mapping.yaml` para mapear archivos CSV a estaciones:

```yaml
stations:
  - csv_file: "carvajal,-bogota, colombia-air-quality.csv"
    station_name: "Carvajal"
    latitude: 4.614728
    longitude: -74.139465
    city: "Bogotá"
    country: "Colombia"
```

## 🚀 Uso

### Instalación Local

```bash
# Instalar dependencias
pip install -r requirements.txt

# Configurar .env
cp .env.example .env
# Editar .env con tus credenciales

# Ejecutar ingestion histórica
python -m app.main --mode historical

# Ver ayuda
python -m app.main --help
```

### Docker

```bash
# Build image
docker build -t air-quality-ingestion .

# Run historical ingestion
docker run --rm \
  --env-file .env \
  -v $(pwd)/../data_air:/data_air \
  air-quality-ingestion
```

## 📊 Datos de Entrada

### CSV Files (`data_air/`)

Formato esperado:

```csv
date, pm25, pm10, o3, no2, so2, co
2019/10/2, 116, 47, 9, 14, 1, 11
2019/10/3, 115, 38, 3, 12, 1, 12
```

- **Columnas**: date, pm25, pm10, o3, no2, so2, co
- **Fechas**: formato `YYYY/M/D`
- **Valores vacíos**: se omiten (missing data)

### GeoJSON Files

Metadata de estaciones en formato GeoJSON:

```json
{
  "type": "FeatureCollection",
  "features": [{
    "properties": {
      "estacion": "Centro de Alto Rendimiento",
      "codestac": "5",
      "altura": 2577
    }
  }]
}
```

## 🔧 Desarrollo

### Agregar Nueva Fuente de Datos

1. Crear nuevo adapter en `app/providers/`:

```python
from app.providers.base_adapter import BaseExternalApiAdapter

class MyNewAdapter(BaseExternalApiAdapter):
    def fetch_readings(self) -> List[NormalizedReading]:
        # Implementar lógica
        pass
```

2. Registrar en el servicio de ingestion

3. Configurar en `.env` si es necesario

### Tests

```bash
# Ejecutar tests (cuando estén implementados)
pytest

# Test con log detallado
python -m app.main --mode historical --log-level DEBUG
```

## 📝 Notas de Implementación

### Normalización de Datos

- **Timestamps**: Convertidos a UTC
- **Pollutants**: Nombres estandarizados (PM2.5, PM10, O3, etc.)
- **Units**: µg/m³ para PM, ppb para gases, ppm para CO
- **AQI**: Estimado usando fórmula simplificada EPA (solo PM2.5 por ahora)

### Manejo de Duplicados

El servicio detecta y omite lecturas duplicadas basándose en:
- `station_id`
- `pollutant_id`
- `datetime`

Esto permite re-ejecutar la ingestion histórica de forma segura.

### Base de Datos

Requiere que las tablas ya estén creadas:
- `station`
- `pollutant` (con datos seed)
- `air_quality_reading`

El servicio **no** crea tablas ni datos de catálogo.

## 🔮 Trabajo Futuro

- [ ] Implementar `AqicnAdapter` para API en tiempo real
- [ ] Agregar scheduler para ingestion periódica
- [ ] Implementar `AggregationService` para stats diarias
- [ ] Agregar tests unitarios
- [ ] Mejorar cálculo de AQI (más pollutants)
- [ ] Validación de coordenadas GeoJSON

## 📚 Referencias

- [AQICN API Documentation](https://aqicn.org/api/)
- [EPA AQI Calculator](https://www.airnow.gov/aqi/aqi-calculator/)
- [Adapter Pattern](https://refactoring.guru/design-patterns/adapter)
