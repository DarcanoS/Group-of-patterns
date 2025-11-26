#!/bin/bash
# Setup systemd timer for Air Quality Ingestion Service

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}Setting up Systemd Timer...${NC}"

APP_DIR="/opt/air-quality-ingestion"
APP_USER="${USER}"

# Check if systemd is available
if ! command -v systemctl &> /dev/null; then
    echo -e "${RED}Error: systemd not found${NC}"
    exit 1
fi

# Create service file
echo "Creating service file..."
sudo tee /etc/systemd/system/air-quality-ingestion.service > /dev/null <<EOF
[Unit]
Description=Air Quality Data Ingestion Service
After=network.target postgresql.service
Wants=postgresql.service

[Service]
Type=oneshot
User=${APP_USER}
WorkingDirectory=${APP_DIR}
Environment="PATH=${APP_DIR}/venv/bin"
ExecStart=${APP_DIR}/venv/bin/python -m app.main --mode realtime
StandardOutput=append:/var/log/air-quality-ingestion/ingestion.log
StandardError=append:/var/log/air-quality-ingestion/error.log

# Security
NoNewPrivileges=true
PrivateTmp=true

[Install]
WantedBy=multi-user.target
EOF

# Create timer file
echo "Creating timer file..."
sudo tee /etc/systemd/system/air-quality-ingestion.timer > /dev/null <<EOF
[Unit]
Description=Run Air Quality Ingestion every 10 minutes
Requires=air-quality-ingestion.service

[Timer]
# Run every 10 minutes
OnBootSec=2min
OnUnitActiveSec=10min
AccuracySec=1min

[Install]
WantedBy=timers.target
EOF

# Reload systemd
echo "Reloading systemd..."
sudo systemctl daemon-reload

# Enable and start timer
echo "Enabling timer..."
sudo systemctl enable air-quality-ingestion.timer
sudo systemctl start air-quality-ingestion.timer

echo ""
echo -e "${GREEN}✓ Systemd timer configured successfully${NC}"
echo ""
echo "Timer status:"
sudo systemctl status air-quality-ingestion.timer --no-pager

echo ""
echo "Useful commands:"
echo "  Check timer status:   sudo systemctl status air-quality-ingestion.timer"
echo "  Check service status: sudo systemctl status air-quality-ingestion.service"
echo "  View logs:           sudo journalctl -u air-quality-ingestion.service -f"
echo "  Manual run:          sudo systemctl start air-quality-ingestion.service"
echo "  Stop timer:          sudo systemctl stop air-quality-ingestion.timer"
echo "  Restart timer:       sudo systemctl restart air-quality-ingestion.timer"
