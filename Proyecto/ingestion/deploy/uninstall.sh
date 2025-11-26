#!/bin/bash
# Air Quality Ingestion - Uninstall Script

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${YELLOW}========================================${NC}"
echo -e "${YELLOW}Air Quality Ingestion - Uninstall${NC}"
echo -e "${YELLOW}========================================${NC}"
echo ""

APP_DIR="/opt/air-quality-ingestion"
LOG_DIR="/var/log/air-quality-ingestion"

echo -e "${RED}WARNING: This will remove:${NC}"
echo "  - Application files: ${APP_DIR}"
echo "  - Log files: ${LOG_DIR}"
echo "  - Systemd timer/service"
echo "  - Cron jobs"
echo ""
read -p "Are you sure you want to continue? (yes/no): " confirm

if [ "$confirm" != "yes" ]; then
    echo "Uninstall cancelled."
    exit 0
fi

# Stop and disable systemd timer
if systemctl list-unit-files | grep -q "air-quality-ingestion.timer"; then
    echo "Stopping systemd timer..."
    sudo systemctl stop air-quality-ingestion.timer 2>/dev/null || true
    sudo systemctl disable air-quality-ingestion.timer 2>/dev/null || true
    sudo rm -f /etc/systemd/system/air-quality-ingestion.timer
    sudo rm -f /etc/systemd/system/air-quality-ingestion.service
    sudo systemctl daemon-reload
    echo -e "${GREEN}✓ Systemd timer removed${NC}"
fi

# Remove cron jobs
if crontab -l 2>/dev/null | grep -q "air-quality-ingestion"; then
    echo "Removing cron job..."
    crontab -l 2>/dev/null | grep -v "air-quality-ingestion" | crontab -
    echo -e "${GREEN}✓ Cron job removed${NC}"
fi

# Remove application directory
if [ -d "${APP_DIR}" ]; then
    read -p "Remove application directory ${APP_DIR}? (yes/no): " rm_app
    if [ "$rm_app" = "yes" ]; then
        sudo rm -rf ${APP_DIR}
        echo -e "${GREEN}✓ Application directory removed${NC}"
    fi
fi

# Remove log directory
if [ -d "${LOG_DIR}" ]; then
    read -p "Remove log directory ${LOG_DIR}? (yes/no): " rm_logs
    if [ "$rm_logs" = "yes" ]; then
        sudo rm -rf ${LOG_DIR}
        echo -e "${GREEN}✓ Log directory removed${NC}"
    fi
fi

echo ""
echo -e "${GREEN}Uninstall complete!${NC}"
