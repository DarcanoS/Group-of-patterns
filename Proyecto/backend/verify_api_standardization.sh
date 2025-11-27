#!/bin/bash

# Script de verificación de endpoints estandarizados
# Verifica que todos los endpoints funcionen con el prefijo /api/v1

echo "🔍 Verificando estandarización de API endpoints..."
echo "=================================================="
echo ""

BASE_URL="http://localhost:8000"
API_V1="/api/v1"

# Colores para output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Contador de tests
PASSED=0
FAILED=0

# Función para verificar endpoint
check_endpoint() {
    local method=$1
    local path=$2
    local description=$3
    local expected_status=${4:-200}

    echo -n "Testing: $description... "

    http_code=$(curl -s -o /dev/null -w "%{http_code}" -X $method "$BASE_URL$path")

    if [ "$http_code" == "$expected_status" ] || [ "$http_code" == "401" ] || [ "$http_code" == "403" ]; then
        echo -e "${GREEN}✓ PASS${NC} (HTTP $http_code)"
        ((PASSED++))
    else
        echo -e "${RED}✗ FAIL${NC} (HTTP $http_code, esperado $expected_status o 401/403)"
        ((FAILED++))
    fi
}

# Función para verificar que endpoint antiguo NO funcione
check_old_endpoint() {
    local path=$1
    local description=$2

    echo -n "Verificando endpoint antiguo: $description... "

    http_code=$(curl -s -o /dev/null -w "%{http_code}" "$BASE_URL$path")

    if [ "$http_code" == "404" ]; then
        echo -e "${GREEN}✓ PASS${NC} (correctamente retorna 404)"
        ((PASSED++))
    else
        echo -e "${RED}✗ FAIL${NC} (HTTP $http_code, debería ser 404)"
        ((FAILED++))
    fi
}

echo "1. Verificando endpoints raíz (sin /api/v1)..."
echo "----------------------------------------------"
check_endpoint "GET" "/" "Root endpoint" 200
check_endpoint "GET" "/health" "Health check básico" 200
echo ""

echo "2. Verificando que endpoints antiguos ya NO funcionen..."
echo "--------------------------------------------------------"
check_old_endpoint "/api/admin/health" "/api/admin/health"
check_old_endpoint "/api/stations" "/api/stations"
check_old_endpoint "/api/auth/login" "/api/auth/login"
echo ""

echo "3. Verificando endpoints nuevos con /api/v1..."
echo "----------------------------------------------"

# Authentication
echo "📝 Authentication:"
check_endpoint "GET" "$API_V1/auth/me" "GET /api/v1/auth/me" 401
echo ""

# Stations
echo "🏭 Stations:"
check_endpoint "GET" "$API_V1/stations" "GET /api/v1/stations"
check_endpoint "GET" "$API_V1/stations/1" "GET /api/v1/stations/1"
check_endpoint "GET" "$API_V1/stations/1/readings/current" "GET /api/v1/stations/1/readings/current"
echo ""

# Air Quality
echo "🌫️ Air Quality:"
check_endpoint "GET" "$API_V1/air-quality/dashboard?city=New%20York" "GET /api/v1/air-quality/dashboard"
echo ""

# Admin
echo "👔 Admin:"
check_endpoint "GET" "$API_V1/admin/health" "GET /api/v1/admin/health"
check_endpoint "GET" "$API_V1/admin/stations" "GET /api/v1/admin/stations" 403
echo ""

# Recommendations
echo "💡 Recommendations:"
check_endpoint "GET" "$API_V1/recommendations/current" "GET /api/v1/recommendations/current" 401
check_endpoint "GET" "$API_V1/recommendations/history" "GET /api/v1/recommendations/history" 401
echo ""

# Settings
echo "⚙️ Settings:"
check_endpoint "GET" "$API_V1/settings/preferences" "GET /api/v1/settings/preferences" 401
check_endpoint "GET" "$API_V1/settings/dashboard" "GET /api/v1/settings/dashboard" 401
echo ""

# Reports
echo "📊 Reports:"
check_endpoint "GET" "$API_V1/reports" "GET /api/v1/reports" 401
echo ""

echo "=================================================="
echo "Resumen de tests:"
echo "=================================================="
echo -e "${GREEN}✓ PASSED: $PASSED${NC}"
echo -e "${RED}✗ FAILED: $FAILED${NC}"
echo ""

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}🎉 ¡Todos los tests pasaron! La API está correctamente estandarizada.${NC}"
    echo ""
    echo "✅ Documentación disponible en:"
    echo "   - Swagger UI: $BASE_URL$API_V1/docs"
    echo "   - ReDoc: $BASE_URL$API_V1/redoc"
    echo "   - OpenAPI JSON: $BASE_URL$API_V1/openapi.json"
    exit 0
else
    echo -e "${RED}❌ Algunos tests fallaron. Revisa la configuración.${NC}"
    echo ""
    echo "Verifica que:"
    echo "  1. El servidor esté corriendo en el puerto 8000"
    echo "  2. El archivo .env tenga API_V1_STR=/api/v1"
    echo "  3. El servidor se haya reiniciado después de cambiar el .env"
    exit 1
fi

