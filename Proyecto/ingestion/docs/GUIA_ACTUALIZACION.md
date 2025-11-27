# 🔄 Guía de Actualización - Servicio de Ingestion

Esta guía explica cómo actualizar el código del servicio de ingestion cuando está desplegado en `/opt/air-quality-ingestion`.

---

## 🎯 Método Recomendado: Script de Actualización

### 📥 Paso 1: Descargar Script de Actualización

En tu servidor:

```bash
# Opción A: Si tienes el repo clonado en algún lugar
cd /path/to/repo/Proyecto/ingestion
sudo ./deploy/update.sh

# Opción B: Descargar solo el script
wget https://raw.githubusercontent.com/DarcanoS/Group_of_patterns/develop/Proyecto/ingestion/deploy/update.sh
chmod +x update.sh
sudo ./update.sh
```

### 🚀 Paso 2: Ejecutar Actualización

```bash
# Actualización completa (rama develop)
sudo ./deploy/update.sh

# Actualizar desde otra rama
sudo ./deploy/update.sh --branch main

# Actualizar sin reinstalar dependencias (más rápido)
sudo ./deploy/update.sh --skip-deps
```

### ✅ Paso 3: Verificar

```bash
# Ver logs en tiempo real
tail -f /var/log/air-quality-ingestion/ingestion.log

# Verificar estado del timer
systemctl status air-quality-ingestion.timer

# Ejecutar manualmente para probar
cd /opt/air-quality-ingestion
sudo -u airquality venv/bin/python -m app.main --mode realtime
```

---

## 🔧 ¿Qué Hace el Script de Actualización?

1. ✅ **Detiene el servicio temporalmente**
2. ✅ **Crea backup automático del código actual**
3. ✅ **Clona la última versión del repositorio**
4. ✅ **Copia el código nuevo (preserva .env)**
5. ✅ **Actualiza dependencias Python**
6. ✅ **Reinicia el servicio**

---

## 📋 Métodos Alternativos

### Método 1: Actualización Manual (Sin Script)

```bash
# 1. Detener servicio
sudo systemctl stop air-quality-ingestion.timer

# 2. Backup manual
sudo cp -r /opt/air-quality-ingestion /opt/air-quality-ingestion-backup-$(date +%Y%m%d)

# 3. Clonar repo actualizado
cd /tmp
git clone -b develop https://github.com/DarcanoS/Group-of-patterns.git
cd Group_of_patterns/Proyecto/ingestion

# 4. Copiar código nuevo (preservando .env y venv)
sudo rsync -av \
  --exclude 'venv/' \
  --exclude '.env' \
  --exclude '__pycache__/' \
  ./ /opt/air-quality-ingestion/

# 5. Actualizar dependencias
cd /opt/air-quality-ingestion
sudo -u airquality venv/bin/pip install -r requirements.txt

# 6. Reiniciar servicio
sudo systemctl start air-quality-ingestion.timer

# 7. Limpiar
rm -rf /tmp/Group_of_patterns
```

---

### Método 2: Usar Git Directamente (Avanzado)

Si inicializaste `/opt/air-quality-ingestion` como un repositorio git:

```bash
# 1. Detener servicio
sudo systemctl stop air-quality-ingestion.timer

# 2. Ir al directorio
cd /opt/air-quality-ingestion

# 3. Guardar cambios locales (si los hay)
sudo git stash

# 4. Actualizar
sudo git pull origin develop

# 5. Actualizar dependencias
sudo -u airquality venv/bin/pip install -r requirements.txt

# 6. Reiniciar
sudo systemctl start air-quality-ingestion.timer
```

**⚠️ Nota:** Este método NO se recomienda porque `/opt/air-quality-ingestion` normalmente NO es un repo git (solo código copiado).

---

### Método 3: Deployment Completo (Reinstalación)

Si quieres empezar de cero:

```bash
# 1. Backup de .env
sudo cp /opt/air-quality-ingestion/.env /tmp/air-quality-backup.env

# 2. Eliminar instalación antigua
sudo systemctl stop air-quality-ingestion.timer
sudo systemctl disable air-quality-ingestion.timer
sudo rm -rf /opt/air-quality-ingestion

# 3. Deployment fresco
cd /tmp
git clone -b develop https://github.com/DarcanoS/Group_of_patterns.git
cd Group_of_patterns/Proyecto/ingestion
sudo ./deploy/deploy.sh

# 4. Restaurar .env
sudo cp /tmp/air-quality-backup.env /opt/air-quality-ingestion/.env
sudo chmod 600 /opt/air-quality-ingestion/.env
sudo chown airquality:airquality /opt/air-quality-ingestion/.env

# 5. Reiniciar
sudo systemctl restart air-quality-ingestion.timer
```

---

## 🔄 Flujo Típico de Desarrollo → Producción

### En tu Máquina Local

```bash
# 1. Desarrollar y probar
cd Proyecto/ingestion
python -m app.main --mode realtime

# 2. Commit y push
git add .
git commit -m "feat(ingestion): agregar logs mejorados"
git push origin develop
```

### En el Servidor

```bash
# 3. Actualizar servidor
sudo ./deploy/update.sh --branch develop

# 4. Verificar logs
tail -f /var/log/air-quality-ingestion/ingestion.log
```

---

## 🛡️ Backups Automáticos

El script `update.sh` crea backups automáticos en:

```
/opt/air-quality-ingestion-backups/
├── backup-20251126-143022/    ← Más reciente
├── backup-20251125-100543/
├── backup-20251124-092314/
├── backup-20251123-155427/
└── backup-20251122-182156/
```

Solo mantiene los **últimos 5 backups** para ahorrar espacio.

### Restaurar un Backup

```bash
# 1. Detener servicio
sudo systemctl stop air-quality-ingestion.timer

# 2. Ver backups disponibles
ls -lh /opt/air-quality-ingestion-backups/

# 3. Restaurar el más reciente
BACKUP_DIR=$(ls -t /opt/air-quality-ingestion-backups/ | head -1)
sudo rsync -av --delete \
  /opt/air-quality-ingestion-backups/$BACKUP_DIR/ \
  /opt/air-quality-ingestion/

# 4. Reiniciar
sudo systemctl start air-quality-ingestion.timer
```

---

## 🧪 Testing Antes de Producción

Antes de actualizar en producción:

```bash
# 1. Clonar código nuevo en /tmp
cd /tmp
git clone -b develop https://github.com/DarcanoS/Group_of_patterns.git
cd Group_of_patterns/Proyecto/ingestion

# 2. Crear venv temporal
python3 -m venv test-venv
source test-venv/bin/activate
pip install -r requirements.txt

# 3. Copiar .env de producción
cp /opt/air-quality-ingestion/.env .env

# 4. Probar ejecución
python -m app.main --mode realtime

# 5. Si funciona, actualizar producción
deactivate
cd /path/to/scripts
sudo ./deploy/update.sh
```

---

## ⚠️ Problemas Comunes

### Problema 1: "requirements.txt not found"

```bash
# Verificar que requirements.txt existe
ls -lh /opt/air-quality-ingestion/requirements.txt

# Si no existe, copiar manualmente
sudo cp /tmp/repo/Proyecto/ingestion/requirements.txt /opt/air-quality-ingestion/
```

### Problema 2: Servicio no reinicia

```bash
# Ver logs del systemd
sudo journalctl -u air-quality-ingestion.service -n 50

# Reiniciar manualmente
sudo systemctl restart air-quality-ingestion.timer
sudo systemctl status air-quality-ingestion.timer
```

### Problema 3: Dependencias rotas

```bash
# Reinstalar todas las dependencias
cd /opt/air-quality-ingestion
source venv/bin/activate
pip uninstall -y -r <(pip freeze)
pip install -r requirements.txt
deactivate
```

### Problema 4: .env perdido

```bash
# Verificar
ls -lh /opt/air-quality-ingestion/.env

# Restaurar desde backup
sudo cp /opt/air-quality-ingestion-backups/backup-*/  .env \
  /opt/air-quality-ingestion/.env
sudo chmod 600 /opt/air-quality-ingestion/.env
```

---

## 📊 Monitoreo Post-Actualización

Después de actualizar, monitorea durante al menos 30 minutos:

```bash
# Terminal 1: Logs en tiempo real
tail -f /var/log/air-quality-ingestion/ingestion.log

# Terminal 2: Estado del servicio
watch -n 10 'systemctl status air-quality-ingestion.timer'

# Terminal 3: Verificar base de datos
psql -U airquality -d air_quality_db -c "
  SELECT 
    s.name AS station,
    p.name AS pollutant,
    MAX(datetime) AS last_reading
  FROM air_quality_reading r
  JOIN station s ON r.station_id = s.id
  JOIN pollutant p ON r.pollutant_id = p.id
  GROUP BY s.name, p.name
  ORDER BY last_reading DESC
  LIMIT 20;
"
```

---

## 🔐 Seguridad

### Permisos Correctos

```bash
# Verificar permisos del directorio
ls -ld /opt/air-quality-ingestion
# Debe ser: drwxr-xr-x airquality airquality

# Verificar permisos de .env
ls -l /opt/air-quality-ingestion/.env
# Debe ser: -rw------- airquality airquality
```

### Variables Sensibles

**NUNCA** hagas commit de:
- `.env` con credenciales reales
- Tokens de API
- Contraseñas de base de datos

```bash
# Verificar que .env está en .gitignore
grep ".env" .gitignore
```

---

## 📚 Resumen de Comandos

| Acción | Comando |
|--------|---------|
| Actualizar código | `sudo ./deploy/update.sh` |
| Actualizar otra rama | `sudo ./deploy/update.sh --branch main` |
| Actualizar sin deps | `sudo ./deploy/update.sh --skip-deps` |
| Ver logs | `tail -f /var/log/air-quality-ingestion/ingestion.log` |
| Estado del servicio | `systemctl status air-quality-ingestion.timer` |
| Listar backups | `ls -lh /opt/air-quality-ingestion-backups/` |
| Ejecutar manual | `sudo -u airquality /opt/air-quality-ingestion/venv/bin/python -m app.main --mode realtime` |
| Restaurar backup | `sudo rsync -av --delete /opt/air-quality-ingestion-backups/BACKUP/ /opt/air-quality-ingestion/` |

---

## ✅ Checklist Post-Actualización

- [ ] Código actualizado sin errores
- [ ] Dependencias instaladas correctamente
- [ ] Timer systemd activo y running
- [ ] Logs no muestran errores críticos
- [ ] Lecturas nuevas aparecen en base de datos
- [ ] .env preservado con valores correctos
- [ ] Permisos de archivos correctos (600 para .env)
- [ ] Backup automático creado

---

**Última actualización:** 26 de noviembre de 2025  
**Compatibilidad:** Ubuntu 20.04+, Python 3.8+
