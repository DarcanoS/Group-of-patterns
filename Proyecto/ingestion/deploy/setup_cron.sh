#!/bin/bash
# Setup cron job for Air Quality Ingestion Service

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}Setting up Cron Job...${NC}"

APP_DIR="/opt/air-quality-ingestion"
LOG_DIR="/var/log/air-quality-ingestion"
APP_USER="${USER}"

# Create cron job script
CRON_SCRIPT="${APP_DIR}/run_ingestion.sh"

echo "Creating ingestion script..."
cat > ${CRON_SCRIPT} <<'EOF'
#!/bin/bash
# Air Quality Ingestion - Cron Runner

APP_DIR="/opt/air-quality-ingestion"
LOG_DIR="/var/log/air-quality-ingestion"

# Activate virtual environment
cd ${APP_DIR}
source venv/bin/activate

# Run ingestion (realtime mode)
python -m app.main --mode realtime >> ${LOG_DIR}/ingestion.log 2>> ${LOG_DIR}/error.log

# Exit with the same code as the ingestion
exit $?
EOF

chmod +x ${CRON_SCRIPT}

# Add to crontab
echo "Configuring crontab..."

# Check if cron job already exists
if crontab -l 2>/dev/null | grep -q "air-quality-ingestion"; then
    echo -e "${YELLOW}Cron job already exists, updating...${NC}"
    # Remove old entry
    crontab -l 2>/dev/null | grep -v "air-quality-ingestion" | crontab -
fi

# Add new cron job (every 10 minutes)
(crontab -l 2>/dev/null; echo "# Air Quality Ingestion - Run every 10 minutes") | crontab -
(crontab -l 2>/dev/null; echo "*/10 * * * * ${CRON_SCRIPT}") | crontab -

echo ""
echo -e "${GREEN}✓ Cron job configured successfully${NC}"
echo ""
echo "Cron schedule: Every 10 minutes"
echo "Script: ${CRON_SCRIPT}"
echo "Logs: ${LOG_DIR}/ingestion.log"
echo ""
echo "Current crontab:"
crontab -l | grep -A 1 "Air Quality"

echo ""
echo "Useful commands:"
echo "  View crontab:        crontab -l"
echo "  Edit crontab:        crontab -e"
echo "  View logs:           tail -f ${LOG_DIR}/ingestion.log"
echo "  View error logs:     tail -f ${LOG_DIR}/error.log"
echo "  Manual run:          ${CRON_SCRIPT}"
echo "  Remove cron job:     crontab -e (then delete the lines)"
