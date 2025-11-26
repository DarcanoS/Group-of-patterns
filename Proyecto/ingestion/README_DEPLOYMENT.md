# 🚀 Deployment Guide - Air Quality Ingestion Service

Guía completa para desplegar el servicio de ingestion en un servidor Ubuntu.

---

## 📋 Requisitos Previos

### Servidor Ubuntu
- Ubuntu 20.04 LTS o superior
- Acceso SSH
- Usuario con privilegios sudo
- Mínimo 512MB RAM
- Mínimo 2GB espacio en disco

### Base de Datos
- PostgreSQL 12+ con PostGIS instalado
- Base de datos `air_quality_db` creada
- Usuario con permisos de escritura
- Tablas creadas (ejecutar `database/seed_data.sql`)

### APIs Externas
- Token de AQICN API (obtener en https://aqicn.org/data-platform/token/)

---

## 🎯 Deployment Rápido (Recomendado)

### Paso 1: Clonar Repositorio

```bash
# En tu servidor Ubuntu
cd /tmp
git clone https://github.com/your-org/air-quality-platform.git
cd air-quality-platform/Proyecto/ingestion
```

### Paso 2: Ejecutar Script de Deployment

```bash
# Hacer ejecutable
chmod +x deploy/deploy.sh

# Ejecutar
./deploy/deploy.sh
```

El script te preguntará si quieres configurar:
- **Systemd Timer** (recomendado para producción)
- **Cron Job** (más simple)
- **Manual** (configurar después)

### Paso 3: Configurar Variables de Entorno

```bash
# Editar configuración
sudo nano /opt/air-quality-ingestion/.env
```

**Variables críticas**:
```bash
DATABASE_URL=postgresql://user:password@host:5432/air_quality_db
TOKEN_API_AQICN=tu_token_aqui
INGESTION_LOG_LEVEL=INFO
```

### Paso 4: Probar Instalación

```bash
# Health check
./deploy/health_check.sh

# Prueba manual
cd /opt/air-quality-ingestion
source venv/bin/activate
python -m app.main --mode realtime
```

### Paso 5: Verificar Logs

```bash
# Ver logs de ingestion
tail -f /var/log/air-quality-ingestion/ingestion.log

# Ver errores
tail -f /var/log/air-quality-ingestion/error.log
```

✅ **¡Listo!** El servicio debería estar ejecutándose automáticamente cada 10 minutos.

---

## 📂 Estructura Post-Deployment

```
/opt/air-quality-ingestion/          # Aplicación
├── app/                              # Código fuente
├── data/                             # Configuración
├── venv/                             # Virtual environment
├── .env                              # Configuración (protegido 600)
└── requirements.txt

/var/log/air-quality-ingestion/       # Logs
├── ingestion.log                     # Logs de ejecución
└── error.log                         # Errores

/etc/systemd/system/                  # Systemd (si usas systemd)
├── air-quality-ingestion.service
└── air-quality-ingestion.timer
```

---

## 🔧 Deployment Manual (Paso a Paso)

Si prefieres instalar manualmente sin el script:

### 1. Instalar Dependencias del Sistema

```bash
sudo apt-get update
sudo apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    postgresql-client \
    git
```

### 2. Crear Directorios

```bash
sudo mkdir -p /opt/air-quality-ingestion
sudo mkdir -p /var/log/air-quality-ingestion
sudo chown $USER:$USER /opt/air-quality-ingestion
sudo chown $USER:$USER /var/log/air-quality-ingestion
```

### 3. Copiar Archivos

```bash
# Desde tu repo local
cd /path/to/Proyecto/ingestion
cp -r app /opt/air-quality-ingestion/
cp -r data /opt/air-quality-ingestion/
cp requirements.txt /opt/air-quality-ingestion/
cp .env.example /opt/air-quality-ingestion/.env
```

### 4. Crear Virtual Environment

```bash
cd /opt/air-quality-ingestion
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
deactivate
```

### 5. Configurar .env

```bash
nano /opt/air-quality-ingestion/.env
```

Editar:
```bash
DATABASE_URL=postgresql://user:pass@host:5432/air_quality_db
TOKEN_API_AQICN=your_real_token_here
INGESTION_LOG_LEVEL=INFO
```

### 6. Configurar Permisos

```bash
chmod 600 /opt/air-quality-ingestion/.env
```

---

## ⏰ Configurar Automatización

### Opción A: Systemd Timer (Recomendado)

**Ventajas**:
- Integrado con sistema
- Logs con `journalctl`
- Fácil de monitorear
- Restart automático en fallos

**Setup**:
```bash
./deploy/setup_systemd.sh
```

**Comandos útiles**:
```bash
# Ver estado
sudo systemctl status air-quality-ingestion.timer

# Ver logs
sudo journalctl -u air-quality-ingestion.service -f

# Ejecutar manualmente
sudo systemctl start air-quality-ingestion.service

# Detener
sudo systemctl stop air-quality-ingestion.timer

# Reiniciar
sudo systemctl restart air-quality-ingestion.timer
```

### Opción B: Cron Job (Más Simple)

**Ventajas**:
- Familiar para la mayoría
- No requiere systemd
- Setup más simple

**Setup**:
```bash
./deploy/setup_cron.sh
```

**Comandos útiles**:
```bash
# Ver crontab
crontab -l

# Editar crontab
crontab -e

# Ejecutar manualmente
/opt/air-quality-ingestion/run_ingestion.sh
```

---

## 🔍 Monitoreo y Troubleshooting

### Health Check

```bash
# Ejecutar health check completo
./deploy/health_check.sh
```

Verifica:
- ✓ Directorios instalados
- ✓ Virtual environment
- ✓ Configuración
- ✓ Conexión a base de datos
- ✓ Token de API
- ✓ Logs recientes
- ✓ Errores

### Ver Logs

```bash
# Logs de ingestion (últimas 100 líneas)
tail -100 /var/log/air-quality-ingestion/ingestion.log

# Seguir logs en tiempo real
tail -f /var/log/air-quality-ingestion/ingestion.log

# Errores
tail -50 /var/log/air-quality-ingestion/error.log

# Logs de systemd (si usas systemd)
sudo journalctl -u air-quality-ingestion.service -n 100
```

### Problemas Comunes

#### 1. Error: "Database connection failed"

**Causa**: Credenciales incorrectas o DB inaccesible

**Solución**:
```bash
# Verificar .env
cat /opt/air-quality-ingestion/.env | grep DATABASE_URL

# Probar conexión
psql "postgresql://user:pass@host:5432/air_quality_db" -c "SELECT 1"
```

#### 2. Error: "No stations found in database"

**Causa**: Base de datos sin datos seed

**Solución**:
```bash
# Ejecutar seed data
cd /path/to/database
psql $DATABASE_URL -f seed_data.sql
```

#### 3. Error: "AQICN API: 401 Unauthorized"

**Causa**: Token inválido o expirado

**Solución**:
```bash
# Verificar token
cat /opt/air-quality-ingestion/.env | grep AQICN_TOKEN

# Obtener nuevo token en:
# https://aqicn.org/data-platform/token/

# Actualizar .env
nano /opt/air-quality-ingestion/.env
```

#### 4. Error: "Permission denied"

**Causa**: Permisos incorrectos

**Solución**:
```bash
# Verificar ownership
ls -la /opt/air-quality-ingestion/

# Corregir si es necesario
sudo chown -R $USER:$USER /opt/air-quality-ingestion/
chmod 600 /opt/air-quality-ingestion/.env
```

#### 5. Servicio no ejecuta automáticamente

**Si usas systemd**:
```bash
# Verificar timer
sudo systemctl status air-quality-ingestion.timer

# Ver próxima ejecución
sudo systemctl list-timers | grep air-quality

# Habilitar si está deshabilitado
sudo systemctl enable air-quality-ingestion.timer
sudo systemctl start air-quality-ingestion.timer
```

**Si usas cron**:
```bash
# Verificar crontab
crontab -l | grep air-quality

# Ver logs de cron
grep CRON /var/log/syslog | tail -20
```

---

## 🔄 Actualización del Servicio

### Actualizar Código

```bash
# Detener servicio
# Si usas systemd:
sudo systemctl stop air-quality-ingestion.timer

# Si usas cron:
crontab -e  # Comentar línea temporalmente

# Actualizar código
cd /tmp
git clone https://github.com/your-org/air-quality-platform.git
cd air-quality-platform/Proyecto/ingestion

# Backup actual
sudo cp -r /opt/air-quality-ingestion /opt/air-quality-ingestion.backup

# Copiar nuevos archivos
cp -r app /opt/air-quality-ingestion/
cp -r data /opt/air-quality-ingestion/

# Actualizar dependencias
cd /opt/air-quality-ingestion
source venv/bin/activate
pip install -r requirements.txt
deactivate

# Reiniciar servicio
# Si usas systemd:
sudo systemctl start air-quality-ingestion.timer

# Si usas cron:
crontab -e  # Descomentar línea
```

### Actualizar Configuración

```bash
# Editar .env
nano /opt/air-quality-ingestion/.env

# No es necesario reiniciar, se lee cada ejecución
```

---

## 🗑️ Desinstalación

```bash
./deploy/uninstall.sh
```

O manualmente:
```bash
# Detener servicios
sudo systemctl stop air-quality-ingestion.timer 2>/dev/null || true
sudo systemctl disable air-quality-ingestion.timer 2>/dev/null || true

# Remover archivos
sudo rm -f /etc/systemd/system/air-quality-ingestion.*
sudo systemctl daemon-reload
sudo rm -rf /opt/air-quality-ingestion
sudo rm -rf /var/log/air-quality-ingestion

# Remover cron
crontab -e  # Eliminar líneas de air-quality
```

---

## 📊 Validación Post-Deployment

### Checklist de Validación

- [ ] Health check pasa todas las pruebas
- [ ] Conexión a base de datos funciona
- [ ] Token de AQICN configurado (no demo)
- [ ] Logs se están generando
- [ ] Timer/cron está activo
- [ ] Primera ejecución exitosa
- [ ] Datos insertados en base de datos

### Comandos de Validación

```bash
# 1. Health check
./deploy/health_check.sh

# 2. Verificar última ejecución
tail -20 /var/log/air-quality-ingestion/ingestion.log

# 3. Verificar datos en BD
psql $DATABASE_URL -c "
SELECT 
    COUNT(*) as total_readings,
    MAX(datetime) as last_reading
FROM air_quality_reading
WHERE datetime > NOW() - INTERVAL '1 hour';
"

# 4. Verificar próxima ejecución (systemd)
sudo systemctl list-timers | grep air-quality

# 5. Verificar cron (si usas cron)
crontab -l
```

---

## 📈 Monitoreo Continuo

### Métricas a Monitorear

1. **Frecuencia de ejecución**: Debe ejecutar cada 10 minutos
2. **Lecturas insertadas**: Debe haber datos nuevos cada hora
3. **Errores**: Log de errores debe estar (casi) vacío
4. **Uso de disco**: Logs no deben crecer infinitamente

### Script de Monitoreo (Opcional)

```bash
# Crear script simple de alerta
cat > /opt/air-quality-ingestion/monitor.sh <<'EOF'
#!/bin/bash
LOG_FILE="/var/log/air-quality-ingestion/ingestion.log"
ERROR_FILE="/var/log/air-quality-ingestion/error.log"

# Verificar si hay ejecuciones recientes (últimos 15 min)
RECENT=$(find $LOG_FILE -mmin -15 2>/dev/null)
if [ -z "$RECENT" ]; then
    echo "WARNING: No recent ingestion activity!"
    # Aquí puedes agregar notificación por email/webhook
fi

# Verificar errores recientes
ERRORS=$(tail -100 $ERROR_FILE 2>/dev/null | grep -c "ERROR")
if [ $ERRORS -gt 5 ]; then
    echo "WARNING: $ERRORS errors in last 100 lines!"
fi
EOF

chmod +x /opt/air-quality-ingestion/monitor.sh

# Ejecutar cada hora
(crontab -l; echo "0 * * * * /opt/air-quality-ingestion/monitor.sh") | crontab -
```

---

## 🔐 Seguridad

### Mejores Prácticas

1. **Permisos de .env**:
   ```bash
   chmod 600 /opt/air-quality-ingestion/.env
   ```

2. **Usuario no-root**:
   - Nunca ejecutar como root
   - Usar usuario dedicado si es posible

3. **Firewall**:
   ```bash
   # Solo permitir PostgreSQL desde IPs específicas
   sudo ufw allow from <db_server_ip> to any port 5432
   ```

4. **Credenciales**:
   - No commits de .env al repositorio
   - Rotar tokens periódicamente
   - Usar secretos manager en producción seria

5. **Updates**:
   ```bash
   # Mantener sistema actualizado
   sudo apt-get update && sudo apt-get upgrade
   ```

---

## 📚 Referencias

- **Código fuente**: `/opt/air-quality-ingestion/app/`
- **Documentación técnica**: `Proyecto/ingestion/docs/`
- **Tests**: `Proyecto/ingestion/tests/`
- **Logs**: `/var/log/air-quality-ingestion/`
- **AQICN API**: https://aqicn.org/json-api/doc/

---

## 🆘 Soporte

### Logs para Debugging

Cuando reportes un problema, incluye:

```bash
# 1. Health check
./deploy/health_check.sh > health_check.txt

# 2. Últimos logs
tail -100 /var/log/air-quality-ingestion/ingestion.log > logs.txt

# 3. Errores
tail -50 /var/log/air-quality-ingestion/error.log > errors.txt

# 4. Configuración (sin secretos)
cat /opt/air-quality-ingestion/.env | grep -v "PASSWORD\|TOKEN" > config.txt
```

---

**Última actualización**: 26 de noviembre de 2025  
**Versión**: 1.0  
**Plataforma**: Ubuntu 20.04+ LTS
