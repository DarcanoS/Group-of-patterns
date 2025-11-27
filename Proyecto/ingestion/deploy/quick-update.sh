#!/bin/bash

###############################################################################
# QUICK UPDATE - Air Quality Ingestion Service
#
# Este script descarga y ejecuta el update.sh directamente desde GitHub
# Útil cuando solo necesitas actualizar sin tener el repo completo
#
# Uso:
#   curl -fsSL https://raw.githubusercontent.com/DarcanoS/Group_of_patterns/develop/Proyecto/ingestion/deploy/quick-update.sh | sudo bash
#
#   O descargar primero:
#   wget https://raw.githubusercontent.com/DarcanoS/Group_of_patterns/develop/Proyecto/ingestion/deploy/quick-update.sh
#   chmod +x quick-update.sh
#   sudo ./quick-update.sh
###############################################################################

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# GitHub raw URL
REPO_RAW_URL="https://raw.githubusercontent.com/DarcanoS/Group_of_patterns/develop/Proyecto/ingestion/deploy"

echo -e "${BLUE}===============================================================================${NC}"
echo -e "${BLUE}  QUICK UPDATE - Air Quality Ingestion Service${NC}"
echo -e "${BLUE}===============================================================================${NC}"
echo ""

# Check root
if [[ $EUID -ne 0 ]]; then
    echo -e "${RED}✗ Este script debe ejecutarse como root (sudo)${NC}"
    exit 1
fi

# Verify installation exists
if [ ! -d "/opt/air-quality-ingestion" ]; then
    echo -e "${RED}✗ Instalación no encontrada en /opt/air-quality-ingestion${NC}"
    echo "   Por favor ejecuta primero el deployment inicial"
    exit 1
fi

# Download update script
TMP_SCRIPT="/tmp/air-quality-update-script-$$.sh"

echo -e "${YELLOW}Descargando script de actualización...${NC}"
curl -fsSL "$REPO_RAW_URL/update.sh" -o "$TMP_SCRIPT"

if [ $? -ne 0 ]; then
    echo -e "${RED}✗ Error descargando script de actualización${NC}"
    exit 1
fi

chmod +x "$TMP_SCRIPT"
echo -e "${GREEN}✓ Script descargado${NC}"
echo ""

# Execute
echo -e "${BLUE}Ejecutando actualización...${NC}"
echo ""

"$TMP_SCRIPT" "$@"

# Cleanup
rm -f "$TMP_SCRIPT"

echo ""
echo -e "${GREEN}✓ Actualización completada${NC}"
