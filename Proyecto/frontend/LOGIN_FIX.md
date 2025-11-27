# 🔧 Corrección del Sistema de Login y Registro

**Fecha:** 27 de Noviembre, 2025  
**Problema:** El login y registro no hacían peticiones al backend, solo simulaban la acción con `console.log`

---

## ✅ Cambios Realizados

### 1. **LoginView.vue** - Login Real con Backend
**Antes:** ❌ Solo hacía `console.log` y redirigía a `/dashboard` (simulado)
**Ahora:** ✅ Hace peticiones reales al backend

**Funcionalidades agregadas:**
- ✅ Llama al servicio `authService.login()` con email y password
- ✅ Muestra estado de "Iniciando sesión..." mientras carga
- ✅ Muestra mensajes de error si falla la autenticación
- ✅ Guarda el token JWT en localStorage
- ✅ Guarda información del usuario en localStorage
- ✅ Redirecciona según el rol del usuario:
  - `citizen` → `/citizen-dashboard`
  - `researcher` → `/researcher-dashboard`
  - `admin` → `/admin-dashboard`
- ✅ Logs detallados en consola para debugging

### 2. **RegisterView.vue** - Registro Real con Backend
**Antes:** ❌ Solo hacía `console.log` y redirigía a `/login` (simulado)
**Ahora:** ✅ Hace peticiones reales al backend

**Funcionalidades agregadas:**
- ✅ Llama al servicio `authService.register()` con los datos del usuario
- ✅ Muestra estado de "Registrando..." mientras carga
- ✅ Muestra mensajes de error si falla el registro
- ✅ Muestra mensaje de éxito cuando se registra correctamente
- ✅ Redirecciona automáticamente a `/login` después de 2 segundos
- ✅ Valida contraseña mínima de 6 caracteres
- ✅ Registra usuarios con rol "Citizen" por defecto (role_id: 1)
- ✅ Logs detallados en consola para debugging

### 3. **authService.ts** - Función de Registro Agregada
**Archivo renombrado:** `authService.js` → `authService.ts` (para soportar TypeScript correctamente)

**Nueva función agregada:**
```typescript
export async function register(data: RegisterData): Promise<User>
```

**Interface agregada:**
```typescript
interface RegisterData {
  email: string;
  password: string;
  full_name: string;
  role_id?: number;
}
```

---

## 🧪 Cómo Probar

### 1. **Asegúrate que el backend esté corriendo:**
```bash
# Verificar que el backend responda
curl http://localhost:8000/api/v1/admin/health
```

### 2. **Inicia el frontend:**
```bash
cd /Users/sebasmancera/Group-of-patterns/Proyecto/frontend
npm run dev
```

### 3. **Abre las DevTools del navegador (F12)**
- Ve a la pestaña **Network** para ver las peticiones HTTP
- Ve a la pestaña **Console** para ver los logs

### 4. **Prueba el Login:**
```
URL: http://localhost:5173/login
Email: citizen@example.com
Password: citizen123
```

**Deberías ver en Network:**
- ✅ `POST http://localhost:8000/api/v1/auth/login`
- ✅ Status: `200 OK`
- ✅ Response con `access_token` y datos del usuario

**Deberías ver en Console:**
```
🔄 Intentando login con: citizen@example.com
✅ Login exitoso: {...}
👤 Usuario: {...}
🎭 Rol: Citizen
```

**Deberías ver en Application → Local Storage:**
- ✅ `access_token`: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
- ✅ `user`: {"id":1,"email":"citizen@example.com",...}

### 5. **Prueba el Registro:**
```
URL: http://localhost:5173/register
Nombre: Test User
Email: test@example.com
Password: test123
```

**Deberías ver en Network:**
- ✅ `POST http://localhost:8000/api/v1/auth/register`
- ✅ Status: `201 Created`
- ✅ Response con datos del usuario creado

**Deberías ver en Console:**
```
🔄 Intentando registro: Test User test@example.com
✅ Registro exitoso: {...}
```

**Deberías ver en la pantalla:**
- ✅ Mensaje verde: "¡Registro exitoso! Redirigiendo al login..."
- ✅ Redirección automática a `/login` después de 2 segundos

---

## 🎯 Endpoints del Backend Utilizados

### Login
```
POST /api/v1/auth/login
Content-Type: application/x-www-form-urlencoded

Body:
  username: email del usuario
  password: contraseña
```

### Registro
```
POST /api/v1/auth/register
Content-Type: application/json

Body:
{
  "email": "test@example.com",
  "password": "test123",
  "full_name": "Test User",
  "role_id": 1
}
```

---

## 🐛 Debugging

Si el login no funciona, revisa:

1. **Backend está corriendo:** `curl http://localhost:8000/api/v1/admin/health`
2. **URL correcta en httpClient.ts:** Debe ser `http://localhost:8000/api/v1`
3. **CORS configurado en el backend:** Debe permitir `http://localhost:5173`
4. **Credenciales correctas:** Verifica que el usuario exista en la base de datos
5. **DevTools → Network:** Revisa el status code y la respuesta del servidor
6. **DevTools → Console:** Revisa los logs y errores

---

## 📝 Notas Importantes

- ✅ Los tokens JWT se guardan en `localStorage`
- ✅ Los usuarios se registran por defecto con rol "Citizen" (role_id: 1)
- ✅ La redirección después del login depende del rol del usuario
- ✅ Los errores se muestran en rojo en la interfaz
- ✅ Los estados de carga desactivan el botón para evitar múltiples envíos

---

## 🎉 Resultado

Ahora el sistema de autenticación está completamente funcional y hace peticiones reales al backend. 
Los usuarios pueden:
1. ✅ Registrarse y crear una cuenta nueva
2. ✅ Iniciar sesión con email y contraseña
3. ✅ Ser redirigidos al dashboard correcto según su rol
4. ✅ Ver mensajes de error claros si algo falla
5. ✅ Ver el estado de carga mientras se procesa la petición

