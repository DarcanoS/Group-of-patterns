#!/bin/bash
# Air Quality Platform - Container Management Script
# Manages PostgreSQL and MongoDB containers with Podman

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
POSTGRES_CONTAINER="air-quality-postgis"
MONGO_CONTAINER="air-quality-mongodb"
NETWORK_NAME="air-quality-network"

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

# Check if podman is installed
check_podman() {
    if ! command -v podman &> /dev/null; then
        print_error "Podman is not installed!"
        echo "  Install with: sudo apt install podman"
        exit 1
    fi
    print_success "Podman is installed"
}

# Check if podman-compose is available
check_compose() {
    if command -v podman-compose &> /dev/null; then
        COMPOSE_CMD="podman-compose"
        print_success "Using podman-compose"
    elif command -v docker-compose &> /dev/null; then
        COMPOSE_CMD="docker-compose"
        print_warning "Using docker-compose (podman-compose recommended)"
    else
        print_error "Neither podman-compose nor docker-compose found!"
        echo "  Install podman-compose with: pip3 install podman-compose"
        exit 1
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
    print_header "Starting Database Containers"
    
    cd "$SCRIPT_DIR"
    
    if [ -f "podman-compose.yml" ]; then
        print_info "Starting containers with $COMPOSE_CMD..."
        $COMPOSE_CMD -f podman-compose.yml up -d
        print_success "Containers started"
    else
        print_error "podman-compose.yml not found!"
        exit 1
    fi
    
    echo ""
    print_info "Waiting for containers to be healthy..."
    sleep 5
    
    check_health
}

# Stop containers
stop_containers() {
    print_header "Stopping Database Containers"
    
    cd "$SCRIPT_DIR"
    
    print_info "Stopping containers..."
    $COMPOSE_CMD -f podman-compose.yml down
    print_success "Containers stopped"
}

# Restart containers
restart_containers() {
    print_header "Restarting Database Containers"
    stop_containers
    sleep 2
    start_containers
}

# Check container health
check_health() {
    print_header "Container Health Status"
    
    # Check PostgreSQL
    if podman ps --filter "name=$POSTGRES_CONTAINER" --filter "status=running" | grep -q "$POSTGRES_CONTAINER"; then
        print_success "PostgreSQL: Running"
        
        # Test connection
        if podman exec $POSTGRES_CONTAINER pg_isready -U postgres &> /dev/null; then
            print_success "PostgreSQL: Ready to accept connections"
        else
            print_warning "PostgreSQL: Not ready yet"
        fi
    else
        print_error "PostgreSQL: Not running"
    fi
    
    echo ""
    
    # Check MongoDB
    if podman ps --filter "name=$MONGO_CONTAINER" --filter "status=running" | grep -q "$MONGO_CONTAINER"; then
        print_success "MongoDB: Running"
        
        # Test connection
        if podman exec $MONGO_CONTAINER mongosh --eval "db.adminCommand('ping')" &> /dev/null; then
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
    print_header "Container Status"
    
    podman ps -a --filter "name=$POSTGRES_CONTAINER" --filter "name=$MONGO_CONTAINER" \
        --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
}

# Show logs
show_logs() {
    local container=${1:-all}
    
    case $container in
        postgres|postgis)
            print_header "PostgreSQL Logs"
            podman logs --tail 50 -f $POSTGRES_CONTAINER
            ;;
        mongo|mongodb)
            print_header "MongoDB Logs"
            podman logs --tail 50 -f $MONGO_CONTAINER
            ;;
        all)
            print_header "All Container Logs"
            cd "$SCRIPT_DIR"
            $COMPOSE_CMD -f podman-compose.yml logs -f
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
    print_info "Connecting to PostgreSQL as postgres user..."
    podman exec -it $POSTGRES_CONTAINER psql -U postgres -d air_quality_db
}

# Connect to MongoDB
connect_mongo() {
    print_info "Connecting to MongoDB as root user..."
    podman exec -it $MONGO_CONTAINER mongosh -u root -p
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
    print_header "Cleanup - Remove Containers and Volumes"
    
    read -p "This will DELETE all data! Continue? (y/N): " -n 1 -r
    echo
    
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        cd "$SCRIPT_DIR"
        
        print_info "Stopping and removing containers..."
        $COMPOSE_CMD -f podman-compose.yml down -v
        
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
  start           Start database containers
  stop            Stop database containers
  restart         Restart database containers
  status          Show container status
  health          Check container health
  logs [NAME]     Show container logs (postgres, mongo, or all)
  
  psql            Connect to PostgreSQL
  mongo           Connect to MongoDB
  
  info            Show connection information
  cleanup         Remove containers and volumes (DELETES DATA!)
  
  help            Show this help message

Examples:
  $0 start                # Start all containers
  $0 logs postgres        # Show PostgreSQL logs
  $0 psql                 # Connect to PostgreSQL
  $0 cleanup              # Remove everything (with confirmation)

EOF
}

# Main script logic
main() {
    check_podman
    check_compose
    
    case "${1:-help}" in
        start)
            load_env
            start_containers
            ;;
        stop)
            stop_containers
            ;;
        restart)
            load_env
            restart_containers
            ;;
        status)
            show_status
            ;;
        health)
            check_health
            ;;
        logs)
            show_logs "${2:-all}"
            ;;
        psql|postgres)
            connect_postgres
            ;;
        mongo|mongodb)
            connect_mongo
            ;;
        info)
            show_info
            ;;
        cleanup)
            cleanup
            ;;
        help|--help|-h)
            show_help
            ;;
        *)
            print_error "Unknown command: $1"
            echo ""
            show_help
            exit 1
            ;;
    esac
}

# Run main function
main "$@"
