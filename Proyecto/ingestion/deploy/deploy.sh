#!/bin/bash
# Air Quality Platform - Ingestion Service Deployment Script
# Deploy to Ubuntu Server

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}======================================${NC}"
echo -e "${GREEN}Air Quality Ingestion - Deployment${NC}"
echo -e "${GREEN}======================================${NC}"
echo ""

# Check if running as root
if [ "$EUID" -eq 0 ]; then 
   echo -e "${RED}Error: Do not run this script as root${NC}"
   echo "Run as regular user with sudo privileges"
   exit 1
fi

# Variables
APP_USER="${USER}"
APP_DIR="/opt/air-quality-ingestion"
LOG_DIR="/var/log/air-quality-ingestion"
SERVICE_NAME="air-quality-ingestion"

echo -e "${YELLOW}Configuration:${NC}"
echo "  App User: ${APP_USER}"
echo "  App Directory: ${APP_DIR}"
echo "  Log Directory: ${LOG_DIR}"
echo ""

# Step 1: Update system and install dependencies
echo -e "${GREEN}[1/8] Installing system dependencies...${NC}"
sudo apt-get update
sudo apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    postgresql-client \
    git \
    cron

# Step 2: Create directories
echo -e "${GREEN}[2/8] Creating directories...${NC}"
sudo mkdir -p ${APP_DIR}
sudo mkdir -p ${LOG_DIR}
sudo chown ${APP_USER}:${APP_USER} ${APP_DIR}
sudo chown ${APP_USER}:${APP_USER} ${LOG_DIR}

# Step 3: Copy application files
echo -e "${GREEN}[3/8] Copying application files...${NC}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cp -r ${SCRIPT_DIR}/app ${APP_DIR}/
cp -r ${SCRIPT_DIR}/data ${APP_DIR}/
cp ${SCRIPT_DIR}/requirements.txt ${APP_DIR}/
cp ${SCRIPT_DIR}/.env.example ${APP_DIR}/.env

echo "Files copied to ${APP_DIR}"

# Step 4: Create Python virtual environment
echo -e "${GREEN}[4/8] Creating Python virtual environment...${NC}"
cd ${APP_DIR}
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
deactivate

# Step 5: Configure environment variables
echo -e "${GREEN}[5/8] Configuring environment...${NC}"
if [ ! -f "${APP_DIR}/.env" ]; then
    cp ${APP_DIR}/.env.example ${APP_DIR}/.env
    echo -e "${YELLOW}⚠️  IMPORTANT: Edit ${APP_DIR}/.env with your configuration${NC}"
    echo -e "${YELLOW}   Especially: DATABASE_URL and AQICN_TOKEN${NC}"
fi

# Step 6: Set permissions
echo -e "${GREEN}[6/8] Setting permissions...${NC}"
chmod +x ${APP_DIR}/app/main.py
chmod 600 ${APP_DIR}/.env  # Protect sensitive config

# Step 7: Test installation
echo -e "${GREEN}[7/8] Testing installation...${NC}"
cd ${APP_DIR}
source venv/bin/activate
python -m app.main --help > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Installation test passed${NC}"
else
    echo -e "${RED}✗ Installation test failed${NC}"
    exit 1
fi
deactivate

# Step 8: Setup automation (ask user)
echo ""
echo -e "${GREEN}[8/8] Setup automation${NC}"
echo "Choose automation method:"
echo "  1) Systemd Timer (recommended)"
echo "  2) Cron Job (simpler)"
echo "  3) Skip (manual setup later)"
read -p "Enter choice [1-3]: " choice

case $choice in
    1)
        echo "Setting up systemd timer..."
        bash ${SCRIPT_DIR}/deploy/setup_systemd.sh
        ;;
    2)
        echo "Setting up cron job..."
        bash ${SCRIPT_DIR}/deploy/setup_cron.sh
        ;;
    3)
        echo "Skipping automation setup"
        ;;
    *)
        echo "Invalid choice, skipping automation setup"
        ;;
esac

echo ""
echo -e "${GREEN}======================================${NC}"
echo -e "${GREEN}✓ Deployment Complete!${NC}"
echo -e "${GREEN}======================================${NC}"
echo ""
echo "Next steps:"
echo "1. Edit configuration: nano ${APP_DIR}/.env"
echo "2. Test ingestion: cd ${APP_DIR} && source venv/bin/activate && python -m app.main --mode historical"
echo "3. Check logs: tail -f ${LOG_DIR}/ingestion.log"
echo ""
echo "For more info, see: ${SCRIPT_DIR}/README_DEPLOYMENT.md"
