# 🔄 Instrucciones para Resetear Contenedores en el Servidor

## ✅ Resumen

Los contenedores ahora leen la configuración del archivo **`.env`** (no `.env.containers`).

---

## 📋 Pasos en el Servidor

### 1️⃣ Actualizar el Repositorio

```bash
cd ~/Proyecto/database
git pull origin develop
```

### 2️⃣ Configurar Credenciales

```bash
# Copiar plantilla
cp .env.example .env

# Editar con contraseñas SEGURAS
nano .env
```

**Cambia TODAS estas contraseñas:**
- `POSTGRES_PASSWORD`
- `MONGO_ROOT_PASSWORD`
- `DB_ADMIN_PASSWORD`
- `DB_APP_PASSWORD`
- `MONGO_APP_PASSWORD`

### 3️⃣ Eliminar Contenedores Viejos

**Opción A: Script Automatizado**
```bash
chmod +x reset_containers.sh
./reset_containers.sh podman
```

**Opción B: Manual**
```bash
# Detener y eliminar contenedores
./containers.sh clean podman

# Recrear con nuevas credenciales
./containers.sh up podman
```

### 4️⃣ Verificar

```bash
# Ver estado
./containers.sh status podman

# Probar conexión PostgreSQL
podman exec -it air-quality-postgis psql -U air_quality_admin -d air_quality_db

# Probar conexión MongoDB
podman exec -it air-quality-mongodb mongosh -u root -p
```

---

## 🔐 Seguridad

- ✅ El archivo `.env` está en `.gitignore` (no se hace commit)
- ✅ Usa contraseñas fuertes y únicas
- ✅ Guarda `.env` en un lugar seguro
- ❌ NUNCA compartas `.env` por chat/email

---

## 📞 Solución de Problemas

### Las contraseñas no funcionan
```bash
# Asegúrate de eliminar TODOS los volúmenes
podman volume ls | grep air-quality
podman volume rm air-quality-postgis-data air-quality-mongodb-data air-quality-mongodb-config

# Recrear contenedores
./containers.sh up podman
```

### Ver logs de error
```bash
./containers.sh logs postgres podman
./containers.sh logs mongo podman
```
