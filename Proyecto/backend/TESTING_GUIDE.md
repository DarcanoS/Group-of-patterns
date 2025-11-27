# 🧪 Testing Guide - Postman & cURL Examples

Esta guía contiene ejemplos completos para probar todos los endpoints usando cURL o Postman.

---

## 🔧 Configuración Inicial

### Variables de Entorno
```bash
export API_URL="http://localhost:8000/api/v1"
export TOKEN=""  # Se llenará después del login
```

---

## 1️⃣ Authentication

### 1.1 Login

**cURL:**
```bash
curl -X POST "$API_URL/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=user@example.com&password=password123"
```

**Postman:**
- Method: `POST`
- URL: `{{API_URL}}/auth/login`
- Body (x-www-form-urlencoded):
  - `username`: `user@example.com`
  - `password`: `password123`

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "full_name": "John Doe",
    "role": {
      "id": 1,
      "name": "Citizen"
    }
  }
}
```

**Guardar el token:**
```bash
export TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

---

### 1.2 Get Current User

**cURL:**
```bash
curl -X GET "$API_URL/auth/me" \
  -H "Authorization: Bearer $TOKEN"
```

**Postman:**
- Method: `GET`
- URL: `{{API_URL}}/auth/me`
- Headers:
  - `Authorization`: `Bearer {{TOKEN}}`

---

## 2️⃣ Stations

### 2.1 List All Stations

**cURL:**
```bash
curl -X GET "$API_URL/stations?limit=10"
```

**Con filtros:**
```bash
curl -X GET "$API_URL/stations?city=New%20York&limit=10&skip=0"
```

**Postman:**
- Method: `GET`
- URL: `{{API_URL}}/stations`
- Params:
  - `city`: `New York`
  - `limit`: `10`
  - `skip`: `0`

---

### 2.2 Get Station by ID

**cURL:**
```bash
curl -X GET "$API_URL/stations/1"
```

**Postman:**
- Method: `GET`
- URL: `{{API_URL}}/stations/1`

---

### 2.3 Get Current Readings

**cURL:**
```bash
curl -X GET "$API_URL/stations/1/readings/current"
```

**Postman:**
- Method: `GET`
- URL: `{{API_URL}}/stations/1/readings/current`

---

## 3️⃣ Air Quality

### 3.1 Get Current AQI

**cURL:**
```bash
curl -X GET "$API_URL/air-quality/current?city=New%20York"
```

**Postman:**
- Method: `GET`
- URL: `{{API_URL}}/air-quality/current`
- Params:
  - `city`: `New York`

---

### 3.2 Get Dashboard Data

**Por ciudad:**
```bash
curl -X GET "$API_URL/air-quality/dashboard?city=New%20York"
```

**Por estación:**
```bash
curl -X GET "$API_URL/air-quality/dashboard?station_id=1"
```

**Postman:**
- Method: `GET`
- URL: `{{API_URL}}/air-quality/dashboard`
- Params:
  - `city`: `New York` (o `station_id`: `1`)

---

### 3.3 Get Daily Stats

**cURL:**
```bash
curl -X GET "$API_URL/air-quality/daily-stats?station_id=1&start_date=2025-11-01&end_date=2025-11-27&limit=30"
```

**Postman:**
- Method: `GET`
- URL: `{{API_URL}}/air-quality/daily-stats`
- Params:
  - `station_id`: `1`
  - `start_date`: `2025-11-01`
  - `end_date`: `2025-11-27`
  - `limit`: `30`

---

## 4️⃣ Recommendations

### 4.1 Get Current Recommendation

**cURL:**
```bash
curl -X GET "$API_URL/recommendations/current?location=New%20York" \
  -H "Authorization: Bearer $TOKEN"
```

**Con AQI específico:**
```bash
curl -X GET "$API_URL/recommendations/current?aqi=150" \
  -H "Authorization: Bearer $TOKEN"
```

**Postman:**
- Method: `GET`
- URL: `{{API_URL}}/recommendations/current`
- Headers:
  - `Authorization`: `Bearer {{TOKEN}}`
- Params:
  - `location`: `New York` (opcional)
  - `aqi`: `150` (opcional)

---

### 4.2 Get Recommendation History

**cURL:**
```bash
curl -X GET "$API_URL/recommendations/history?limit=10" \
  -H "Authorization: Bearer $TOKEN"
```

**Postman:**
- Method: `GET`
- URL: `{{API_URL}}/recommendations/history`
- Headers:
  - `Authorization`: `Bearer {{TOKEN}}`
- Params:
  - `limit`: `10`
  - `skip`: `0`

---

## 5️⃣ Admin Endpoints

### 5.1 Health Check

**cURL:**
```bash
curl -X GET "$API_URL/admin/health"
```

**Postman:**
- Method: `GET`
- URL: `{{API_URL}}/admin/health`

---

### 5.2 List Stations (Admin)

**cURL:**
```bash
curl -X GET "$API_URL/admin/stations?limit=20" \
  -H "Authorization: Bearer $TOKEN"
```

**Postman:**
- Method: `GET`
- URL: `{{API_URL}}/admin/stations`
- Headers:
  - `Authorization`: `Bearer {{TOKEN}}`
- Params:
  - `limit`: `20`

---

### 5.3 Create Station

**cURL:**
```bash
curl -X POST "$API_URL/admin/stations" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Brooklyn Air Monitor",
    "latitude": 40.6782,
    "longitude": -73.9442,
    "city": "Brooklyn",
    "country": "USA",
    "region_id": 1
  }'
```

**Postman:**
- Method: `POST`
- URL: `{{API_URL}}/admin/stations`
- Headers:
  - `Authorization`: `Bearer {{TOKEN}}`
  - `Content-Type`: `application/json`
- Body (raw JSON):
```json
{
  "name": "Brooklyn Air Monitor",
  "latitude": 40.6782,
  "longitude": -73.9442,
  "city": "Brooklyn",
  "country": "USA",
  "region_id": 1
}
```

---

### 5.4 Update Station

**cURL:**
```bash
curl -X PUT "$API_URL/admin/stations/1" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Updated Station Name",
    "is_active": false
  }'
```

**Postman:**
- Method: `PUT`
- URL: `{{API_URL}}/admin/stations/1`
- Headers:
  - `Authorization`: `Bearer {{TOKEN}}`
  - `Content-Type`: `application/json`
- Body (raw JSON):
```json
{
  "name": "Updated Station Name",
  "is_active": false
}
```

---

### 5.5 Delete Station

**cURL:**
```bash
curl -X DELETE "$API_URL/admin/stations/1" \
  -H "Authorization: Bearer $TOKEN"
```

**Postman:**
- Method: `DELETE`
- URL: `{{API_URL}}/admin/stations/1`
- Headers:
  - `Authorization`: `Bearer {{TOKEN}}`

---

### 5.6 List Users

**cURL:**
```bash
curl -X GET "$API_URL/admin/users?limit=20" \
  -H "Authorization: Bearer $TOKEN"
```

**Postman:**
- Method: `GET`
- URL: `{{API_URL}}/admin/users`
- Headers:
  - `Authorization`: `Bearer {{TOKEN}}`
- Params:
  - `limit`: `20`

---

### 5.7 Update User Role

**cURL:**
```bash
curl -X PUT "$API_URL/admin/users/2/role" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "role_id": 2
  }'
```

**Postman:**
- Method: `PUT`
- URL: `{{API_URL}}/admin/users/2/role`
- Headers:
  - `Authorization`: `Bearer {{TOKEN}}`
  - `Content-Type`: `application/json`
- Body (raw JSON):
```json
{
  "role_id": 2
}
```

---

## 6️⃣ Settings

### 6.1 Get User Preferences

**cURL:**
```bash
curl -X GET "$API_URL/settings/preferences" \
  -H "Authorization: Bearer $TOKEN"
```

**Postman:**
- Method: `GET`
- URL: `{{API_URL}}/settings/preferences`
- Headers:
  - `Authorization`: `Bearer {{TOKEN}}`

---

### 6.2 Update User Preferences

**cURL:**
```bash
curl -X PUT "$API_URL/settings/preferences" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "theme": "dark",
    "language": "es",
    "notifications_enabled": true,
    "aqi_threshold": 100
  }'
```

**Postman:**
- Method: `PUT`
- URL: `{{API_URL}}/settings/preferences`
- Headers:
  - `Authorization`: `Bearer {{TOKEN}}`
  - `Content-Type`: `application/json`
- Body (raw JSON):
```json
{
  "theme": "dark",
  "language": "es",
  "notifications_enabled": true,
  "email_alerts": true,
  "aqi_threshold": 100,
  "preferred_units": "metric"
}
```

---

### 6.3 Get Dashboard Config

**cURL:**
```bash
curl -X GET "$API_URL/settings/dashboard" \
  -H "Authorization: Bearer $TOKEN"
```

**Postman:**
- Method: `GET`
- URL: `{{API_URL}}/settings/dashboard`
- Headers:
  - `Authorization`: `Bearer {{TOKEN}}`

---

### 6.4 Update Dashboard Config

**cURL:**
```bash
curl -X PUT "$API_URL/settings/dashboard" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "widgets": [
      {
        "id": "aqi-gauge",
        "type": "gauge",
        "position": {"x": 0, "y": 0},
        "size": {"width": 3, "height": 2},
        "settings": {
          "show_history": true,
          "time_range": "48h"
        }
      }
    ],
    "layout": "flex",
    "refresh_interval": 180
  }'
```

**Postman:**
- Method: `PUT`
- URL: `{{API_URL}}/settings/dashboard`
- Headers:
  - `Authorization`: `Bearer {{TOKEN}}`
  - `Content-Type`: `application/json`
- Body (raw JSON):
```json
{
  "widgets": [
    {
      "id": "aqi-gauge",
      "type": "gauge",
      "position": {"x": 0, "y": 0},
      "size": {"width": 3, "height": 2},
      "settings": {
        "show_history": true,
        "time_range": "48h"
      }
    }
  ],
  "layout": "flex",
  "refresh_interval": 180
}
```

---

## 7️⃣ Reports

### 7.1 Create Report

**cURL:**
```bash
curl -X POST "$API_URL/reports" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "city": "New York",
    "start_date": "2025-11-01",
    "end_date": "2025-11-27",
    "station_id": 1,
    "pollutant_id": 1
  }'
```

**Postman:**
- Method: `POST`
- URL: `{{API_URL}}/reports`
- Headers:
  - `Authorization`: `Bearer {{TOKEN}}`
  - `Content-Type`: `application/json`
- Body (raw JSON):
```json
{
  "city": "New York",
  "start_date": "2025-11-01",
  "end_date": "2025-11-27",
  "station_id": 1,
  "pollutant_id": 1
}
```

---

### 7.2 List User Reports

**cURL:**
```bash
curl -X GET "$API_URL/reports?limit=10" \
  -H "Authorization: Bearer $TOKEN"
```

**Postman:**
- Method: `GET`
- URL: `{{API_URL}}/reports`
- Headers:
  - `Authorization`: `Bearer {{TOKEN}}`
- Params:
  - `limit`: `10`
  - `skip`: `0`

---

### 7.3 Get Report by ID

**cURL:**
```bash
curl -X GET "$API_URL/reports/1" \
  -H "Authorization: Bearer $TOKEN"
```

**Postman:**
- Method: `GET`
- URL: `{{API_URL}}/reports/1`
- Headers:
  - `Authorization`: `Bearer {{TOKEN}}`

---

## 📦 Colección Postman

### Importar Variables de Entorno

Crear un archivo `environment.json`:

```json
{
  "id": "air-quality-env",
  "name": "Air Quality API",
  "values": [
    {
      "key": "API_URL",
      "value": "http://localhost:8000/api/v1",
      "enabled": true
    },
    {
      "key": "TOKEN",
      "value": "",
      "enabled": true
    },
    {
      "key": "USER_EMAIL",
      "value": "user@example.com",
      "enabled": true
    },
    {
      "key": "USER_PASSWORD",
      "value": "password123",
      "enabled": true
    }
  ]
}
```

### Script para Auto-guardar Token

En Postman, en la request de Login, agregar en "Tests":

```javascript
// Parse response
var jsonData = pm.response.json();

// Save token to environment
if (jsonData.access_token) {
    pm.environment.set("TOKEN", jsonData.access_token);
    console.log("Token saved:", jsonData.access_token);
}

// Save user info
if (jsonData.user) {
    pm.environment.set("USER_ID", jsonData.user.id);
    pm.environment.set("USER_ROLE", jsonData.user.role.name);
    console.log("User info saved");
}
```

---

## 🧪 Test Sequences (Flujos Completos)

### Secuencia 1: Usuario Normal

```bash
# 1. Login
curl -X POST "$API_URL/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=user@example.com&password=password123" \
  | jq -r '.access_token' > token.txt

export TOKEN=$(cat token.txt)

# 2. Ver mi información
curl -X GET "$API_URL/auth/me" \
  -H "Authorization: Bearer $TOKEN" | jq

# 3. Ver estaciones
curl -X GET "$API_URL/stations?limit=5" | jq

# 4. Ver dashboard
curl -X GET "$API_URL/air-quality/dashboard?city=New%20York" | jq

# 5. Obtener recomendación
curl -X GET "$API_URL/recommendations/current?location=New%20York" \
  -H "Authorization: Bearer $TOKEN" | jq

# 6. Ver mis preferencias
curl -X GET "$API_URL/settings/preferences" \
  -H "Authorization: Bearer $TOKEN" | jq

# 7. Generar reporte
curl -X POST "$API_URL/reports" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "city": "New York",
    "start_date": "2025-11-01",
    "end_date": "2025-11-27"
  }' | jq
```

---

### Secuencia 2: Administrador

```bash
# 1. Login como admin
curl -X POST "$API_URL/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin@example.com&password=admin123" \
  | jq -r '.access_token' > admin_token.txt

export ADMIN_TOKEN=$(cat admin_token.txt)

# 2. Verificar salud del sistema
curl -X GET "$API_URL/admin/health" | jq

# 3. Listar todos los usuarios
curl -X GET "$API_URL/admin/users" \
  -H "Authorization: Bearer $ADMIN_TOKEN" | jq

# 4. Crear nueva estación
curl -X POST "$API_URL/admin/stations" \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Station",
    "latitude": 40.7128,
    "longitude": -74.0060,
    "city": "New York",
    "country": "USA",
    "region_id": 1
  }' | jq

# 5. Actualizar rol de usuario
curl -X PUT "$API_URL/admin/users/2/role" \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"role_id": 2}' | jq
```

---

## 🔍 Testing con Scripts

### Script Bash Completo

```bash
#!/bin/bash

API_URL="http://localhost:8000/api/v1"

echo "=== Testing Air Quality API ==="
echo ""

# 1. Health Check
echo "1. Health Check..."
curl -s "$API_URL/admin/health" | jq '.'
echo ""

# 2. Login
echo "2. Login..."
LOGIN_RESPONSE=$(curl -s -X POST "$API_URL/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=user@example.com&password=password123")

TOKEN=$(echo $LOGIN_RESPONSE | jq -r '.access_token')
echo "Token: ${TOKEN:0:20}..."
echo ""

# 3. Get current user
echo "3. Get Current User..."
curl -s "$API_URL/auth/me" \
  -H "Authorization: Bearer $TOKEN" | jq '.'
echo ""

# 4. List stations
echo "4. List Stations..."
curl -s "$API_URL/stations?limit=3" | jq '.[] | {id, name, city}'
echo ""

# 5. Get dashboard
echo "5. Get Dashboard..."
curl -s "$API_URL/air-quality/dashboard?city=New%20York" | jq '.daily_stats'
echo ""

echo "=== Tests completed ==="
```

Guardar como `test_api.sh` y ejecutar:

```bash
chmod +x test_api.sh
./test_api.sh
```

---

## 📊 Validación de Respuestas

### Usando jq para filtrar

```bash
# Obtener solo el AQI
curl -s "$API_URL/air-quality/current?city=New%20York" | jq '.aqi'

# Obtener nombres de estaciones
curl -s "$API_URL/stations" | jq '.[].name'

# Obtener solo productos recomendados
curl -s "$API_URL/recommendations/current" \
  -H "Authorization: Bearer $TOKEN" | jq '.products'

# Contar usuarios
curl -s "$API_URL/admin/users" \
  -H "Authorization: Bearer $TOKEN" | jq 'length'
```

---

## ✅ Checklist de Testing

- [ ] Login funciona correctamente
- [ ] Token se guarda y usa correctamente
- [ ] Endpoints públicos responden sin auth
- [ ] Endpoints protegidos requieren token
- [ ] Endpoints admin solo funcionan con role Admin
- [ ] Paginación funciona (skip/limit)
- [ ] Filtros funcionan correctamente
- [ ] Validación de datos rechaza entrada inválida
- [ ] Errores retornan códigos HTTP correctos
- [ ] Respuestas siguen el formato especificado

---

**Happy Testing! 🧪**

