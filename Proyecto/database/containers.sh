#!/bin/bash
# Air Quality Platform - Container Management Script
# Manages PostgreSQL and MongoDB containers with Podman or Docker

set -e  # Exit on error

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Container names
POSTGRES_CONTAINER="air_quality_postgres"
MONGO_CONTAINER="air_quality_mongo"
NETWORK_NAME="air_quality_network"

# Function to print colored messages
print_info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_header() {
    echo ""
    echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
    echo -e "${BLUE}  $1${NC}"
    echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
    echo ""
}

# Detect engine and compose file
detect_engine() {
    ENGINE="podman"
    COMPOSE_FILE="podman-compose.yml"
    COMPOSE_CMD="podman-compose"
    if [[ "$1" == "docker" ]]; then
        ENGINE="docker"
        COMPOSE_FILE="docker-compose.yml"
        if command -v docker-compose &> /dev/null; then
            COMPOSE_CMD="docker-compose"
            print_success "Using Docker Compose"
        else
            print_error "docker-compose not found! Install with: sudo apt install docker-compose"
            exit 1
        fi
    else
        if ! command -v podman &> /dev/null; then
            print_error "Podman is not installed! Install with: sudo apt install podman"
            exit 1
        fi
        if command -v podman-compose &> /dev/null; then
            COMPOSE_CMD="podman-compose"
            print_success "Using Podman Compose"
        else
            print_error "podman-compose not found! Install with: pip3 install podman-compose"
            exit 1
        fi
    fi
}

# Load environment variables
load_env() {
    if [ -f "$SCRIPT_DIR/.env.containers" ]; then
        export $(grep -v '^#' "$SCRIPT_DIR/.env.containers" | xargs)
        print_success "Loaded .env.containers"
    else
        print_warning ".env.containers not found, using defaults"
    fi
}

# Start containers
start_containers() {
    local engine="${1:-podman}"
    detect_engine "$engine"
    print_header "Starting Database Containers ($ENGINE)"
    cd "$SCRIPT_DIR"
    if [ -f "$COMPOSE_FILE" ]; then
        print_info "Starting containers with $COMPOSE_CMD ($COMPOSE_FILE)..."
        $COMPOSE_CMD -f "$COMPOSE_FILE" up -d
        print_success "Containers started"
    else
        print_error "$COMPOSE_FILE not found!"
        exit 1
    fi
    echo ""
    print_info "Waiting for containers to be healthy..."
    sleep 5
    check_health "$engine"
}

# Stop containers
stop_containers() {
    local engine="${1:-podman}"
    detect_engine "$engine"
    print_header "Stopping Database Containers ($ENGINE)"
    cd "$SCRIPT_DIR"
    print_info "Stopping containers..."
    $COMPOSE_CMD -f "$COMPOSE_FILE" down
    print_success "Containers stopped"
}

# Restart containers
restart_containers() {
    local engine="${1:-podman}"
    print_header "Restarting Database Containers ($engine)"
    stop_containers "$engine"
    sleep 2
    start_containers "$engine"
}

# Check container health
check_health() {
    local engine="${1:-podman}"
    detect_engine "$engine"
    print_header "Container Health Status ($ENGINE)"
    # Check PostgreSQL
    if $ENGINE ps --filter "name=$POSTGRES_CONTAINER" --filter "status=running" | grep -q "$POSTGRES_CONTAINER"; then
        print_success "PostgreSQL: Running"
        if $ENGINE exec $POSTGRES_CONTAINER pg_isready -U air_quality_admin -d air_quality_db &> /dev/null; then
            print_success "PostgreSQL: Ready to accept connections"
        else
            print_warning "PostgreSQL: Not ready yet"
        fi
    else
        print_error "PostgreSQL: Not running"
    fi
    echo ""
    # Check MongoDB
    if $ENGINE ps --filter "name=$MONGO_CONTAINER" --filter "status=running" | grep -q "$MONGO_CONTAINER"; then
        print_success "MongoDB: Running"
        if $ENGINE exec $MONGO_CONTAINER mongosh --eval "db.adminCommand('ping')" &> /dev/null; then
            print_success "MongoDB: Ready to accept connections"
        else
            print_warning "MongoDB: Not ready yet"
        fi
    else
        print_error "MongoDB: Not running"
    fi
}

# Show container status
show_status() {
    local engine="${1:-podman}"
    detect_engine "$engine"
    print_header "Container Status ($ENGINE)"
    $ENGINE ps -a --filter "name=$POSTGRES_CONTAINER" --filter "name=$MONGO_CONTAINER" \
        --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
}

# Show logs
show_logs() {
    local container=${1:-all}
    local engine="${2:-podman}"
    detect_engine "$engine"
    case $container in
        postgres|postgis)
            print_header "PostgreSQL Logs ($ENGINE)"
            $ENGINE logs --tail 50 -f $POSTGRES_CONTAINER
            ;;
        mongo|mongodb)
            print_header "MongoDB Logs ($ENGINE)"
            $ENGINE logs --tail 50 -f $MONGO_CONTAINER
            ;;
        all)
            print_header "All Container Logs ($ENGINE)"
            cd "$SCRIPT_DIR"
            $COMPOSE_CMD -f "$COMPOSE_FILE" logs -f
            ;;
        *)
            print_error "Unknown container: $container"
            echo "  Use: postgres, mongo, or all"
            exit 1
            ;;
    esac
}

# Connect to PostgreSQL
connect_postgres() {
    local engine="${1:-podman}"
    detect_engine "$engine"
    print_info "Connecting to PostgreSQL as air_quality_admin..."
    $ENGINE exec -it $POSTGRES_CONTAINER psql -U air_quality_admin -d air_quality_db
}

# Connect to MongoDB
connect_mongo() {
    local engine="${1:-podman}"
    detect_engine "$engine"
    print_info "Connecting to MongoDB as mongo_admin..."
    $ENGINE exec -it $MONGO_CONTAINER mongosh -u mongo_admin -p
}

# Show connection info
show_info() {
    load_env
    
    print_header "Database Connection Information"
    
    echo -e "${GREEN}PostgreSQL + PostGIS:${NC}"
    echo "  Host:     localhost"
    echo "  Port:     ${POSTGRES_PORT:-5433}"
    echo "  Database: air_quality_db"
    echo "  Admin:    air_quality_admin / admin_secure_password"
    echo "  App:      air_quality_app / app_secure_password"
    echo ""
    echo "  Connection (Admin):"
    echo "    psql -h localhost -p ${POSTGRES_PORT:-5433} -U air_quality_admin -d air_quality_db"
    echo ""
    echo "  Connection String (Admin):"
    echo "    ${DATABASE_URL_ADMIN}"
    echo ""
    echo "  Connection String (App):"
    echo "    ${DATABASE_URL}"
    
    echo ""
    echo -e "${GREEN}MongoDB:${NC}"
    echo "  Host:     localhost"
    echo "  Port:     ${MONGO_PORT:-27017}"
    echo "  Database: air_quality_config"
    echo "  Root:     root / mongo_secure_pass"
    echo "  App:      air_quality_user / secure_password"
    echo ""
    echo "  Connection:"
    echo "    mongosh -u root -p mongo_secure_pass"
    echo ""
    echo "  Connection String:"
    echo "    ${NOSQL_URI}"
}

# Clean up (remove containers and volumes)
cleanup() {
    local engine="${1:-podman}"
    detect_engine "$engine"
    print_header "Cleanup - Remove Containers and Volumes ($ENGINE)"
    read -p "This will DELETE all data! Continue? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        cd "$SCRIPT_DIR"
        print_info "Stopping and removing containers..."
        $COMPOSE_CMD -f "$COMPOSE_FILE" down -v
        print_success "Cleanup complete"
    else
        print_info "Cleanup cancelled"
    fi
}

# Show help
show_help() {
        cat << EOF
Air Quality Platform - Database Container Management

Usage: $0 <command> [options]

Commands:
    up [engine]         Start containers (engine: podman|docker)
    down [engine]       Stop containers
    restart [engine]    Restart containers
    status [engine]     Show container status
    health [engine]     Check container health
    logs [NAME] [engine] Show logs (postgres, mongo, all)
    psql [engine]       Connect to PostgreSQL
    mongo [engine]      Connect to MongoDB
    info                Show connection info
    clean [engine]      Remove containers and volumes (DELETES DATA!)
    help                Show this help message

Examples:
    $0 up podman            # Start with Podman
    $0 up docker            # Start with Docker
    $0 logs postgres docker # Show PostgreSQL logs (Docker)
    $0 psql podman          # Connect to PostgreSQL (Podman)
    $0 clean docker         # Remove everything (Docker)

EOF
}

# Main script logic
main() {
    cmd="${1:-help}"
    arg1="${2:-podman}"
    arg2="${3:-}"
    case "$cmd" in
        up|start)
            load_env
            start_containers "$arg1"
            ;;
        down|stop)
            stop_containers "$arg1"
            ;;
        restart)
            load_env
            restart_containers "$arg1"
            ;;
        status)
            show_status "$arg1"
            ;;
        health)
            check_health "$arg1"
            ;;
        logs)
            show_logs "$arg1" "$arg2"
            ;;
        psql|postgres)
            connect_postgres "$arg1"
            ;;
        mongo|mongodb)
            connect_mongo "$arg1"
            ;;
        info)
            show_info
            ;;
        clean|cleanup)
            cleanup "$arg1"
            ;;
        help|--help|-h)
            show_help
            ;;
        *)
            print_error "Unknown command: $cmd"
            echo ""
            show_help
            exit 1
            ;;
    esac
}

# Run main function
main "$@"
