# Air Quality Platform - Ingestion Service

Servicio de ingestion de datos para la plataforma Air Quality Platform.

## 📋 Descripción

Este servicio implementa:

1. **Ingestion Histórica** (one-time, repeatable):
   - Lee datos de archivos CSV históricos
   - Lee metadata de estaciones desde archivos GeoJSON
   - Normaliza y valida los datos
   - Inserta en PostgreSQL

2. **Ingestion en Tiempo Real** ✅ **IMPLEMENTADO**:
   - Consume API de AQICN (World Air Quality Index)
   - Datos actualizados de calidad del aire
   - Ejecución bajo demanda o periódica

## 🎨 Patrones de Diseño

### Adapter Pattern ⭐

El patrón **Adapter** está implementado en `app/providers/`:

- **`BaseExternalApiAdapter`**: Interfaz base para adaptadores
- **`HistoricalCsvAdapter`**: Adapta archivos CSV al formato común
- **`AqicnAdapter`**: ✅ Implementado - Adapta API de AQICN en tiempo real

Esto permite:
- Unificar diferentes fuentes de datos (CSV, APIs)
- Desacoplar la lógica de ingestion de las fuentes específicas
- Facilitar la adición de nuevas fuentes sin modificar el core

**📚 Documentación Completa**:
- **[docs/DESIGN_PATTERNS.md](./docs/DESIGN_PATTERNS.md)**: Teoría, ejemplos de código, referencias
- **[docs/ARCHITECTURE.md](./docs/ARCHITECTURE.md)**: Diagramas visuales, flujos de datos, casos de uso

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
│   │   ├── base_adapter.py              # Adapter pattern base
│   │   ├── historical_csv_adapter.py    # CSV adapter
│   │   └── aqicn_adapter.py             # ✅ AQICN API adapter
│   │
│   └── services/
│       └── ingestion_service.py         # Orchestration
│
├── data/
│   └── station_mapping.yaml   # Mapeo CSV → Station metadata
│
├── docs/                      # 📚 Documentación técnica
│   ├── ARCHITECTURE.md        # Arquitectura y diagramas
│   ├── DESIGN_PATTERNS.md     # Patrones de diseño
│   ├── API_AQICN.md          # Especificación API AQICN
│   ├── AQICN_USAGE.md        # Guía de uso ingestion tiempo real
│   └── DOCS_INDEX.md         # Índice de documentación
│
├── tests/                     # 🧪 Tests
│   ├── test_aqicn_api.py     # Tests de API AQICN
│   └── test_aqicn_ingestion.py # Tests de ingestion completa
│
├── requirements.txt
├── Dockerfile
├── .env.example
└── README.md                  # ← Este archivo
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

# Ejecutar ingestion histórica (CSV)
python -m app.main --mode historical

# Ejecutar ingestion en tiempo real (AQICN API)
python -m app.main --mode realtime

# Ver ayuda
python -m app.main --help
```

### Tests

```bash
# Test de conectividad con API AQICN
python tests/test_aqicn_api.py

# Test de ingestion completa (incluye BD)
python tests/test_aqicn_ingestion.py
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

## 🚀 Deployment en Servidor Ubuntu

Para desplegar este servicio en un servidor Ubuntu con ingestion automática (cada 10 minutos), consulta la **[Guía de Deployment](./README_DEPLOYMENT.md)**.

### Deployment Rápido

```bash
# 1. Clonar repositorio en el servidor
git clone https://github.com/your-org/air-quality-platform.git
cd air-quality-platform/Proyecto/ingestion

# 2. Ejecutar script de deployment
chmod +x deploy/deploy.sh
./deploy/deploy.sh

# 3. Configurar .env
sudo nano /opt/air-quality-ingestion/.env

# 4. Verificar instalación
./deploy/health_check.sh
```

**Opciones de automatización**:
- **Systemd Timer** (recomendado): Integrado con sistema, logs centralizados
- **Cron Job**: Más simple, compatible con cualquier Linux

**Ubicaciones en producción**:
- Aplicación: `/opt/air-quality-ingestion/`
- Logs: `/var/log/air-quality-ingestion/`
- Scripts: `deploy/`

📖 **[Ver Guía Completa de Deployment →](./README_DEPLOYMENT.md)**

---

## 🔮 Trabajo Futuro

- [x] ~~Implementar `AqicnAdapter` para API en tiempo real~~ ✅ **COMPLETADO**
- [x] ~~Agregar scheduler para ingestion periódica~~ ✅ **COMPLETADO** (systemd/cron)
- [ ] Implementar `AggregationService` para stats diarias
- [ ] Agregar más tests unitarios
- [ ] Mejorar cálculo de AQI (más pollutants)
- [ ] Validación de coordenadas GeoJSON

## 📚 Documentación Adicional

Para más detalles, consulta:

- **[docs/DOCS_INDEX.md](./docs/DOCS_INDEX.md)** - Índice completo de documentación
- **[docs/ARCHITECTURE.md](./docs/ARCHITECTURE.md)** - Arquitectura y diagramas
- **[docs/DESIGN_PATTERNS.md](./docs/DESIGN_PATTERNS.md)** - Patrones de diseño implementados
- **[docs/AQICN_USAGE.md](./docs/AQICN_USAGE.md)** - Guía de uso de ingestion en tiempo real
- **[docs/API_AQICN.md](./docs/API_AQICN.md)** - Especificación del cliente AQICN
- **[README_DEPLOYMENT.md](./README_DEPLOYMENT.md)** - 🚀 Guía completa de deployment en Ubuntu
