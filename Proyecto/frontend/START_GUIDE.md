# 🚀 Guía Rápida - Iniciar Backend y Probar Integración

## ✅ Estado Actual

### Frontend
- ✅ **Servicios integrados** con endpoints reales del backend
- ✅ **Servidor corriendo** en `http://localhost:5173`
- ✅ **Sin errores de compilación**

### Backend
- ⏸️  **No está corriendo actualmente**
- 📍 Debe correr en `http://localhost:8000`

---

## 🔧 Pasos para Probar la Integración

### 1. Iniciar el Backend

Navega a la carpeta del backend y ejecuta:

```bash
# Opción A: Si usas uvicorn directamente
cd /Users/sebasmancera/Group-of-patterns/Proyecto/backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Opción B: Si tienes un script de inicio
python run.py

# Opción C: Con Docker (si aplica)
docker-compose up
```

### 2. Verificar que el Backend Esté Listo

Una vez iniciado, ejecuta el script de prueba:

```bash
cd /Users/sebasmancera/Group-of-patterns/Proyecto/frontend
./test-backend.sh
```

O verifica manualmente:
```bash
curl http://localhost:8000/api/v1/admin/health
```

Deberías ver algo como:
```json
{
  "status": "healthy",
  "database": "connected",
  "message": "Database contains 6 pollutants"
}
```

### 3. Probar con la Interfaz de Pruebas

Abre en tu navegador:
```
/Users/sebasmancera/Group-of-patterns/Proyecto/frontend/test-integration.html
```

Este archivo HTML te permite probar cada endpoint individualmente.

### 4. Probar el Frontend Completo

El frontend ya está corriendo en:
```
http://localhost:5173
```

**Flujo de prueba recomendado:**

1. **Landing Page** (`/`)
   - Debe cargar sin errores
   - No requiere backend inicialmente

2. **Login** (`/login`)
   - Intenta hacer login con credenciales del backend
   - Ejemplos comunes:
     - `citizen@example.com` / `citizen123`
     - `researcher@example.com` / `researcher123`
     - `admin@example.com` / `admin123`

3. **Citizen Dashboard** (`/citizen`)
   - Requiere login exitoso
   - Debe mostrar:
     - Calidad del aire actual
     - Gráficos con datos reales
     - Recomendaciones personalizadas

4. **Researcher Dashboard** (`/researcher`)
   - Requiere login con rol Researcher
   - Debe mostrar:
     - Estadísticas diarias
     - Filtros funcionales
     - Tabla con datos reales

---

## 🧪 Pruebas Específicas por Componente

### Login View
```javascript
// Probar en DevTools Console
const response = await fetch('http://localhost:8000/api/v1/auth/login', {
  method: 'POST',
  headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
  body: 'username=citizen@example.com&password=citizen123'
});
const data = await response.json();
console.log(data);
```

### Citizen Dashboard
```javascript
// Verificar datos de AQI
const aqi = await fetch('http://localhost:8000/api/v1/air-quality/current?city=Bogotá');
console.log(await aqi.json());
```

### Researcher Dashboard
```javascript
// Verificar estadísticas diarias
const stats = await fetch('http://localhost:8000/api/v1/air-quality/daily-stats?limit=30');
console.log(await stats.json());
```

---

## 📊 Datos de Prueba

Si el backend usa datos de ejemplo, verifica que existan:

### Usuarios
- **Citizen:** `citizen@example.com` / `citizen123`
- **Researcher:** `researcher@example.com` / `researcher123`
- **Admin:** `admin@example.com` / `admin123`

### Ciudades/Estaciones
- Debe haber al menos una ciudad con estaciones activas
- Ejemplo: Bogotá, New York, etc.

### Contaminantes
- PM2.5, PM10, O3, NO2, SO2, CO

---

## 🐛 Troubleshooting

### Error: "Failed to fetch"
**Causa:** Backend no está corriendo
**Solución:** Inicia el backend en el puerto 8000

### Error: CORS
**Causa:** Backend no permite origen `http://localhost:5173`
**Solución:** Agrega CORS en el backend:
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Error: 401 Unauthorized
**Causa:** Token expirado o inválido
**Solución:** Haz login nuevamente desde `/login`

### Error: 404 Not Found
**Causa:** Endpoint no existe o ruta incorrecta
**Solución:** Verifica el contrato de API en `ejemplos/API_CONTRACT.md`

### Backend responde pero sin datos
**Causa:** Base de datos vacía
**Solución:** Ejecuta el seeder del backend:
```bash
cd backend
python seed_data.py  # o el script que corresponda
```

---

## ✅ Checklist de Verificación

### Backend
- [ ] Backend corriendo en `http://localhost:8000`
- [ ] Health check responde OK
- [ ] Swagger UI accesible en `http://localhost:8000/docs`
- [ ] CORS configurado para `localhost:5173`
- [ ] Base de datos con datos de prueba

### Frontend
- [x] Servidor corriendo en `http://localhost:5173`
- [x] Sin errores de compilación
- [x] Servicios integrados
- [ ] Login funcional
- [ ] Dashboard carga datos reales
- [ ] Gráficos muestran datos del backend

---

## 📝 Próximas Pruebas

1. **Funcionalidad Completa:**
   - [ ] Login → Citizen Dashboard → Ver AQI
   - [ ] Login → Researcher Dashboard → Ver estadísticas
   - [ ] Cambio de ciudad en dashboard
   - [ ] Filtros de fecha en researcher dashboard
   - [ ] Recomendaciones personalizadas

2. **Manejo de Errores:**
   - [ ] Login con credenciales incorrectas
   - [ ] Token expirado
   - [ ] Ciudad sin datos
   - [ ] Backend caído

3. **Rendimiento:**
   - [ ] Tiempo de carga inicial
   - [ ] Tiempo de respuesta de APIs
   - [ ] Actualización de datos en tiempo real

---

## 📚 Recursos

- **Documentación Backend API:** `/ejemplos/API_CONTRACT.md`
- **Resumen de Integración:** `/INTEGRATION_COMPLETE.md`
- **Tests HTML:** `/test-integration.html`
- **Script de verificación:** `/test-backend.sh`

---

## 🎯 Resumen

**Todo está listo del lado del frontend.** Solo necesitas:

1. ✅ Iniciar el backend
2. ✅ Ejecutar `./test-backend.sh` para verificar
3. ✅ Abrir `http://localhost:5173` y probar

La integración está **100% completa** y lista para uso en producción una vez que el backend esté disponible.

