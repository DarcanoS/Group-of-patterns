# Tests - Ingestion Service

Esta carpeta contiene tests para el servicio de ingestion.

## 📂 Archivos

### `test_aqicn_api.py`
**Propósito**: Verificar conectividad y funcionamiento de la API de AQICN

**Qué prueba**:
- ✅ Conexión con la API de AQICN
- ✅ Autenticación con token
- ✅ Obtención de datos de estaciones
- ✅ Formato de respuesta

**Cómo ejecutar**:
```bash
cd /path/to/Proyecto/ingestion
python tests/test_aqicn_api.py
```

**Resultado esperado**:
```
Testing AQICN API connection...
✅ API connection successful!
✅ Retrieved data for station: [station_name]
```

---

### `test_aqicn_ingestion.py`
**Propósito**: Probar el flujo completo de ingestion en tiempo real

**Qué prueba**:
- ✅ Configuración del servicio de ingestion
- ✅ Conexión a base de datos
- ✅ Adaptador AQICN funcional
- ✅ Normalización de datos
- ✅ Inserción en base de datos
- ✅ Detección de duplicados

**Cómo ejecutar**:
```bash
cd /path/to/Proyecto/ingestion
python tests/test_aqicn_ingestion.py
```

**Resultado esperado**:
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

---

## ⚙️ Requisitos

Para ejecutar los tests necesitas:

1. **Base de datos configurada**:
   - PostgreSQL corriendo
   - Tablas creadas (`station`, `pollutant`, `air_quality_reading`)
   - Datos seed de pollutants

2. **Variables de entorno** (`.env`):
   ```bash
   DATABASE_URL=postgresql://user:password@localhost:5432/air_quality_db
   TOKEN_API_AQICN=your_api_key_here
   ```

3. **Dependencias instaladas**:
   ```bash
   pip install -r requirements.txt
   ```

---

## 🐛 Troubleshooting

### Error: "AQICN_API_KEY not configured"
**Solución**: Verifica que `.env` tenga `TOKEN_API_AQICN` definido

### Error: "No stations found in database"
**Solución**: Ejecuta primero los scripts de seed:
```bash
cd ../database
psql $DATABASE_URL -f seed_data.sql
```

### Error: "Connection refused"
**Solución**: Verifica que PostgreSQL esté corriendo:
```bash
pg_isready -h localhost -p 5432
```

---

## 📝 Notas

- Los tests **NO** son destructivos, puedes ejecutarlos múltiples veces
- El test de ingestion detecta duplicados automáticamente
- Si re-ejecutas el test de ingestion, verás más skips y 0 inserts (esperado)

---

**Última actualización**: 26 de noviembre de 2025
