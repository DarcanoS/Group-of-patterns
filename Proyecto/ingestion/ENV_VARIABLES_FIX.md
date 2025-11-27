# Corrección de Variables de Entorno

## Problema Identificado

El servicio de ingestión no estaba leyendo correctamente la ruta de los archivos de datos porque las variables en el archivo `.env` **no coincidían** con los nombres que Pydantic Settings espera en `app/config.py`.

### Variables Incorrectas (antes)
```env
DATA_DIR=../data_air
HISTORICAL_DATA_DIR=../data_air
STATION_MAPPING_FILE=./data/station_mapping.yaml
HISTORICAL_ENABLED=true
REALTIME_ENABLED=false
```

### Variables Correctas (ahora)
```env
HISTORICAL_DATA_PATH=../data_air
STATION_MAPPING_PATH=./data/station_mapping.yaml
INGESTION_MODE=historical
ALLOW_REINGESTION=true
LOG_FORMAT=colorlog
```

## Explicación Técnica

Pydantic Settings lee las variables de entorno usando el nombre del atributo en la clase `Settings`. Por ejemplo:

```python
class Settings(BaseSettings):
    historical_data_path: Path = Field(
        default=Path("../data_air"),
        description="Path to historical CSV and GeoJSON data files"
    )
```

Pydantic buscará la variable de entorno `HISTORICAL_DATA_PATH` (case-insensitive). Si usas `DATA_DIR` en el `.env`, Pydantic **NO** lo reconocerá y usará el valor por defecto.

## Cambios Realizados

### 1. Archivo `.env`
- ✅ Renombrado `DATA_DIR` → `HISTORICAL_DATA_PATH`
- ✅ Renombrado `STATION_MAPPING_FILE` → `STATION_MAPPING_PATH`
- ✅ Eliminado `HISTORICAL_DATA_DIR` (duplicado)
- ✅ Eliminado `HISTORICAL_ENABLED` (usar `INGESTION_MODE` en su lugar)
- ✅ Eliminado `REALTIME_ENABLED` (usar `INGESTION_MODE` en su lugar)
- ✅ Agregado `LOG_FORMAT=colorlog`
- ✅ Agregado `INGESTION_MODE=historical`
- ✅ Agregado `ALLOW_REINGESTION=true`
- ✅ Agregado `AQICN_BASE_URL` y `AQICN_CITIES`

### 2. Archivo `.env.example`
- ✅ Actualizado con los nombres correctos de variables
- ✅ Documentado que `TOKEN_API_AQICN` es el alias para `aqicn_api_key`
- ✅ Agregado `AQICN_CITIES` con ejemplo

## Variables que Pydantic Espera

### Base de Datos
```env
DATABASE_URL=postgresql://user:password@host:port/dbname
# O componentes individuales:
DB_HOST=localhost
DB_PORT=5433
DB_NAME=air_quality_db
DB_USER=air_quality_admin
DB_PASSWORD=admin_secure_password
```

### API Externa (AQICN)
```env
TOKEN_API_AQICN=your_api_token_here      # Alias para aqicn_api_key
AQICN_BASE_URL=https://api.waqi.info
AQICN_CITIES=bogota                       # Alias para aqicn_cities
```

### Configuración de Ingestión
```env
HISTORICAL_DATA_PATH=../data_air
STATION_MAPPING_PATH=./data/station_mapping.yaml
INGESTION_INTERVAL_MINUTES=10
INGESTION_LOG_LEVEL=INFO
LOG_FORMAT=colorlog
INGESTION_MODE=historical
ALLOW_REINGESTION=true
```

## Verificación

Para verificar que las variables se están leyendo correctamente, ejecuta:

```bash
cd Proyecto/ingestion
source venv/bin/activate
python test_env_vars.py
```

Este script mostrará:
- ✅ Qué variables están definidas en `.env`
- ✅ Qué variables Pydantic espera
- ✅ Qué variables no se están usando
- ✅ Los valores finales cargados por `settings`
- ✅ La ruta resuelta para `data_air`

## Resultado

Ahora `settings.get_historical_data_path()` retorna correctamente:
```
/home/stivel/Documentos/UD/2025_3/Patrones/Repos/Group_of_patterns/Proyecto/data_air
```

En lugar del valor incorrecto `/pot/data_air` que aparecía antes.

## Variables No Utilizadas (pueden eliminarse)

Estas variables están en `.env` pero no las usa el código actual:
- `MONGO_URI` - Reservado para futuro uso con MongoDB
- `MONGO_DB_NAME` - Reservado para futuro uso con MongoDB

Puedes dejarlas comentadas para uso futuro.
