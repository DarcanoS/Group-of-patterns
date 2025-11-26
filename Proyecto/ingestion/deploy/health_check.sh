#!/bin/bash
# Air Quality Ingestion - Health Check Script
# Validates that the ingestion service is working properly

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

APP_DIR="/opt/air-quality-ingestion"
LOG_DIR="/var/log/air-quality-ingestion"

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Air Quality Ingestion - Health Check${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

CHECKS_PASSED=0
CHECKS_FAILED=0

# Function to check and report
check_item() {
    local name=$1
    local command=$2
    
    echo -n "Checking ${name}... "
    if eval ${command} > /dev/null 2>&1; then
        echo -e "${GREEN}✓ OK${NC}"
        ((CHECKS_PASSED++))
        return 0
    else
        echo -e "${RED}✗ FAILED${NC}"
        ((CHECKS_FAILED++))
        return 1
    fi
}

# 1. Check if app directory exists
check_item "App directory" "[ -d ${APP_DIR} ]"

# 2. Check if virtual environment exists
check_item "Virtual environment" "[ -d ${APP_DIR}/venv ]"

# 3. Check if .env file exists
check_item "Configuration file" "[ -f ${APP_DIR}/.env ]"

# 4. Check if log directory exists
check_item "Log directory" "[ -d ${LOG_DIR} ]"

# 5. Check if Python modules are importable
echo -n "Checking Python dependencies... "
if cd ${APP_DIR} && source venv/bin/activate && python -c "import app.main" 2>/dev/null; then
    echo -e "${GREEN}✓ OK${NC}"
    ((CHECKS_PASSED++))
else
    echo -e "${RED}✗ FAILED${NC}"
    ((CHECKS_FAILED++))
fi
deactivate 2>/dev/null || true

# 6. Check database connectivity
echo -n "Checking database connection... "
if cd ${APP_DIR} && source venv/bin/activate && python -c "
from app.db.session import engine
from sqlalchemy import text
with engine.connect() as conn:
    conn.execute(text('SELECT 1'))
" 2>/dev/null; then
    echo -e "${GREEN}✓ OK${NC}"
    ((CHECKS_PASSED++))
else
    echo -e "${RED}✗ FAILED${NC}"
    echo -e "${YELLOW}  Check DATABASE_URL in .env${NC}"
    ((CHECKS_FAILED++))
fi
deactivate 2>/dev/null || true

# 7. Check AQICN API token
echo -n "Checking AQICN API token... "
if grep -q "AQICN_TOKEN=demo" ${APP_DIR}/.env 2>/dev/null; then
    echo -e "${YELLOW}⚠ WARNING (using demo token)${NC}"
    ((CHECKS_PASSED++))
elif grep -q "AQICN_TOKEN=" ${APP_DIR}/.env 2>/dev/null; then
    echo -e "${GREEN}✓ OK${NC}"
    ((CHECKS_PASSED++))
else
    echo -e "${RED}✗ FAILED (not configured)${NC}"
    ((CHECKS_FAILED++))
fi

# 8. Check systemd timer (if exists)
if systemctl list-unit-files | grep -q "air-quality-ingestion.timer"; then
    check_item "Systemd timer enabled" "systemctl is-enabled air-quality-ingestion.timer"
    
    echo -n "Checking timer status... "
    if systemctl is-active air-quality-ingestion.timer > /dev/null 2>&1; then
        echo -e "${GREEN}✓ RUNNING${NC}"
        ((CHECKS_PASSED++))
    else
        echo -e "${YELLOW}⚠ INACTIVE${NC}"
        ((CHECKS_PASSED++))
    fi
fi

# 9. Check cron job (if exists)
echo -n "Checking cron job... "
if crontab -l 2>/dev/null | grep -q "air-quality-ingestion"; then
    echo -e "${GREEN}✓ CONFIGURED${NC}"
    ((CHECKS_PASSED++))
else
    echo -e "${YELLOW}⚠ NOT FOUND${NC}"
    echo -e "${YELLOW}  (May be using systemd instead)${NC}"
fi

# 10. Check recent logs
echo -n "Checking recent ingestion logs... "
if [ -f "${LOG_DIR}/ingestion.log" ]; then
    LOG_LINES=$(wc -l < ${LOG_DIR}/ingestion.log)
    RECENT_LOGS=$(tail -n 100 ${LOG_DIR}/ingestion.log 2>/dev/null | grep -i "success\|inserted\|fetched" | wc -l)
    
    if [ ${RECENT_LOGS} -gt 0 ]; then
        echo -e "${GREEN}✓ OK (${RECENT_LOGS} recent entries, ${LOG_LINES} total)${NC}"
        ((CHECKS_PASSED++))
    else
        echo -e "${YELLOW}⚠ NO RECENT ACTIVITY${NC}"
        ((CHECKS_PASSED++))
    fi
else
    echo -e "${YELLOW}⚠ NO LOGS YET${NC}"
fi

# 11. Check for errors in logs
echo -n "Checking for recent errors... "
if [ -f "${LOG_DIR}/error.log" ]; then
    RECENT_ERRORS=$(tail -n 100 ${LOG_DIR}/error.log 2>/dev/null | grep -i "error\|exception\|failed" | wc -l)
    
    if [ ${RECENT_ERRORS} -eq 0 ]; then
        echo -e "${GREEN}✓ NO ERRORS${NC}"
        ((CHECKS_PASSED++))
    else
        echo -e "${RED}✗ ${RECENT_ERRORS} ERRORS FOUND${NC}"
        echo -e "${YELLOW}  Run: tail -50 ${LOG_DIR}/error.log${NC}"
        ((CHECKS_FAILED++))
    fi
else
    echo -e "${GREEN}✓ NO ERROR LOG${NC}"
    ((CHECKS_PASSED++))
fi

# Summary
echo ""
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Summary${NC}"
echo -e "${BLUE}========================================${NC}"
echo -e "Checks passed: ${GREEN}${CHECKS_PASSED}${NC}"
echo -e "Checks failed: ${RED}${CHECKS_FAILED}${NC}"

if [ ${CHECKS_FAILED} -eq 0 ]; then
    echo ""
    echo -e "${GREEN}✓ All checks passed! Service is healthy.${NC}"
    exit 0
else
    echo ""
    echo -e "${RED}✗ Some checks failed. Please review.${NC}"
    exit 1
fi
