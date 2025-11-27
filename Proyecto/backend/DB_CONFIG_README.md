# Configuración de Bases de Datos

## Resumen de Cambios Aplicados

Se ha actualizado la configuración del backend para conectarse a las bases de datos remotas:

### PostgreSQL
- **Usuario**: air_quality_app
- **Host**: darcano.duckdns.org
- **Puerto**: 15433
- **Base de datos**: air_quality_db

### MongoDB
- **Host**: darcano.duckdns.org
- **Puerto**: 47017
- **Base de datos**: air_quality_config
- **Auth Source**: air_quality_config

## Archivos Modificados

1. **`.env`** - Actualizado con las credenciales de conexión
2. **`requirements.txt`** - Agregadas dependencias de MongoDB (pymongo, motor)
3. **`app/db/mongodb.py`** - Nuevo archivo para gestionar conexiones MongoDB
4. **`app/db/__init__.py`** - Exporta funciones de conexión MongoDB
5. **`app/main.py`** - Inicializa y cierra conexión MongoDB en startup/shutdown
6. **`.env.example`** - Actualizado con ejemplos de configuración

## Archivos Creados

1. **`test_db_connection.py`** - Script para probar conexiones a ambas bases de datos

## Estado Actual de Conexión

⚠️ **IMPORTANTE**: Las pruebas de conexión muestran que ambos servicios están rechazando conexiones:

```
PostgreSQL (darcano.duckdns.org:15433): Connection refused
MongoDB (darcano.duckdns.org:47017): Connection refused
```

## Diagnóstico y Soluciones

### Verificar Conectividad

Ejecuta estos comandos para diagnosticar problemas de red:

```bash
# Verificar si el host responde
ping darcano.duckdns.org

# Verificar si los puertos están abiertos
nc -zv darcano.duckdns.org 15433  # PostgreSQL
nc -zv darcano.duckdns.org 47017  # MongoDB

# Alternativa con telnet
telnet darcano.duckdns.org 15433
telnet darcano.duckdns.org 47017
```

### Posibles Causas

1. **Firewall**: Los puertos pueden estar bloqueados por un firewall
2. **Servicios Inactivos**: Las bases de datos pueden no estar corriendo
3. **Configuración de Red**: Puede haber restricciones de red o VPN requerida
4. **DuckDNS**: El dominio dinámico puede no estar apuntando a la IP correcta

### Soluciones Recomendadas

1. **Verificar servicios en el servidor**:
   ```bash
   # En el servidor donde están las bases de datos
   systemctl status postgresql
   systemctl status mongod
   ```

2. **Verificar puertos abiertos en el servidor**:
   ```bash
   # En el servidor
   sudo netstat -tlnp | grep 15433
   sudo netstat -tlnp | grep 47017
   ```

3. **Verificar configuración de PostgreSQL**:
   - Asegurar que `postgresql.conf` tiene `listen_addresses = '*'`
   - Verificar `pg_hba.conf` permite conexiones desde tu IP

4. **Verificar configuración de MongoDB**:
   - Asegurar que `mongod.conf` tiene `bindIp: 0.0.0.0`
   - Verificar que el puerto 47017 está configurado correctamente

5. **Firewall en el servidor**:
   ```bash
   # Abrir puertos si están cerrados
   sudo ufw allow 15433/tcp
   sudo ufw allow 47017/tcp
   sudo ufw reload
   ```

## Probar Conexión

Una vez resueltos los problemas de conectividad, ejecuta:

```bash
python test_db_connection.py
```

## Conectarse Manualmente

### PostgreSQL
```bash
psql -h darcano.duckdns.org -p 15433 -U air_quality_app -d air_quality_db
```

### MongoDB
```bash
mongosh "mongodb://air_quality_app:MGaC6G0!Jq@darcano.duckdns.org:47017/air_quality_config?authSource=air_quality_config"
```

## Iniciar el Backend

Una vez que las conexiones funcionen:

```bash
# Instalar dependencias (si no están instaladas)
pip install -r requirements.txt

# Iniciar el servidor
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

El backend intentará conectarse a MongoDB al iniciar, pero continuará funcionando aunque MongoDB no esté disponible (solo PostgreSQL es crítico).

## Variables de Entorno

Las credenciales están almacenadas en el archivo `.env`:

```dotenv
DATABASE_URL=postgresql://air_quality_app:MGaC6G0!Jq@darcano.duckdns.org:15433/air_quality_db
NOSQL_URI=mongodb://air_quality_app:MGaC6G0!Jq@darcano.duckdns.org:47017/air_quality_config?authSource=air_quality_config
NOSQL_DB_NAME=air_quality_config
```

⚠️ **Seguridad**: Asegúrate de no commitear el archivo `.env` a Git. Está incluido en `.gitignore`.

