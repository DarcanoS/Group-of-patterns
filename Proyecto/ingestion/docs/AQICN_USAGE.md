# AQICN Real-Time Ingestion - Guía de Uso

## ✅ Implementación Completada

Se ha implementado exitosamente la ingesta en tiempo real usando la API de AQICN (Air Quality Index China Network).

### 🎯 Características

- **Patrón Adapter**: Implementa el patrón de diseño Adapter para unificar datos de AQICN con nuestro formato interno
- **Basado en Estaciones Existentes**: Consulta automáticamente las estaciones que ya están en la base de datos
- **Matching Inteligente**: Mapea nombres de estaciones de AQICN a nombres de nuestra BD
- **Datos en Tiempo Real**: Obtiene lecturas actuales cada vez que se ejecuta

### 📊 Datos Obtenidos

Por cada estación consulta:
- PM2.5 (µg/m³)
- PM10 (µg/m³)
- O3 (ppb)
- NO2 (ppb)
- SO2 (ppb)
- CO (ppm)

### 🚀 Uso

#### 1. Configuración

El token de API ya está configurado en `.env`:

```bash
TOKEN_API_AQICN=56de3cea9ff0128d2aca8e86f4ff5b20bd8ddc4e
```

#### 2. Ejecutar Ingesta en Tiempo Real

```bash
# Desde Proyecto/ingestion/
source venv/bin/activate
python -m app.main --mode realtime --log-level INFO
```

#### 3. Ejecutar Pruebas

**Prueba de API** (verifica conectividad):
```bash
python3 test_aqicn_api.py
```

**Prueba de Ingesta Completa** (incluye inserción en BD):
```bash
python3 test_aqicn_ingestion.py
```

### 📋 Resultado de Prueba

```
==========================================================================
AQICN REAL-TIME INGESTION - QUICK TEST
==========================================================================

📋 Configuration:
   API Key: 56de3cea9ff0128d2aca...
   Base URL: https://api.waqi.info
   Cities: bogota

🔌 Testing database connection...
✅ Database connection OK

🚀 Running AQICN ingestion...

==========================================================================
✅ SUCCESS!
==========================================================================
   Total fetched: 27
   Inserted:      27
   Skipped:       0
==========================================================================
```

### 🔄 Flujo de Trabajo

1. **Cargar Estaciones**: Lee todas las estaciones de la base de datos
2. **Extraer Coordenadas**: Obtiene lat/lon de cada estación
3. **Consultar AQICN**: Usa endpoint `/feed/geo:{lat};{lon}/` para cada ubicación
4. **Normalizar Datos**: Convierte respuesta AQICN a formato interno
5. **Matching**: Asocia datos con estaciones existentes usando nombres
6. **Persistir**: Inserta lecturas en `air_quality_reading`

### 📝 Estaciones de Bogotá

El servicio consulta automáticamente las 5 estaciones que tenemos:

1. **Carvajal** (4.5958, -74.1486)
2. **Centro de Alto Rendimiento** (4.6321, -74.1383)
3. **Las Ferias** (4.6921, -74.0936)
4. **Puente Aranda** (4.6165, -74.1175)
5. **Suba** (4.7451, -74.0861)

### 🏗️ Arquitectura

```
IngestionService
    ↓
AqicnApiAdapter (Adapter Pattern)
    ↓
AQICN API (https://api.waqi.info)
    ↓
NormalizedReading (DTO)
    ↓
Database (air_quality_reading)
```

### 🔍 Mapeo de Estaciones

El adapter incluye lógica para mapear nombres de AQICN a nuestra BD:

| AQICN API                      | Base de Datos                |
|--------------------------------|------------------------------|
| Carvajal - Sevillana           | Carvajal                     |
| Centro de Alto Rendimiento     | Centro de Alto Rendimiento   |
| Las Ferias                     | Las Ferias                   |
| Puente Aranda                  | Puente Aranda                |
| Suba                           | Suba                         |

### ⚙️ Configuración Avanzada

En `.env` puedes configurar:

```bash
# Token de API (obligatorio)
TOKEN_API_AQICN=your_api_key_here

# URL base (opcional, tiene default)
AQICN_BASE_URL=https://api.waqi.info

# Ciudades adicionales si se quiere usar modo ciudad (opcional)
AQICN_CITIES=bogota,medellin,cali
```

### 🔄 Automatización

Para ejecutar periódicamente:

**Con cron** (cada 10 minutos):
```bash
*/10 * * * * cd /path/to/ingestion && source venv/bin/activate && python -m app.main --mode realtime >> logs/realtime.log 2>&1
```

**Con systemd timer** (recomendado para producción):
```ini
[Unit]
Description=AQICN Real-Time Data Ingestion
Wants=aqicn-ingestion.timer

[Service]
Type=oneshot
WorkingDirectory=/path/to/Proyecto/ingestion
ExecStart=/path/to/venv/bin/python -m app.main --mode realtime
User=your_user

[Install]
WantedBy=multi-user.target
```

### 📚 Referencias

- **AQICN API Docs**: https://aqicn.org/json-api/doc/
- **Adapter Pattern**: `DESIGN_PATTERNS.md`
- **API Documentation**: `API_AQICN.md`

### 🐛 Troubleshooting

**Error: "AQICN_API_KEY not configured"**
- Verifica que `.env` tenga `TOKEN_API_AQICN` definido

**Error: "No stations found in database"**
- Ejecuta primero `seed_data.sql` para crear estaciones

**Warning: "No valid pollutant readings found"**
- Algunos endpoints de AQICN pueden no tener todos los contaminantes
- Es normal, se omiten las lecturas faltantes

---

**Fecha**: 26 de noviembre de 2025  
**Rama**: `feature/realtime-ingestion-aqicn`  
**Estado**: ✅ FUNCIONAL
