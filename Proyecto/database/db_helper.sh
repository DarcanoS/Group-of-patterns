#!/bin/bash
# Air Quality Platform - Database Connection Helper
# This script helps load environment variables and connect to the database

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
ENV_FILE="$SCRIPT_DIR/.env"

# Check if .env file exists
if [ ! -f "$ENV_FILE" ]; then
    echo -e "${RED}Error: .env file not found!${NC}"
    echo -e "${YELLOW}Please create it from .env.example:${NC}"
    echo "  cp .env.example .env"
    echo "  nano .env  # Edit with your credentials"
    exit 1
fi

# Load environment variables
set -a
source "$ENV_FILE"
set +a

echo -e "${GREEN}Environment variables loaded from .env${NC}"

# Function to connect as admin
connect_admin() {
    echo -e "${GREEN}Connecting as admin user...${NC}"
    podman exec -it "$POSTGRES_CONTAINER_NAME" psql -U "$DB_ADMIN_USER" -d "$DB_NAME"
}

# Function to connect as app user
connect_app() {
    echo -e "${GREEN}Connecting as application user...${NC}"
    podman exec -it "$POSTGRES_CONTAINER_NAME" psql -U "$DB_APP_USER" -d "$DB_NAME"
}

# Function to run a SQL script as admin
run_script_admin() {
    if [ -z "$1" ]; then
        echo -e "${RED}Error: Please provide a SQL script file${NC}"
        echo "Usage: $0 run-admin <script.sql>"
        exit 1
    fi
    
    if [ ! -f "$1" ]; then
        echo -e "${RED}Error: File '$1' not found${NC}"
        exit 1
    fi
    
    echo -e "${GREEN}Running $1 as admin user...${NC}"
    podman exec -i "$POSTGRES_CONTAINER_NAME" psql -U "$DB_ADMIN_USER" -d "$DB_NAME" < "$1"
}

# Function to run a SQL script as app user
run_script_app() {
    if [ -z "$1" ]; then
        echo -e "${RED}Error: Please provide a SQL script file${NC}"
        echo "Usage: $0 run-app <script.sql>"
        exit 1
    fi
    
    if [ ! -f "$1" ]; then
        echo -e "${RED}Error: File '$1' not found${NC}"
        exit 1
    fi
    
    echo -e "${GREEN}Running $1 as application user...${NC}"
    podman exec -i "$POSTGRES_CONTAINER_NAME" psql -U "$DB_APP_USER" -d "$DB_NAME" < "$1"
}

# Function to show connection info
show_info() {
    echo -e "${GREEN}=== Database Connection Information ===${NC}"
    echo ""
    echo "Container: $POSTGRES_CONTAINER_NAME"
    echo "Database: $DB_NAME"
    echo "Host: $DB_HOST"
    echo "Port: $DB_PORT"
    echo ""
    echo "Admin User: $DB_ADMIN_USER"
    echo "App User: $DB_APP_USER"
    echo ""
    echo -e "${YELLOW}Connection Strings:${NC}"
    echo "Admin: $DATABASE_URL_ADMIN"
    echo "App:   $DATABASE_URL"
}

# Main script logic
case "$1" in
    admin)
        connect_admin
        ;;
    app)
        connect_app
        ;;
    run-admin)
        run_script_admin "$2"
        ;;
    run-app)
        run_script_app "$2"
        ;;
    info)
        show_info
        ;;
    *)
        echo -e "${GREEN}Air Quality Platform - Database Helper${NC}"
        echo ""
        echo "Usage: $0 {admin|app|run-admin|run-app|info} [file]"
        echo ""
        echo "Commands:"
        echo "  admin              Connect to database as admin user"
        echo "  app                Connect to database as app user"
        echo "  run-admin <file>   Run SQL script as admin user"
        echo "  run-app <file>     Run SQL script as app user"
        echo "  info               Show connection information"
        echo ""
        echo "Examples:"
        echo "  $0 admin"
        echo "  $0 run-admin postgresql/init_schema.sql"
        echo "  $0 run-admin postgresql/seed_data.sql"
        echo "  $0 info"
        exit 1
        ;;
esac
