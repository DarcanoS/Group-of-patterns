# 📚 Documentación del Servicio de Ingestion

Índice de toda la documentación del servicio de ingestion de Air Quality Platform.

---

## 🗺️ Guía de Navegación

### Para empezar rápido
👉 **[../README.md](../README.md)** - Inicio rápido, instalación y uso básico

### Para entender la arquitectura
👉 **[ARCHITECTURE.md](./ARCHITECTURE.md)** - Diagramas, flujos de datos y casos de uso

### Para entender los patrones de diseño
👉 **[DESIGN_PATTERNS.md](./DESIGN_PATTERNS.md)** - Teoría, implementación y ejemplos

### Para usar la API de AQICN
👉 **[AQICN_USAGE.md](./AQICN_USAGE.md)** - Guía de uso de ingestion en tiempo real
👉 **[API_AQICN.md](./API_AQICN.md)** - Especificación técnica del cliente AQICN

---

## 📖 Resumen de Cada Documento

### 1. [../README.md](../README.md) - Documentación Principal
**Audiencia**: Desarrolladores que usan el servicio

**Contenido**:
- ✅ Descripción general del servicio
- ✅ Instalación y configuración
- ✅ Uso local y con Docker
- ✅ Formato de datos de entrada (CSV, GeoJSON)
- ✅ Comandos CLI
- ✅ Troubleshooting básico

**Cuándo leerlo**: 
- Primera vez usando el servicio
- Necesitas ejecutar ingestion histórica o en tiempo real
- Configurando environment variables

---

### 2. [ARCHITECTURE.md](./ARCHITECTURE.md) - Arquitectura Visual
**Audiencia**: Desarrolladores, arquitectos, estudiantes

**Contenido**:
- 🏗️ Diagrama de arquitectura general
- 🔄 Flujo completo de datos (paso a paso)
- 🎨 Secuencia de ejecución del Adapter Pattern
- 📊 Transformación de datos (CSV → DTO → DB)
- 🗄️ Modelo de datos con relaciones
- 📂 Estructura de archivos anotada
- 🔀 Casos de uso reales con ejemplos
- 🧩 Ejemplos de extensibilidad
- 📈 Consideraciones de performance
- 🚀 Ejemplos de deployment

**Cuándo leerlo**:
- Necesitas entender cómo funciona internamente
- Vas a agregar una nueva fuente de datos
- Estás estudiando patrones de diseño
- Debugging de problemas complejos

**Diagramas incluidos**:
```
- Arquitectura general
- Flujo de ingestion histórica (14 pasos)
- Secuencia de ejecución Adapter Pattern
- Transformación CSV → DB
- Modelo de datos (ERD simplificado)
- Estructura de archivos con leyenda
```

---

### 3. [DESIGN_PATTERNS.md](./DESIGN_PATTERNS.md) - Patrones de Diseño
**Audiencia**: Estudiantes, arquitectos, code reviewers

**Contenido**:
- 📐 **Adapter Pattern** (principal)
  - Teoría y propósito
  - Componentes (Base, Concrete, Target)
  - Diagrama de clases UML
  - Ventajas del patrón
  - Ejemplo de uso real
  - Caso de uso completo
- 🔄 **Patrones relacionados**
  - Repository Pattern (implícito)
  - Strategy Pattern (normalización)
  - DTO Pattern
- 🏗️ Arquitectura en capas
- 🎯 SOLID Principles aplicados
- 📝 Ejemplo completo: Agregar nueva fuente
- 🧪 Estrategias de testing
- 📊 Tabla resumen de patrones
- 🔮 Patrones candidatos para futuro

**Cuándo leerlo**:
- Estudiando patrones de diseño
- Preparando presentación/documentación académica
- Revisión de código (code review)
- Planeando nuevas features

**Conceptos clave**:
- ¿Qué es el Adapter Pattern?
- ¿Por qué lo usamos?
- ¿Cómo implementarlo en Python?
- ¿Qué otros patrones usamos?
- ¿Cómo testear adapters?

---

### 4. [AQICN_USAGE.md](./AQICN_USAGE.md) - Guía de Uso AQICN ✅ **NUEVO**
**Audiencia**: Desarrolladores usando ingestion en tiempo real

**Contenido**:
- ✅ Cómo usar el servicio de ingestion en tiempo real
- ✅ Configuración del token de API AQICN
- ✅ Ejecutar tests
- ✅ Resultado esperado
- ✅ Flujo de trabajo completo
- ✅ Mapeo de estaciones
- ✅ Automatización con cron/systemd

**Cuándo leerlo**:
- Ejecutando ingestion en tiempo real por primera vez
- Configurando automatización
- Debugging de problemas con AQICN API

---

### 5. [API_AQICN.md](./API_AQICN.md) - Especificación Técnica AQICN
**Audiencia**: Desarrolladores implementando o extendiendo `AqicnAdapter`

**Contenido**:
- 📡 Especificación de API AQICN/WAQI
- 🔑 Autenticación y rate limiting
- 🛠️ Endpoints soportados
  - Search stations
  - City feed
  - Station feed by UID
  - Geo feed
  - Map bounds
- 💻 Estructura del cliente Python
- 📝 Ejemplos de uso
- ⚠️ Consideraciones de uso aceptable

**Cuándo leerlo**:
- Implementando funcionalidad relacionada con AQICN
- Debugging de llamadas a API
- Entendiendo formato de respuesta AQICN
- Extendiendo el cliente con nuevos endpoints

---

## 🎓 Rutas de Aprendizaje

### 🚀 Ruta "Quick Start" (Usuario)
```
1. ../README.md (sección "Uso")
   ↓
2. Configurar .env
   ↓
3a. Ingestion Histórica: python -m app.main --mode historical
3b. Ingestion Tiempo Real: python -m app.main --mode realtime
```

### 🏗️ Ruta "Arquitectura" (Desarrollador)
```
1. ../README.md (descripción general)
   ↓
2. ARCHITECTURE.md (flujos y diagramas)
   ↓
3. Ver código: app/main.py → ingestion_service.py → csv_adapter.py / aqicn_adapter.py
```

### 📐 Ruta "Patrones de Diseño" (Estudiante)
```
1. DESIGN_PATTERNS.md (teoría)
   ↓
2. ARCHITECTURE.md (implementación visual)
   ↓
3. Ver código: app/providers/base_adapter.py
   ↓
4. Ejercicio: Implementar MockAdapter para testing
```

### 🔧 Ruta "Usar Ingestion Tiempo Real" (Desarrollador)
```
1. AQICN_USAGE.md (guía completa)
   ↓
2. Configurar TOKEN_API_AQICN en .env
   ↓
3. python tests/test_aqicn_api.py (verificar API)
   ↓
4. python -m app.main --mode realtime
```

---

## 🔍 Buscar por Tema

### Configuración
- [../README.md § Configuración](../README.md#⚙️-configuración)
- [../README.md § .env variables](../README.md#1-variables-de-entorno)
- [AQICN_USAGE.md § Configuración](./AQICN_USAGE.md#1-configuración)

### Patrones de Diseño
- [DESIGN_PATTERNS.md § Adapter Pattern](./DESIGN_PATTERNS.md#1-adapter-pattern-patrón-adaptador)
- [DESIGN_PATTERNS.md § SOLID Principles](./DESIGN_PATTERNS.md#🎯-principios-solid-aplicados)
- [ARCHITECTURE.md § Adapter Sequence](./ARCHITECTURE.md#🎨-adapter-pattern---secuencia-de-ejecución)

### Datos
- [../README.md § Datos de Entrada](../README.md#📊-datos-de-entrada)
- [ARCHITECTURE.md § Data Transformation](./ARCHITECTURE.md#📊-transformación-de-datos)

### API AQICN
- [AQICN_USAGE.md](./AQICN_USAGE.md) - Guía completa de uso
- [API_AQICN.md](./API_AQICN.md) - Especificación técnica

### Extensibilidad
- [DESIGN_PATTERNS.md § Agregar Nueva Fuente](./DESIGN_PATTERNS.md#📝-ejemplo-completo-agregar-nueva-fuente-de-datos)
- [ARCHITECTURE.md § Extensibilidad](./ARCHITECTURE.md#🧩-extensibilidad)

### Performance
- [ARCHITECTURE.md § Performance](./ARCHITECTURE.md#📈-performance-considerations)

### Testing
- [DESIGN_PATTERNS.md § Testing](./DESIGN_PATTERNS.md#🧪-testing-de-patrones)
- [ARCHITECTURE.md § Testing Strategy](./ARCHITECTURE.md#🎯-testing-strategy)
- [AQICN_USAGE.md § Tests](./AQICN_USAGE.md#3-ejecutar-pruebas)

### Deployment
- [../README.md § Docker](../README.md#docker)
- [ARCHITECTURE.md § Deployment](./ARCHITECTURE.md#🚀-deployment)
- [AQICN_USAGE.md § Automatización](./AQICN_USAGE.md#🔄-automatización)

---

## 📊 Matriz de Documentos

| Documento | Usuario | Dev | Arquitecto | Estudiante |
|-----------|---------|-----|------------|------------|
| README.md | ✅✅✅ | ✅✅ | ✅ | ✅ |
| ARCHITECTURE.md | ✅ | ✅✅✅ | ✅✅✅ | ✅✅✅ |
| DESIGN_PATTERNS.md | - | ✅✅ | ✅✅✅ | ✅✅✅ |
| AQICN_USAGE.md | ✅✅ | ✅✅✅ | ✅ | ✅✅ |
| API_AQICN.md | - | ✅✅✅ | ✅✅ | ✅ |

**Leyenda**: ✅ = Útil, ✅✅ = Muy útil, ✅✅✅ = Esencial

---

## 🗂️ Archivos del Proyecto

```
ingestion/
│
├── 📘 README.md                 ← Inicio: Instalación y uso
│
├── 📂 docs/                     ← Documentación técnica
│   ├── ARCHITECTURE.md          ← Diagramas y flujos visuales
│   ├── DESIGN_PATTERNS.md       ← Teoría de patrones
│   ├── AQICN_USAGE.md          ← Guía de uso tiempo real ✅ NUEVO
│   ├── API_AQICN.md            ← Spec técnica de cliente AQICN
│   └── DOCS_INDEX.md           ← Este archivo (índice)
│
├── 📂 tests/                    ← Tests ✅ REORGANIZADO
│   ├── test_aqicn_api.py       ← Test de API AQICN
│   └── test_aqicn_ingestion.py ← Test de ingestion completa
│
├── 📄 .env.example              ← Template de configuración
├── 📄 requirements.txt          ← Dependencias Python
├── 🐳 Dockerfile                ← Container image
│
├── 📂 app/                      ← Código fuente
│   ├── main.py
│   ├── config.py
│   ├── db/
│   ├── domain/
│   ├── providers/              ← 🎨 Adapter Pattern
│   │   ├── base_adapter.py
│   │   ├── historical_csv_adapter.py
│   │   └── aqicn_adapter.py   ← ✅ IMPLEMENTADO
│   └── services/
│
└── 📂 data/
    └── station_mapping.yaml    ← Configuración de estaciones
```

---

## ❓ FAQs

### "¿Por dónde empiezo?"
→ [../README.md](../README.md)

### "¿Cómo funciona internamente?"
→ [ARCHITECTURE.md](./ARCHITECTURE.md) - Sección "Flujo de Datos Completo"

### "¿Qué patrones de diseño usan?"
→ [DESIGN_PATTERNS.md](./DESIGN_PATTERNS.md) - Sección "Adapter Pattern"

### "¿Cómo agrego una nueva fuente de datos?"
→ [DESIGN_PATTERNS.md § Ejemplo Completo](./DESIGN_PATTERNS.md#📝-ejemplo-completo-agregar-nueva-fuente-de-datos)

### "¿Cómo uso la ingestion en tiempo real con AQICN?"
→ [AQICN_USAGE.md](./AQICN_USAGE.md) - Guía completa paso a paso

### "¿Cómo extiendo el cliente AQICN?"
→ [API_AQICN.md](./API_AQICN.md) - Especificación técnica completa

### "¿Cómo funciona la normalización de datos?"
→ [ARCHITECTURE.md § Transformación de Datos](./ARCHITECTURE.md#📊-transformación-de-datos)

### "¿Qué principios SOLID se usan?"
→ [DESIGN_PATTERNS.md § SOLID](./DESIGN_PATTERNS.md#🎯-principios-solid-aplicados)

---

## 🎯 Objetivos de la Documentación

✅ **Claridad**: Explicar conceptos complejos con diagramas y ejemplos  
✅ **Completitud**: Cubrir desde uso básico hasta arquitectura avanzada  
✅ **Navegabilidad**: Índices, enlaces internos y rutas de aprendizaje  
✅ **Practicidad**: Ejemplos reales, casos de uso, código funcional  
✅ **Educación**: Teoría de patrones, principios de diseño, best practices  

---

**Última actualización**: 26 de noviembre de 2025  
**Versión**: 1.0  
**Mantenedores**: Air Quality Platform Team
