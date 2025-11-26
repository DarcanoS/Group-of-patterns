#!/bin/bash
# Script para Resetear Contenedores de Air Quality Platform
# Elimina contenedores, volúmenes y recrea todo con credenciales del archivo .env

set -e  # Salir en caso de error

# Colores
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

# Mensajes
print_info() { echo -e "${BLUE}ℹ${NC} $1"; }
print_success() { echo -e "${GREEN}✓${NC} $1"; }
print_warning() { echo -e "${YELLOW}⚠${NC} $1"; }
print_error() { echo -e "${RED}✗${NC} $1"; }
print_header() {
    echo ""
    echo -e "${BLUE}═══════════════════════════════════════════════${NC}"
    echo -e "${BLUE}  $1${NC}"
    echo -e "${BLUE}═══════════════════════════════════════════════${NC}"
    echo ""
}

# Detectar motor (podman o docker)
ENGINE="podman"
if [[ "$1" == "docker" ]]; then
    ENGINE="docker"
    COMPOSE_CMD="docker-compose"
else
    COMPOSE_CMD="podman-compose"
fi

# Directorio del script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Verificar que existe .env
if [ ! -f ".env" ]; then
    print_error "Archivo .env no encontrado!"
    echo ""
    echo "Copia el archivo de ejemplo y edítalo con tus credenciales:"
    echo "  cp .env.containers.example .env"
    echo "  nano .env"
    exit 1
fi

# Mostrar advertencia
print_header "RESETEO COMPLETO DE CONTENEDORES"
print_warning "Este script va a:"
echo "  1. Detener todos los contenedores"
echo "  2. Eliminar contenedores existentes"
echo "  3. Eliminar TODOS los volúmenes y DATOS"
echo "  4. Recrear contenedores con credenciales del .env"
echo ""
print_error "⚠️  TODOS LOS DATOS ACTUALES SE PERDERÁN ⚠️"
echo ""
read -p "¿Estás seguro de continuar? (escribe 'SI' para confirmar): " confirmacion

if [[ "$confirmacion" != "SI" ]]; then
    print_info "Operación cancelada"
    exit 0
fi

# Paso 1: Detener contenedores
print_header "Paso 1: Deteniendo contenedores"
if $ENGINE ps -q --filter "name=air-quality" | grep -q .; then
    print_info "Deteniendo contenedores air-quality..."
    $ENGINE stop $(podman ps -q --filter "name=air-quality") 2>/dev/null || true
    print_success "Contenedores detenidos"
else
    print_info "No hay contenedores corriendo"
fi

# Paso 2: Eliminar contenedores
print_header "Paso 2: Eliminando contenedores"
if $ENGINE ps -a -q --filter "name=air-quality" | grep -q .; then
    print_info "Eliminando contenedores air-quality..."
    $ENGINE rm -f $(podman ps -a -q --filter "name=air-quality") 2>/dev/null || true
    print_success "Contenedores eliminados"
else
    print_info "No hay contenedores que eliminar"
fi

# Paso 3: Eliminar volúmenes
print_header "Paso 3: Eliminando volúmenes"
volumes=("air-quality-postgis-data" "air-quality-mongodb-data" "air-quality-mongodb-config")
for vol in "${volumes[@]}"; do
    if $ENGINE volume ls -q | grep -q "^${vol}$"; then
        print_info "Eliminando volumen $vol..."
        $ENGINE volume rm "$vol" 2>/dev/null || true
        print_success "Volumen $vol eliminado"
    fi
done

# Paso 4: Eliminar red
print_header "Paso 4: Eliminando red"
if $ENGINE network ls -q --filter "name=air-quality-network" | grep -q .; then
    print_info "Eliminando red air-quality-network..."
    $ENGINE network rm air-quality-network 2>/dev/null || true
    print_success "Red eliminada"
else
    print_info "Red no existe"
fi

# Paso 5: Verificar limpieza
print_header "Paso 5: Verificando limpieza"
if $ENGINE ps -a -q --filter "name=air-quality" | grep -q .; then
    print_warning "Aún existen contenedores air-quality"
else
    print_success "No quedan contenedores air-quality"
fi

if $ENGINE volume ls -q | grep -q "air-quality"; then
    print_warning "Aún existen volúmenes air-quality"
else
    print_success "No quedan volúmenes air-quality"
fi

# Paso 6: Mostrar credenciales que se usarán
print_header "Paso 6: Credenciales a usar"
source .env
echo "PostgreSQL:"
echo "  Usuario Admin: ${DB_ADMIN_USER}"
echo "  Password Admin: ${DB_ADMIN_PASSWORD}"
echo "  Puerto: ${POSTGRES_PORT}"
echo ""
echo "MongoDB:"
echo "  Usuario Root: ${MONGO_ROOT_USER}"
echo "  Password Root: ${MONGO_ROOT_PASSWORD}"
echo "  Puerto: ${MONGO_PORT}"
echo ""

read -p "¿Las credenciales son correctas? (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    print_info "Edita el archivo .env antes de continuar"
    echo "  nano .env"
    exit 0
fi

# Paso 7: Recrear contenedores
print_header "Paso 7: Recreando contenedores"
print_info "Iniciando contenedores con $COMPOSE_CMD..."
if [ "$ENGINE" == "docker" ]; then
    $COMPOSE_CMD -f docker-compose.yml up -d
else
    $COMPOSE_CMD -f podman-compose.yml up -d
fi
print_success "Contenedores iniciados"

# Paso 8: Esperar a que estén listos
print_header "Paso 8: Esperando inicialización"
print_info "Esperando 10 segundos para que los servicios inicien..."
sleep 10

# Paso 9: Verificar salud
print_header "Paso 9: Verificando salud de contenedores"

# PostgreSQL
if $ENGINE exec air-quality-postgis pg_isready -U air_quality_admin -d air_quality_db &>/dev/null; then
    print_success "PostgreSQL: Listo y aceptando conexiones"
else
    print_warning "PostgreSQL: Aún no está listo (puede tomar 30-60 segundos)"
fi

# MongoDB
if $ENGINE exec air-quality-mongodb mongosh --eval "db.adminCommand('ping')" &>/dev/null; then
    print_success "MongoDB: Listo y aceptando conexiones"
else
    print_warning "MongoDB: Aún no está listo (puede tomar 30-60 segundos)"
fi

# Paso 10: Mostrar información de conexión
print_header "Paso 10: Información de Conexión"
echo "PostgreSQL:"
echo "  Comando: $ENGINE exec -it air-quality-postgis psql -U air_quality_admin -d air_quality_db"
echo "  Desde host: psql -h localhost -p ${POSTGRES_PORT} -U air_quality_admin -d air_quality_db"
echo ""
echo "MongoDB:"
echo "  Comando: $ENGINE exec -it air-quality-mongodb mongosh -u root -p"
echo "  Desde host: mongosh \"mongodb://root:${MONGO_ROOT_PASSWORD}@localhost:${MONGO_PORT}\""
echo ""

print_success "¡Reseteo completo! Los contenedores están listos."
echo ""
print_info "Para ver el estado:"
echo "  ./containers.sh status $ENGINE"
echo ""
print_info "Para ver logs:"
echo "  ./containers.sh logs all $ENGINE"
