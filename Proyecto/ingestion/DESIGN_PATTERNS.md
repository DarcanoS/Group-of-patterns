# Design Patterns - Ingestion Service

Este documento describe los patrones de diseño implementados en el servicio de ingestion de Air Quality Platform.

---

## 📐 Patrones Implementados

### 1. Adapter Pattern (Patrón Adaptador)

**Ubicación**: `app/providers/`

**Propósito**: Convertir la interfaz de diferentes fuentes de datos (archivos CSV, APIs externas) en una interfaz común que el servicio de ingestion pueda consumir de manera uniforme.

#### Estructura

```
app/providers/
├── base_adapter.py              # Interface abstracta
├── historical_csv_adapter.py    # Adapter concreto para CSV
└── aqicn_adapter.py             # (Futuro) Adapter para AQICN API
```

#### Componentes

**1. Base Adapter (Interface)**

```python
# app/providers/base_adapter.py

class BaseExternalApiAdapter(ABC):
    """
    Adapter Pattern Implementation
    
    Interfaz base que define el contrato común para todos los adaptadores
    de fuentes de datos externas.
    """
    
    @abstractmethod
    def fetch_readings(self) -> List[NormalizedReading]:
        """
        Obtiene y normaliza lecturas desde la fuente de datos específica.
        
        Returns:
            Lista de objetos NormalizedReading
        """
        pass
```

**2. Concrete Adapter - CSV**

```python
# app/providers/historical_csv_adapter.py

class HistoricalCsvAdapter(BaseExternalApiAdapter):
    """
    Adapter Pattern: CSV File Source
    
    Adapta archivos CSV históricos al formato común NormalizedReading.
    """
    
    def __init__(
        self,
        csv_file_path: Path,
        station_metadata: StationMetadata,
        pollutant_mapping: Dict[str, Dict[str, str]]
    ):
        # Configuración específica para CSV
        ...
    
    def fetch_readings(self) -> List[NormalizedReading]:
        # Lógica específica para leer CSV
        # 1. Lee archivo CSV con pandas
        # 2. Procesa cada fila
        # 3. Normaliza timestamps, pollutants, unidades
        # 4. Valida valores
        # 5. Estima AQI
        # 6. Retorna lista de NormalizedReading
        ...
```

**3. Target Format (DTO común)**

```python
# app/domain/dto.py

class NormalizedReading(BaseModel):
    """
    Formato común de salida para todos los adapters.
    
    Independiente de la fuente de datos original.
    """
    external_station_id: str
    station_name: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float]
    city: Optional[str]
    country: Optional[str]
    pollutant_code: str
    unit: str
    value: float
    aqi: Optional[int]
    timestamp_utc: datetime
```

#### Diagrama de Clases

```
┌─────────────────────────────────────┐
│   BaseExternalApiAdapter (ABC)     │
│                                     │
│  + fetch_readings()                 │
│    → List[NormalizedReading]        │
└──────────────┬──────────────────────┘
               │
               │ implements
    ┌──────────┴──────────┐
    │                     │
┌───▼──────────────┐  ┌──▼─────────────────┐
│ HistoricalCSV    │  │  AqicnAdapter      │
│ Adapter          │  │  (futuro)          │
│                  │  │                    │
│ - csv_file_path  │  │ - api_token        │
│ - station_meta   │  │ - base_url         │
│                  │  │                    │
│ + fetch_readings │  │ + fetch_readings   │
└──────────────────┘  └────────────────────┘
         │                      │
         │ produces             │ produces
         └──────────┬───────────┘
                    │
            ┌───────▼───────┐
            │ Normalized    │
            │ Reading       │
            │ (DTO)         │
            └───────────────┘
```

#### Ventajas del Patrón

1. **Desacoplamiento**: El servicio de ingestion no necesita conocer los detalles de cada fuente de datos.

2. **Extensibilidad**: Agregar una nueva fuente de datos solo requiere:
   - Crear un nuevo adapter que implemente `BaseExternalApiAdapter`
   - No modificar el código existente (Open/Closed Principle)

3. **Uniformidad**: Todas las fuentes producen el mismo formato de salida (`NormalizedReading`).

4. **Testabilidad**: Cada adapter puede testearse de forma independiente.

#### Ejemplo de Uso

```python
# En app/services/ingestion_service.py

class IngestionService:
    def create_historical_adapters(self) -> List[BaseExternalApiAdapter]:
        adapters = []
        
        # Crear adapters CSV para cada estación
        for station_config in config['stations']:
            adapter = HistoricalCsvAdapter(
                csv_file_path=Path(station_config['csv_file']),
                station_metadata=StationMetadata(**station_config),
                pollutant_mapping=config['pollutant_mapping']
            )
            adapters.append(adapter)
        
        return adapters
    
    def run_historical_ingestion(self):
        # El servicio trabaja con la interfaz abstracta
        adapters = self.create_historical_adapters()
        
        for adapter in adapters:
            # Mismo código funciona para cualquier adapter
            readings = adapter.fetch_readings()
            self._persist_readings(readings)
```

#### Caso Real de Uso

**Problema Original**: 
- Datos históricos en CSV con formato específico
- Futuras fuentes: API AQICN, sensores IoT, otras APIs públicas
- Cada fuente tiene formato, unidades y nombres diferentes

**Solución con Adapter**:
```python
# CSV Adapter
csv_adapter = HistoricalCsvAdapter(...)
readings_csv = csv_adapter.fetch_readings()  # → List[NormalizedReading]

# API Adapter (futuro)
api_adapter = AqicnAdapter(token="...")
readings_api = api_adapter.fetch_readings()  # → List[NormalizedReading]

# El servicio procesa ambos de la misma forma
for reading in readings_csv + readings_api:
    persist_to_database(reading)
```

---

## 🔄 Patrones Relacionados

### Repository Pattern (Implícito)

Aunque no está explícitamente nombrado, el servicio de ingestion implementa el patrón Repository al separar la lógica de acceso a datos:

```python
# app/services/ingestion_service.py

class IngestionService:
    """Actúa como un Repository para operaciones de ingestion"""
    
    def _get_or_create_station(self, reading: NormalizedReading) -> int:
        """Abstrae la lógica de acceso a Station"""
        ...
    
    def _get_pollutant_id(self, pollutant_code: str) -> Optional[int]:
        """Abstrae la lógica de acceso a Pollutant"""
        ...
    
    def _persist_readings(self, readings: List[NormalizedReading]):
        """Abstrae la persistencia de readings"""
        ...
```

**Beneficios**:
- Lógica de BD centralizada
- Fácil testing con mocks
- Cache interno para performance

### Strategy Pattern (Implícito en Normalización)

La normalización de datos usa diferentes estrategias según el tipo de pollutant:

```python
# app/domain/normalization.py

def estimate_aqi(pollutant_code: str, value: float) -> Optional[int]:
    """
    Strategy Pattern implícito: diferentes algoritmos según pollutant
    """
    if pollutant_code == "PM2.5":
        return calculate_aqi_pm25(value)
    elif pollutant_code == "PM10":
        return calculate_aqi_pm10(value)  # (futuro)
    # ... otras estrategias
```

---

## 📊 Data Transfer Object (DTO) Pattern

**Ubicación**: `app/domain/dto.py`

El servicio usa DTOs (Pydantic models) para transferir datos entre capas:

```python
class NormalizedReading(BaseModel):
    """
    DTO para lecturas normalizadas.
    
    Ventajas:
    - Validación automática (Pydantic)
    - Type safety
    - Serialización/Deserialización
    - Documentación clara
    """
    pollutant_code: str = Field(...)
    value: float = Field(ge=0)  # Validación: >= 0
    timestamp_utc: datetime
    
    @field_validator('pollutant_code')
    @classmethod
    def normalize_pollutant_code(cls, v: str) -> str:
        return v.strip().upper()
```

**Separación de capas**:
```
CSV Row → NormalizedReading (DTO) → AirQualityReading (ORM)
  ↑                  ↑                        ↑
Fuente         Domain Layer              Database Layer
```

---

## 🏗️ Arquitectura en Capas

El servicio sigue una arquitectura limpia por capas:

```
┌─────────────────────────────────────────┐
│         Presentation Layer              │
│         (app/main.py - CLI)             │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│         Service Layer                   │
│    (app/services/ingestion_service.py)  │
│    - Orchestration                      │
│    - Business logic                     │
└──────────────┬──────────────────────────┘
               │
    ┌──────────┼──────────┐
    │          │          │
┌───▼────┐ ┌──▼──────┐ ┌▼───────────┐
│Providers│ │ Domain  │ │ DB Layer   │
│(Adapters)│ │ (DTOs,  │ │ (Models,   │
│          │ │  Norm.) │ │  Session)  │
└──────────┘ └─────────┘ └────────────┘
```

**Ventajas**:
- Cada capa tiene responsabilidades claras
- Fácil testing individual
- Cambios en una capa no afectan otras

---

## 🎯 Principios SOLID Aplicados

### Single Responsibility Principle (SRP)
- `HistoricalCsvAdapter`: Solo lee y normaliza CSV
- `IngestionService`: Solo orquesta la ingestion
- `normalization.py`: Solo normaliza datos

### Open/Closed Principle (OCP)
- Agregar nuevo adapter no requiere modificar código existente
- Solo extender `BaseExternalApiAdapter`

### Liskov Substitution Principle (LSP)
- Cualquier `BaseExternalApiAdapter` puede usarse donde se espera la interfaz base
- `HistoricalCsvAdapter` y `AqicnAdapter` son intercambiables

### Interface Segregation Principle (ISP)
- `BaseExternalApiAdapter` define solo el método necesario: `fetch_readings()`
- No fuerza implementaciones innecesarias

### Dependency Inversion Principle (DIP)
- `IngestionService` depende de la abstracción `BaseExternalApiAdapter`
- No depende de implementaciones concretas (CSV, API)

---

## 📝 Ejemplo Completo: Agregar Nueva Fuente de Datos

### Paso 1: Crear Nuevo Adapter

```python
# app/providers/iot_sensor_adapter.py

from app.providers.base_adapter import BaseExternalApiAdapter
from app.domain.dto import NormalizedReading

class IoTSensorAdapter(BaseExternalApiAdapter):
    """
    Adapter Pattern: IoT Sensor API
    
    Adapta datos de sensores IoT al formato común.
    """
    
    def __init__(self, mqtt_broker: str, topic: str):
        self.mqtt_broker = mqtt_broker
        self.topic = topic
    
    def fetch_readings(self) -> List[NormalizedReading]:
        # 1. Conectar a MQTT broker
        client = mqtt.Client()
        client.connect(self.mqtt_broker)
        
        # 2. Suscribirse al topic
        messages = client.subscribe(self.topic)
        
        # 3. Parsear mensajes JSON
        readings = []
        for msg in messages:
            data = json.loads(msg.payload)
            
            # 4. Normalizar a NormalizedReading
            reading = NormalizedReading(
                external_station_id=data['sensor_id'],
                pollutant_code=standardize_pollutant_name(data['pollutant']),
                value=float(data['value']),
                timestamp_utc=normalize_timestamp(data['timestamp']),
                # ... otros campos
            )
            readings.append(reading)
        
        return readings
```

### Paso 2: Registrar en el Servicio

```python
# app/services/ingestion_service.py

def create_iot_adapters(self) -> List[BaseExternalApiAdapter]:
    adapters = []
    
    for sensor_config in config['iot_sensors']:
        adapter = IoTSensorAdapter(
            mqtt_broker=sensor_config['broker'],
            topic=sensor_config['topic']
        )
        adapters.append(adapter)
    
    return adapters
```

### Paso 3: Usar (sin cambios en código existente)

```python
# El mismo código funciona para cualquier adapter
adapters = create_historical_adapters() + create_iot_adapters()

for adapter in adapters:
    readings = adapter.fetch_readings()  # ✓ Mismo método
    persist_readings(readings)            # ✓ Mismo procesamiento
```

---

## 🧪 Testing de Patrones

### Test del Adapter Pattern

```python
import pytest
from app.providers.historical_csv_adapter import HistoricalCsvAdapter

def test_csv_adapter_normalizes_data():
    """Verifica que el CSV adapter normaliza correctamente"""
    adapter = HistoricalCsvAdapter(
        csv_file_path=Path("test_data.csv"),
        station_metadata=mock_station,
        pollutant_mapping=mock_pollutants
    )
    
    readings = adapter.fetch_readings()
    
    # Assertions
    assert len(readings) > 0
    assert all(isinstance(r, NormalizedReading) for r in readings)
    assert all(r.pollutant_code in ['PM2.5', 'PM10', 'O3'] for r in readings)
    assert all(r.timestamp_utc.tzinfo is not None for r in readings)  # UTC

def test_adapters_are_interchangeable():
    """Verifica que todos los adapters cumplen el contrato"""
    csv_adapter = HistoricalCsvAdapter(...)
    api_adapter = MockApiAdapter(...)
    
    def process_adapter(adapter: BaseExternalApiAdapter):
        readings = adapter.fetch_readings()
        return len(readings)
    
    # Ambos funcionan con la misma función
    assert process_adapter(csv_adapter) > 0
    assert process_adapter(api_adapter) > 0
```

---

## 📚 Referencias

### Adapter Pattern
- **Gang of Four**: "Design Patterns: Elements of Reusable Object-Oriented Software"
- **Refactoring Guru**: https://refactoring.guru/design-patterns/adapter
- **Use Case**: Integrar múltiples fuentes de datos con interfaces incompatibles

### Repository Pattern
- **Martin Fowler**: "Patterns of Enterprise Application Architecture"
- **Use Case**: Separar lógica de negocio de acceso a datos

### DTO Pattern
- **Martin Fowler**: "Patterns of Enterprise Application Architecture"
- **Pydantic Docs**: https://docs.pydantic.dev/
- **Use Case**: Transferir datos entre capas manteniendo type safety

---

## 🔮 Evolución Futura

### Patrones Candidatos para Implementar

#### 1. Factory Pattern
Para crear adapters dinámicamente:

```python
class AdapterFactory:
    @staticmethod
    def create_adapter(source_type: str, config: dict) -> BaseExternalApiAdapter:
        if source_type == "csv":
            return HistoricalCsvAdapter(**config)
        elif source_type == "aqicn":
            return AqicnAdapter(**config)
        elif source_type == "iot":
            return IoTSensorAdapter(**config)
        else:
            raise ValueError(f"Unknown source type: {source_type}")
```

#### 2. Observer Pattern
Para notificaciones cuando llegan nuevos datos:

```python
class IngestionObserver(ABC):
    @abstractmethod
    def on_readings_ingested(self, count: int):
        pass

class MetricsObserver(IngestionObserver):
    def on_readings_ingested(self, count: int):
        send_to_prometheus({"readings_ingested": count})
```

#### 3. Chain of Responsibility
Para procesamiento de validación en cadena:

```python
class ValidationHandler(ABC):
    def __init__(self, next_handler=None):
        self.next = next_handler
    
    @abstractmethod
    def validate(self, reading: NormalizedReading) -> bool:
        pass

class RangeValidator(ValidationHandler):
    def validate(self, reading):
        if not is_valid_concentration(reading.value, reading.pollutant_code):
            return False
        return self.next.validate(reading) if self.next else True
```

---

## 📊 Resumen

| Patrón | Ubicación | Estado | Propósito |
|--------|-----------|--------|-----------|
| **Adapter** | `app/providers/` | ✅ Implementado | Unificar fuentes de datos |
| **DTO** | `app/domain/dto.py` | ✅ Implementado | Transferencia entre capas |
| **Repository** | `app/services/` | ✅ Implícito | Acceso a datos |
| **Strategy** | `app/domain/normalization.py` | ✅ Implícito | Algoritmos de normalización |
| **Factory** | - | 📋 Futuro | Creación dinámica de adapters |
| **Observer** | - | 📋 Futuro | Notificaciones de eventos |

---

**Última actualización**: 26 de noviembre de 2025  
**Autor**: Air Quality Platform Team  
**Versión**: 1.0
