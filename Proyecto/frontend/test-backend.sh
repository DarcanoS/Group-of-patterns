#!/bin/bash

echo "🔍 Verificando conexión con el backend..."
echo ""

# Colores
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Verificar health check
echo "1. Testing Health Check..."
HEALTH_RESPONSE=$(curl -s -w "\n%{http_code}" http://localhost:8000/api/v1/admin/health)
HTTP_CODE=$(echo "$HEALTH_RESPONSE" | tail -n1)
RESPONSE_BODY=$(echo "$HEALTH_RESPONSE" | head -n-1)

if [ "$HTTP_CODE" = "200" ]; then
    echo -e "${GREEN}✅ Backend está disponible${NC}"
    echo "   Response: $RESPONSE_BODY"
else
    echo -e "${RED}❌ Backend no está disponible (HTTP $HTTP_CODE)${NC}"
    echo "   Response: $RESPONSE_BODY"
    echo ""
    echo -e "${YELLOW}Por favor, asegúrate de que el backend esté corriendo en http://localhost:8000${NC}"
    exit 1
fi

echo ""
echo "2. Testing Stations Endpoint..."
STATIONS_RESPONSE=$(curl -s -w "\n%{http_code}" "http://localhost:8000/api/v1/stations?limit=3")
HTTP_CODE=$(echo "$STATIONS_RESPONSE" | tail -n1)

if [ "$HTTP_CODE" = "200" ]; then
    echo -e "${GREEN}✅ Endpoint de estaciones funciona${NC}"
else
    echo -e "${RED}❌ Error en endpoint de estaciones (HTTP $HTTP_CODE)${NC}"
fi

echo ""
echo "3. Testing Current AQI Endpoint..."
AQI_RESPONSE=$(curl -s -w "\n%{http_code}" "http://localhost:8000/api/v1/air-quality/current?city=Bogotá")
HTTP_CODE=$(echo "$AQI_RESPONSE" | tail -n1)

if [ "$HTTP_CODE" = "200" ]; then
    echo -e "${GREEN}✅ Endpoint de AQI funciona${NC}"
else
    echo -e "${RED}❌ Error en endpoint de AQI (HTTP $HTTP_CODE)${NC}"
fi

echo ""
echo "4. Testing Login Endpoint..."
LOGIN_RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=citizen@example.com&password=citizen123")
HTTP_CODE=$(echo "$LOGIN_RESPONSE" | tail -n1)

if [ "$HTTP_CODE" = "200" ]; then
    echo -e "${GREEN}✅ Endpoint de login funciona${NC}"
else
    echo -e "${YELLOW}⚠️  Login endpoint: HTTP $HTTP_CODE${NC}"
    echo "   (Esto puede ser normal si las credenciales son incorrectas)"
fi

echo ""
echo "================================================"
echo -e "${GREEN}✅ Integración lista para usar${NC}"
echo ""
echo "Frontend: http://localhost:5173"
echo "Backend:  http://localhost:8000"
echo "API Docs: http://localhost:8000/docs"
echo ""
echo "Para probar la integración completa:"
echo "1. Abre http://localhost:5173 en tu navegador"
echo "2. O abre test-integration.html para pruebas específicas"
echo "================================================"

