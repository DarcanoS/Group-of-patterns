# Architecture Overview - Ingestion Service

Documentación visual de la arquitectura del servicio de ingestion.

---

## 🏗️ Arquitectura General

```
┌─────────────────────────────────────────────────────────────────┐
│                     INGESTION SERVICE                            │
│                                                                  │
│  ┌────────────┐    ┌──────────────┐    ┌─────────────┐         │
│  │   CLI      │───▶│  Ingestion   │───▶│  Database   │         │
│  │  (main.py) │    │   Service    │    │  (Session)  │         │
│  └────────────┘    └──────┬───────┘    └─────────────┘         │
│                            │                                     │
│                    ┌───────┴────────┐                           │
│                    │                │                            │
│            ┌───────▼──────┐  ┌──────▼──────┐                   │
│            │   Adapters    │  │   Domain    │                   │
│            │  (Providers)  │  │   (DTOs)    │                   │
│            └───────────────┘  └─────────────┘                   │
└─────────────────────────────────────────────────────────────────┘
         │                              │
         │ reads                        │ normalizes
         ▼                              ▼
┌─────────────────┐          ┌─────────────────────┐
│  Data Sources   │          │  PostgreSQL + PostGIS│
│  - CSV files    │          │  - station           │
│  - AQICN API    │          │  - pollutant         │
│  - IoT sensors  │          │  - air_quality_reading│
└─────────────────┘          └─────────────────────┘
```

---

## 🔄 Flujo de Datos Completo

### Ingestion Histórica (CSV)

```
1. Inicio
   │
   ├─▶ main.py --mode historical
   │
   ▼
2. Carga Configuración
   │
   ├─▶ Lee station_mapping.yaml
   ├─▶ Carga .env (DATABASE_URL, etc.)
   │
   ▼
3. Crea Adapters
   │
   ├─▶ Para cada estación en mapping:
   │   └─▶ HistoricalCsvAdapter(csv_path, metadata)
   │
   ▼
4. Fetch Readings (por cada adapter)
   │
   ├─▶ Lee CSV con pandas
   ├─▶ Para cada fila:
   │   ├─▶ Normaliza timestamp → UTC
   │   ├─▶ Para cada pollutant:
   │   │   ├─▶ Estandariza nombre (pm25 → PM2.5)
   │   │   ├─▶ Valida rango (≥0, ≤ max_threshold)
   │   │   ├─▶ Estima AQI (si es PM2.5)
   │   │   └─▶ Crea NormalizedReading
   │   └─▶ Retorna List[NormalizedReading]
   │
   ▼
5. Persistencia (IngestionService)
   │
   ├─▶ Para cada reading:
   │   ├─▶ get_or_create_station()
   │   │   ├─▶ Busca en cache
   │   │   ├─▶ Si no existe, busca en DB
   │   │   └─▶ Si no existe, crea nueva Station
   │   │
   │   ├─▶ get_pollutant_id()
   │   │   ├─▶ Busca en cache
   │   │   └─▶ Si no existe, busca en DB
   │   │
   │   ├─▶ Verifica duplicado
   │   │   └─▶ Query: (station_id, pollutant_id, datetime)
   │   │
   │   └─▶ Si no es duplicado:
   │       └─▶ INSERT INTO air_quality_reading
   │
   ▼
6. Commit & Resultados
   │
   ├─▶ db.commit()
   ├─▶ Log estadísticas:
   │   ├─▶ Lecturas fetched: X
   │   ├─▶ Lecturas insertadas: Y
   │   └─▶ Lecturas omitidas: Z
   │
   └─▶ Exit 0
```

---

## 🎨 Adapter Pattern - Secuencia de Ejecución

```
┌──────┐                ┌─────────────┐              ┌──────────┐
│Client│                │IngestionSvc │              │ Adapter  │
│(main)│                │             │              │ (CSV)    │
└──┬───┘                └──────┬──────┘              └────┬─────┘
   │                           │                          │
   │ run_historical_ingestion()│                          │
   │──────────────────────────▶│                          │
   │                           │                          │
   │                           │ create_historical_adapters()
   │                           │──────────┐               │
   │                           │          │               │
   │                           │◀─────────┘               │
   │                           │                          │
   │                           │ fetch_readings()         │
   │                           │─────────────────────────▶│
   │                           │                          │
   │                           │                          │─┐
   │                           │                          │ │ read CSV
   │                           │                          │ │ parse rows
   │                           │                          │ │ normalize
   │                           │                          │ │ validate
   │                           │                          │◀┘
   │                           │                          │
   │                           │  List[NormalizedReading] │
   │                           │◀─────────────────────────│
   │                           │                          │
   │                           │─┐                        │
   │                           │ │ persist_readings()     │
   │                           │ │ - map to DB entities   │
   │                           │ │ - insert to PostgreSQL │
   │                           │◀┘                        │
   │                           │                          │
   │    stats (success)        │                          │
   │◀──────────────────────────│                          │
   │                           │                          │
```

---

## 📊 Transformación de Datos

### De CSV a Base de Datos

```
┌─────────────────────────────────────────────────────────────────┐
│ CSV File: carvajal,-bogota, colombia-air-quality.csv           │
├─────────────────────────────────────────────────────────────────┤
│ date,       pm25,  pm10,  o3,  no2,  so2,  co                  │
│ 2019/10/2,  116,   47,    9,   14,   1,    11                  │
└─────────────────────────────────────────────────────────────────┘
                           │
                           │ HistoricalCsvAdapter
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│ NormalizedReading (x6, uno por cada pollutant)                 │
├─────────────────────────────────────────────────────────────────┤
│ {                                                               │
│   external_station_id: "CARV-01",                              │
│   station_name: "Carvajal",                                    │
│   latitude: 4.614728,                                          │
│   longitude: -74.139465,                                       │
│   city: "Bogotá",                                              │
│   country: "Colombia",                                         │
│   pollutant_code: "PM2.5",      ← Estandarizado                │
│   unit: "µg/m³",                ← Estandarizado                │
│   value: 116.0,                                                │
│   aqi: 185,                     ← Calculado                    │
│   timestamp_utc: 2019-10-02T00:00:00+00:00  ← UTC             │
│ }                                                               │
│ ... (PM10, O3, NO2, SO2, CO)                                   │
└─────────────────────────────────────────────────────────────────┘
                           │
                           │ IngestionService
                           │ - get_or_create_station()
                           │ - get_pollutant_id()
                           │ - check duplicates
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│ PostgreSQL: air_quality_reading                                 │
├─────────────────────────────────────────────────────────────────┤
│ id | station_id | pollutant_id | datetime            | value...│
│ 1  | 3          | 1            | 2019-10-02 00:00:00 | 116.0...│
│ 2  | 3          | 2            | 2019-10-02 00:00:00 | 47.0 ...│
│ 3  | 3          | 3            | 2019-10-02 00:00:00 | 9.0  ...│
│ ...                                                             │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🗄️ Modelo de Datos

### Relaciones entre Entidades

```
┌─────────────┐
│ map_region  │
│             │
│ id (PK)     │
│ name        │
│ geom        │
└──────┬──────┘
       │
       │ 1:N
       │
┌──────▼──────────┐
│ station         │
│                 │
│ id (PK)         │
│ name            │◀───────────────────┐
│ latitude        │                    │
│ longitude       │                    │
│ city            │                    │
│ country         │                    │
│ region_id (FK)  │                    │
└──────┬──────────┘                    │
       │                               │
       │ 1:N                           │
       │                               │
┌──────▼─────────────────┐             │
│ air_quality_reading    │             │
│                        │             │
│ id (PK)                │             │
│ station_id (FK)  ──────┘             │
│ pollutant_id (FK) ───────┐           │
│ datetime               │ │           │
│ value                  │ │           │
│ aqi                    │ │           │
└────────────────────────┘ │           │
                           │           │
                      ┌────▼────┐      │
                      │pollutant│      │
                      │         │      │
                      │ id (PK) │      │
                      │ name    │      │
                      │ unit    │      │
                      └─────────┘      │
                                       │
┌──────────────────────┐               │
│ NormalizedReading    │               │
│ (DTO - in memory)    │───maps to────┘
│                      │
│ external_station_id  │
│ pollutant_code       │
│ value                │
│ timestamp_utc        │
└──────────────────────┘
```

---

## 📂 Estructura de Archivos Anotada

```
ingestion/
│
├── 📄 .env.example              # Template de configuración
├── 📄 requirements.txt          # Dependencias Python
├── 📄 Dockerfile                # Containerización
├── 📘 README.md                 # Documentación de uso
├── 📘 DESIGN_PATTERNS.md        # Este documento
│
├── 📂 app/                      # Código fuente
│   │
│   ├── 🚀 main.py               # Entry point - CLI
│   ├── ⚙️  config.py            # Settings (Pydantic)
│   ├── 📝 logging_config.py     # Logging setup
│   │
│   ├── 📂 db/                   # Capa de Base de Datos
│   │   ├── session.py           # ✓ SQLAlchemy engine/session
│   │   └── models.py            # ✓ ORM models (Station, Pollutant, Reading)
│   │
│   ├── 📂 domain/               # Lógica de Dominio
│   │   ├── dto.py               # ✓ Pydantic DTOs (NormalizedReading)
│   │   └── normalization.py    # ✓ Conversión, validación, AQI
│   │
│   ├── 📂 providers/            # 🎨 ADAPTER PATTERN
│   │   ├── base_adapter.py            # ✓ Interface abstracta
│   │   ├── historical_csv_adapter.py  # ✓ CSV implementation
│   │   └── aqicn_adapter.py           # 📋 Futuro: API AQICN
│   │
│   └── 📂 services/             # Orquestación
│       ├── ingestion_service.py       # ✓ Main orchestrator
│       └── aggregation_service.py     # 📋 Futuro: Daily stats
│
└── 📂 data/                     # Configuración
    └── station_mapping.yaml     # Mapeo CSV → Station metadata
```

**Leyenda**:
- ✓ = Implementado
- 📋 = Pendiente/Futuro
- 🎨 = Patrón de diseño

---

## 🔀 Casos de Uso

### Caso 1: Ingestion Histórica Inicial

**Escenario**: Primera vez ejecutando el servicio, base de datos vacía.

```
Entrada:
- 5 archivos CSV (~1,700 filas cada uno)
- station_mapping.yaml con 5 estaciones
- Base de datos con tabla pollutant poblada

Proceso:
1. Crea 5 HistoricalCsvAdapters
2. Por cada adapter:
   - Lee CSV (1,700 rows)
   - Genera ~10,200 NormalizedReadings (1,700 × 6 pollutants)
3. Ingestion Service:
   - Crea 5 Stations nuevas
   - Inserta ~51,000 air_quality_readings (10,200 × 5 stations)

Resultado:
✓ 5 stations creadas
✓ 51,000 readings insertadas
✓ 0 duplicados
⏱️ Tiempo estimado: 2-5 minutos
```

### Caso 2: Re-ingestion (con duplicados)

**Escenario**: Re-ejecutar el servicio con datos ya ingresados.

```
Entrada:
- Mismos 5 CSV
- Base de datos ya tiene las 51,000 readings

Proceso:
1. Crea adapters
2. Fetch readings (mismo proceso)
3. Ingestion Service:
   - Encuentra 5 stations existentes (usa cache)
   - Detecta 51,000 duplicados
   - Omite todas las inserciones

Resultado:
✓ 0 stations creadas
✓ 0 readings insertadas
✓ 51,000 duplicados detectados
⏱️ Tiempo: ~30 segundos (más rápido, solo queries)
```

### Caso 3: Agregar Nueva Estación

**Escenario**: Se agrega un nuevo CSV con datos de una estación adicional.

```
Entrada:
- Nuevo CSV: kennedy-bogota.csv
- station_mapping.yaml actualizado con nueva estación

Proceso:
1. Crea 6 adapters (5 existentes + 1 nueva)
2. Adapters existentes:
   - Detectan duplicados, skip
3. Nuevo adapter:
   - Genera ~10,200 readings
   - Crea Station "Kennedy"
   - Inserta 10,200 readings nuevas

Resultado:
✓ 1 station creada (Kennedy)
✓ 10,200 readings insertadas
✓ 51,000 duplicados omitidos
⏱️ Tiempo: ~1 minuto
```

---

## 🧩 Extensibilidad

### Agregar Adapter para AQICN API

**Paso 1**: Implementar adapter

```python
# app/providers/aqicn_adapter.py

from app.providers.base_adapter import BaseExternalApiAdapter
import httpx

class AqicnAdapter(BaseExternalApiAdapter):
    """Adapter para AQICN JSON API"""
    
    def __init__(self, token: str, city: str):
        self.token = token
        self.city = city
        self.base_url = "https://api.waqi.info"
    
    def fetch_readings(self) -> List[NormalizedReading]:
        # 1. Call API
        response = httpx.get(
            f"{self.base_url}/feed/{self.city}/",
            params={"token": self.token}
        )
        data = response.json()
        
        # 2. Parse response
        readings = []
        for pollutant, value in data['data']['iaqi'].items():
            reading = NormalizedReading(
                external_station_id=f"aqicn-{data['data']['idx']}",
                station_name=data['data']['city']['name'],
                latitude=data['data']['city']['geo'][0],
                longitude=data['data']['city']['geo'][1],
                pollutant_code=standardize_pollutant_name(pollutant),
                unit=get_standard_unit(pollutant),
                value=value['v'],
                timestamp_utc=datetime.now(timezone.utc),
                aqi=data['data']['aqi']
            )
            readings.append(reading)
        
        return readings
```

**Paso 2**: Usar en servicio (sin cambios en código existente)

```python
# app/services/ingestion_service.py

def create_realtime_adapters(self) -> List[BaseExternalApiAdapter]:
    adapters = []
    
    for city in settings.ingestion_default_cities:
        adapter = AqicnAdapter(
            token=settings.aqicn_token,
            city=city
        )
        adapters.append(adapter)
    
    return adapters

def run_realtime_ingestion(self):
    adapters = self.create_realtime_adapters()  # Nueva fuente
    
    for adapter in adapters:
        readings = adapter.fetch_readings()  # ✓ Misma interfaz
        self._persist_readings(readings)      # ✓ Misma lógica
```

**Resultado**: Sin modificar `_persist_readings()` ni `main.py`, ahora soportamos API en tiempo real.

---

## 🎯 Testing Strategy

### Unit Tests

```python
# tests/test_csv_adapter.py

def test_csv_adapter_implements_interface():
    """Verifica que implementa BaseExternalApiAdapter"""
    adapter = HistoricalCsvAdapter(...)
    assert isinstance(adapter, BaseExternalApiAdapter)
    assert hasattr(adapter, 'fetch_readings')

def test_csv_adapter_normalizes_timestamps():
    """Verifica conversión a UTC"""
    adapter = HistoricalCsvAdapter(...)
    readings = adapter.fetch_readings()
    
    for reading in readings:
        assert reading.timestamp_utc.tzinfo == timezone.utc

def test_csv_adapter_validates_values():
    """Verifica que omite valores inválidos"""
    # CSV con valor negativo
    adapter = HistoricalCsvAdapter(csv_with_invalid_data)
    readings = adapter.fetch_readings()
    
    # No debe haber valores negativos
    assert all(r.value >= 0 for r in readings)
```

### Integration Tests

```python
# tests/test_ingestion_service.py

def test_full_ingestion_pipeline(db_session):
    """Test end-to-end"""
    service = IngestionService(db_session)
    
    # Mock adapter
    mock_adapter = MockCsvAdapter(test_csv)
    
    # Run ingestion
    stats = service.run_historical_ingestion()
    
    # Verify database
    assert db_session.query(Station).count() > 0
    assert db_session.query(AirQualityReading).count() > 0
    assert stats['readings_inserted'] > 0
```

---

## 📈 Performance Considerations

### Optimizaciones Implementadas

1. **Caching**
   ```python
   self.station_cache: Dict[str, int] = {}
   self.pollutant_cache: Dict[str, int] = {}
   ```
   - Evita queries repetidas
   - ~80% reducción en queries de lookup

2. **Bulk Processing**
   ```python
   for reading in readings:
       db.add(reading)
   db.flush()  # Una vez al final
   ```
   - Batch inserts
   - Reduce roundtrips a DB

3. **Duplicate Detection**
   ```python
   existing = db.query(...).filter(
       station_id == x,
       pollutant_id == y,
       datetime == z
   ).first()
   ```
   - Evita constraint violations
   - Permite re-runs seguros

### Métricas Esperadas

| Operación | Tiempo | Throughput |
|-----------|--------|------------|
| Fetch 1 CSV (1,700 rows) | ~2s | 850 rows/s |
| Normalize 10,200 readings | ~3s | 3,400 readings/s |
| Insert 10,200 readings (new) | ~15s | 680 inserts/s |
| Insert 10,200 readings (duplicates) | ~5s | 2,040 checks/s |
| **Total (5 stations, initial)** | **~2-5 min** | **~400 readings/s** |

---

## 🚀 Deployment

### Docker Compose Example

```yaml
version: '3.8'

services:
  ingestion-historical:
    build: ./ingestion
    environment:
      DATABASE_URL: postgresql://user:pass@postgres:5432/air_quality_db
      INGESTION_MODE: historical
    volumes:
      - ../data_air:/data_air:ro
    depends_on:
      - postgres
    command: ["python", "-m", "app.main", "--mode", "historical"]
  
  ingestion-realtime:
    build: ./ingestion
    environment:
      DATABASE_URL: postgresql://user:pass@postgres:5432/air_quality_db
      AQICN_TOKEN: ${AQICN_TOKEN}
      INGESTION_INTERVAL_MINUTES: 10
    depends_on:
      - postgres
    command: ["python", "-m", "app.main", "--mode", "realtime"]
```

---

## 📚 Conclusión

El servicio de ingestion implementa una arquitectura limpia, extensible y mantenible gracias a:

✅ **Adapter Pattern**: Unifica múltiples fuentes de datos  
✅ **DTOs con Pydantic**: Type safety y validación  
✅ **Arquitectura en capas**: Separación de responsabilidades  
✅ **SOLID principles**: Código extensible sin modificaciones  
✅ **Testing-friendly**: Componentes desacoplados

**Próximos pasos**:
1. Implementar `AqicnAdapter` para tiempo real
2. Agregar tests automatizados
3. Implementar `AggregationService` para stats diarias
4. Agregar observabilidad (metrics, tracing)

---

**Última actualización**: 26 de noviembre de 2025
