# Database Containers - Podman Setup

Este documento describe cómo ejecutar PostgreSQL + PostGIS y MongoDB usando contenedores Podman para Air Quality Platform.

## 📌 Importante: Configuración de Credenciales

**Los contenedores leen la configuración del archivo `.env`** (NO `.env.containers`).

- `.env.example` - Archivo plantilla con todas las variables
- `.env.containers.example` - Misma plantilla (nombre alternativo)
- `.env` - **TU configuración real** (gitignored, no se hace commit)

### Pasos de Configuración:

1. Copia el archivo de ejemplo:
   ```bash
   cp .env.example .env
   ```

2. Edita con contraseñas seguras:
   ```bash
   nano .env
   ```

3. **NUNCA hagas commit de `.env`** - contiene credenciales sensibles

---

## 📋 Requisitos Previos

- **Podman** instalado en Ubuntu
- **podman-compose** (opcional pero recomendado)
- Puertos disponibles: `5433` (PostgreSQL), `27017` (MongoDB)

### Instalación de Podman

```bash
# Ubuntu 22.04+
sudo apt update
sudo apt install podman

# Verificar instalación
podman --version
```

### Instalación de podman-compose (Opcional)

```bash
# Instalar con pip
pip3 install podman-compose

# O usar el paquete de sistema
sudo apt install podman-compose
```

## 🚀 Inicio Rápido

### 1. Configurar Variables de Entorno

```bash
cd Proyecto/database/

# Copiar el template de configuración
cp .env.example .env

# Editar con tus credenciales (¡IMPORTANTE en producción!)
nano .env
```

**IMPORTANTE**: Cambia TODAS las contraseñas en el archivo `.env` antes de usar en producción.

### 2. Iniciar Contenedores

```bash
# Usando el script auxiliar (recomendado)
./containers.sh up podman

# O manualmente con podman-compose
podman-compose -f podman-compose.yml up -d
```

### 3. Verificar Estado

```bash
# Ver estado de contenedores
./containers.sh status

# Verificar salud de contenedores
./containers.sh health
```

## 🛠️ Script de Gestión: `containers.sh`

El script `containers.sh` proporciona una interfaz simplificada para gestionar los contenedores.

### Comandos Disponibles

```bash
./containers.sh start          # Iniciar contenedores
./containers.sh stop           # Detener contenedores
./containers.sh restart        # Reiniciar contenedores
./containers.sh status         # Ver estado
./containers.sh health         # Verificar salud
./containers.sh logs [nombre]  # Ver logs (postgres, mongo, o all)
./containers.sh psql           # Conectar a PostgreSQL
./containers.sh mongo          # Conectar a MongoDB
./containers.sh info           # Mostrar información de conexión
./containers.sh cleanup        # Eliminar contenedores y datos (¡CUIDADO!)
./containers.sh help           # Mostrar ayuda
```

### Ejemplos de Uso

```bash
# Iniciar todo
./containers.sh start

# Ver logs de PostgreSQL
./containers.sh logs postgres

# Conectar a la base de datos
./containers.sh psql

# Ver información de conexión
./containers.sh info
```

## 📦 Contenedores Incluidos

### PostgreSQL + PostGIS

- **Imagen**: `postgis/postgis:17-3.5`
- **Puerto**: `5433` (mapeado desde el puerto interno `5432`)
- **Base de datos**: `air_quality_db`
- **Usuarios**:
  - `postgres` (superusuario)
  - `air_quality_admin` (administración, migraciones)
  - `air_quality_app` (aplicación en runtime)

**Características**:
- PostGIS 3.5 habilitado
- Scripts de inicialización automáticos
- Health checks configurados
- Volumen persistente: `air-quality-postgis-data`

### MongoDB

- **Imagen**: `mongo:7.0`
- **Puerto**: `27017`
- **Base de datos**: `air_quality_config`
- **Usuarios**:
  - `root` (administrador)
  - `air_quality_user` (aplicación)

**Características**:
- Colecciones con validación de esquema
- Índices de rendimiento
- Health checks configurados
- Volúmenes persistentes:
  - `air-quality-mongodb-data`
  - `air-quality-mongodb-config`

## 🗂️ Estructura de Archivos

```
database/
├── podman-compose.yml         # Definición de contenedores
├── .env.containers            # Template de configuración
├── containers.sh              # Script de gestión
│
├── postgresql/                # Scripts de PostgreSQL
│   ├── init_schema.sql       # Se ejecuta automáticamente
│   ├── setup_users_permissions.sql
│   └── seed_data.sql
│
└── mongodb/                   # Scripts de MongoDB
    ├── mongo_init.js         # Se ejecuta automáticamente
    └── mongo_indexes.js
```

## 🔄 Inicialización Automática

Los contenedores ejecutan automáticamente scripts de inicialización en el primer arranque:

### PostgreSQL (orden de ejecución):
1. `01-init_schema.sql` → Crea todas las tablas
2. `02-setup_permissions.sql` → Configura permisos de usuarios
3. `03-seed_data.sql` → Inserta datos iniciales

### MongoDB (orden de ejecución):
1. `01-mongo_init.js` → Crea colecciones y usuarios
2. `02-mongo_indexes.js` → Crea índices de rendimiento

## 🔌 Cadenas de Conexión

### PostgreSQL (Admin)
```bash
postgresql://air_quality_admin:admin_secure_password@localhost:5433/air_quality_db
```

### PostgreSQL (App)
```bash
postgresql://air_quality_app:app_secure_password@localhost:5433/air_quality_db
```

### MongoDB
```bash
mongodb://air_quality_user:secure_password@localhost:27017/air_quality_config
```

## 📊 Gestión de Volúmenes

### Ver volúmenes creados
```bash
podman volume ls | grep air-quality
```

### Inspeccionar un volumen
```bash
podman volume inspect air-quality-postgis-data
```

### Backup de datos
```bash
# PostgreSQL
podman exec air-quality-postgis pg_dump -U postgres air_quality_db > backup.sql

# MongoDB
podman exec air-quality-mongodb mongodump --out /tmp/backup
podman cp air-quality-mongodb:/tmp/backup ./mongodb-backup
```

### Restaurar datos
```bash
# PostgreSQL
cat backup.sql | podman exec -i air-quality-postgis psql -U postgres -d air_quality_db

# MongoDB
podman cp ./mongodb-backup air-quality-mongodb:/tmp/backup
podman exec air-quality-mongodb mongorestore /tmp/backup
```

## 🔒 Seguridad

### En Desarrollo
- Las credenciales por defecto están en `.env.containers`
- Puertos expuestos en localhost

### En Producción
- **CAMBIAR TODAS LAS CONTRASEÑAS** en `.env.containers`
- Usar secretos de Podman:
  ```bash
  echo "secret_password" | podman secret create db_password -
  ```
- Configurar firewall para limitar acceso a puertos
- Usar volúmenes con permisos restringidos
- Habilitar SSL/TLS para conexiones

## 🐛 Troubleshooting

### Contenedores no inician
```bash
# Ver logs detallados
./containers.sh logs postgres
./containers.sh logs mongo

# Verificar puertos en uso
ss -tuln | grep -E '5433|27017'
```

### Error de permisos en volúmenes
```bash
# Verificar propiedad de volúmenes
podman volume inspect air-quality-postgis-data

# Recrear volúmenes si es necesario
./containers.sh cleanup
./containers.sh start
```

### Scripts de inicialización no se ejecutan
Los scripts solo se ejecutan en el **primer inicio** cuando el volumen está vacío. Para forzar reinicialización:

```bash
# Eliminar volúmenes
./containers.sh cleanup

# Iniciar de nuevo
./containers.sh start
```

### Conexión rechazada
```bash
# Verificar que los contenedores estén corriendo
./containers.sh status

# Verificar health checks
./containers.sh health

# Probar conexión directa
podman exec air-quality-postgis pg_isready -U postgres
```

## 🔄 Migración desde Contenedores Existentes

Si ya tienes contenedores PostgreSQL/MongoDB corriendo:

### Opción 1: Cambiar puertos
Edita `.env.containers` para usar puertos diferentes:
```bash
POSTGRES_PORT=5434
MONGO_PORT=27018
```

### Opción 2: Exportar e importar datos
```bash
# Exportar desde contenedor existente
podman exec postgis-db pg_dump -U postgres air_quality_db > export.sql

# Importar a nuevo contenedor
./containers.sh start
cat export.sql | podman exec -i air-quality-postgis psql -U postgres -d air_quality_db
```

## 📚 Referencias

- [Podman Documentation](https://docs.podman.io/)
- [podman-compose](https://github.com/containers/podman-compose)
- [PostGIS Docker](https://registry.hub.docker.com/r/postgis/postgis/)
- [MongoDB Docker](https://hub.docker.com/_/mongo)

## 🆘 Comandos Útiles de Podman

```bash
# Ver contenedores corriendo
podman ps

# Ver todos los contenedores
podman ps -a

# Ver volúmenes
podman volume ls

# Ver redes
podman network ls

# Limpiar recursos no usados
podman system prune

# Ver uso de recursos
podman stats

# Inspeccionar contenedor
podman inspect air-quality-postgis
```
