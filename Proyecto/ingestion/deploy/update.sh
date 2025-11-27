#!/bin/bash

###############################################################################
# UPDATE SCRIPT - Air Quality Ingestion Service
#
# Este script actualiza el código de ingestion en /opt/air-quality-ingestion
# desde el repositorio Git más reciente.
#
# Uso:
#   ./deploy/update.sh
#   ./deploy/update.sh --branch develop
#   ./deploy/update.sh --skip-deps
###############################################################################

set -e  # Exit on error

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Default values
INSTALL_DIR="/opt/air-quality-ingestion"
REPO_URL="https://github.com/DarcanoS/Group-of-patterns.git"
BRANCH="develop"
SKIP_DEPS=false
BACKUP_DIR="/opt/air-quality-ingestion-backups"

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --branch)
            BRANCH="$2"
            shift 2
            ;;
        --skip-deps)
            SKIP_DEPS=true
            shift
            ;;
        --help)
            echo "Uso: $0 [OPTIONS]"
            echo ""
            echo "Opciones:"
            echo "  --branch BRANCH    Rama a actualizar (default: develop)"
            echo "  --skip-deps        Omitir instalación de dependencias"
            echo "  --help             Mostrar esta ayuda"
            exit 0
            ;;
        *)
            echo -e "${RED}Opción desconocida: $1${NC}"
            exit 1
            ;;
    esac
done

###############################################################################
# FUNCTIONS
###############################################################################

print_header() {
    echo -e "${BLUE}===============================================================================${NC}"
    echo -e "${BLUE}  $1${NC}"
    echo -e "${BLUE}===============================================================================${NC}"
}

print_step() {
    echo -e "\n${GREEN}[PASO $1/$2]${NC} $3"
    echo -e "${YELLOW}───────────────────────────────────────────────────────────────────────────${NC}"
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

check_root() {
    if [[ $EUID -ne 0 ]]; then
        print_error "Este script debe ejecutarse como root (sudo)"
        exit 1
    fi
}

###############################################################################
# MAIN SCRIPT
###############################################################################

print_header "UPDATE - Air Quality Ingestion Service"

echo -e "Configuración:"
echo -e "  Directorio: ${BLUE}$INSTALL_DIR${NC}"
echo -e "  Rama:       ${BLUE}$BRANCH${NC}"
echo -e "  Skip deps:  ${BLUE}$SKIP_DEPS${NC}"
echo ""

# Check root
check_root

# Verificar que existe la instalación
if [ ! -d "$INSTALL_DIR" ]; then
    print_error "Directorio $INSTALL_DIR no existe"
    echo "Por favor ejecuta primero: ./deploy/deploy.sh"
    exit 1
fi

TOTAL_STEPS=7
CURRENT_STEP=1

###############################################################################
print_step $CURRENT_STEP $TOTAL_STEPS "Detener servicio (si está corriendo)"
###############################################################################

if systemctl is-active --quiet air-quality-ingestion.timer 2>/dev/null; then
    systemctl stop air-quality-ingestion.timer
    print_success "Timer detenido"
fi

if systemctl is-active --quiet air-quality-ingestion.service 2>/dev/null; then
    systemctl stop air-quality-ingestion.service
    print_success "Service detenido"
fi

CURRENT_STEP=$((CURRENT_STEP + 1))

###############################################################################
print_step $CURRENT_STEP $TOTAL_STEPS "Crear backup del código actual"
###############################################################################

# Crear directorio de backups
mkdir -p "$BACKUP_DIR"

# Nombre del backup con timestamp
BACKUP_NAME="backup-$(date +%Y%m%d-%H%M%S)"
BACKUP_PATH="$BACKUP_DIR/$BACKUP_NAME"

print_warning "Creando backup en: $BACKUP_PATH"

# Copiar código (excluyendo venv y __pycache__)
rsync -a \
    --exclude 'venv/' \
    --exclude '__pycache__/' \
    --exclude '*.pyc' \
    --exclude '.env' \
    "$INSTALL_DIR/" "$BACKUP_PATH/"

print_success "Backup creado"

# Mantener solo últimos 5 backups
cd "$BACKUP_DIR"
ls -t | tail -n +6 | xargs -r rm -rf
print_success "Backups antiguos limpiados (manteniendo últimos 5)"

CURRENT_STEP=$((CURRENT_STEP + 1))

###############################################################################
print_step $CURRENT_STEP $TOTAL_STEPS "Clonar código actualizado desde Git"
###############################################################################

TMP_DIR="/tmp/air-quality-update-$$"
mkdir -p "$TMP_DIR"

cd "$TMP_DIR"
print_warning "Clonando rama '$BRANCH' desde $REPO_URL"

git clone --branch "$BRANCH" --depth 1 "$REPO_URL" repo

if [ $? -eq 0 ]; then
    print_success "Repositorio clonado"
else
    print_error "Error al clonar repositorio"
    exit 1
fi

CURRENT_STEP=$((CURRENT_STEP + 1))

###############################################################################
print_step $CURRENT_STEP $TOTAL_STEPS "Actualizar código en $INSTALL_DIR"
###############################################################################

SOURCE_DIR="$TMP_DIR/repo/Proyecto/ingestion"

if [ ! -d "$SOURCE_DIR" ]; then
    print_error "Directorio de ingestion no encontrado en el repositorio"
    exit 1
fi

# Copiar código nuevo (preservando .env y venv)
print_warning "Copiando archivos..."

rsync -a \
    --exclude 'venv/' \
    --exclude '.env' \
    --exclude '__pycache__/' \
    --exclude '*.pyc' \
    --delete \
    "$SOURCE_DIR/" "$INSTALL_DIR/"

print_success "Código actualizado"

# Limpiar temporal
rm -rf "$TMP_DIR"
print_success "Archivos temporales eliminados"

CURRENT_STEP=$((CURRENT_STEP + 1))

###############################################################################
print_step $CURRENT_STEP $TOTAL_STEPS "Actualizar dependencias Python"
###############################################################################

cd "$INSTALL_DIR"

if [ "$SKIP_DEPS" = true ]; then
    print_warning "Omitiendo actualización de dependencias (--skip-deps)"
else
    if [ -f "requirements.txt" ]; then
        print_warning "Instalando dependencias desde requirements.txt"
        
        source venv/bin/activate
        pip install --upgrade pip
        pip install -r requirements.txt
        deactivate
        
        print_success "Dependencias actualizadas"
    else
        print_error "requirements.txt no encontrado"
    fi
fi

CURRENT_STEP=$((CURRENT_STEP + 1))

###############################################################################
print_step $CURRENT_STEP $TOTAL_STEPS "Verificar permisos"
###############################################################################

# Asegurar que el usuario tenga permisos
if id "airquality" &>/dev/null; then
    chown -R airquality:airquality "$INSTALL_DIR"
    print_success "Permisos actualizados para usuario 'airquality'"
fi

# .env debe ser solo lectura para el usuario
if [ -f "$INSTALL_DIR/.env" ]; then
    chmod 600 "$INSTALL_DIR/.env"
    print_success "Permisos de .env configurados (600)"
fi

CURRENT_STEP=$((CURRENT_STEP + 1))

###############################################################################
print_step $CURRENT_STEP $TOTAL_STEPS "Reiniciar servicio"
###############################################################################

if systemctl is-enabled --quiet air-quality-ingestion.timer 2>/dev/null; then
    systemctl start air-quality-ingestion.timer
    print_success "Timer reiniciado"
    
    # Verificar estado
    if systemctl is-active --quiet air-quality-ingestion.timer; then
        print_success "Timer está activo"
    else
        print_warning "Timer no está activo, verificar manualmente"
    fi
else
    print_warning "Systemd timer no configurado, servicio no reiniciado"
fi

CURRENT_STEP=$((CURRENT_STEP + 1))

###############################################################################
print_header "ACTUALIZACIÓN COMPLETADA"
###############################################################################

echo ""
echo -e "${GREEN}✓ Código actualizado desde rama: $BRANCH${NC}"
echo -e "${GREEN}✓ Backup guardado en: $BACKUP_PATH${NC}"
echo ""
echo -e "${YELLOW}Próximos pasos:${NC}"
echo -e "  1. Verificar logs:  ${BLUE}tail -f /var/log/air-quality-ingestion/ingestion.log${NC}"
echo -e "  2. Ver estado:      ${BLUE}systemctl status air-quality-ingestion.timer${NC}"
echo -e "  3. Ejecutar manual: ${BLUE}sudo -u airquality /opt/air-quality-ingestion/venv/bin/python -m app.main --mode realtime${NC}"
echo ""

if [ "$SKIP_DEPS" = true ]; then
    echo -e "${YELLOW}⚠ ADVERTENCIA: Dependencias no actualizadas (--skip-deps)${NC}"
    echo -e "   Si hay nuevas dependencias, ejecuta:"
    echo -e "   ${BLUE}cd $INSTALL_DIR && source venv/bin/activate && pip install -r requirements.txt${NC}"
    echo ""
fi

print_header "Backup disponible en: $BACKUP_PATH"

echo ""
echo -e "${BLUE}Para restaurar el backup en caso de error:${NC}"
echo -e "  ${YELLOW}sudo systemctl stop air-quality-ingestion.timer${NC}"
echo -e "  ${YELLOW}sudo rsync -a --delete $BACKUP_PATH/ $INSTALL_DIR/${NC}"
echo -e "  ${YELLOW}sudo systemctl start air-quality-ingestion.timer${NC}"
echo ""

exit 0
