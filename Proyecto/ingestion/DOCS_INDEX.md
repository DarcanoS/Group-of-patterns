# 📚 Documentación del Servicio de Ingestion

Índice de toda la documentación del servicio de ingestion de Air Quality Platform.

---

## 🗺️ Guía de Navegación

### Para empezar rápido
👉 **[README.md](./README.md)** - Inicio rápido, instalación y uso básico

### Para entender la arquitectura
👉 **[ARCHITECTURE.md](./ARCHITECTURE.md)** - Diagramas, flujos de datos y casos de uso

### Para entender los patrones de diseño
👉 **[DESIGN_PATTERNS.md](./DESIGN_PATTERNS.md)** - Teoría, implementación y ejemplos

### Para implementar integración con API externa
👉 **[API_AQICN.md](./API_AQICN.md)** - Especificación de cliente AQICN

### Para contribuir al proyecto
👉 **[COPILOT_INGESTION.md](./COPILOT_INGESTION.md)** - Instrucciones para Copilot/desarrolladores

---

## 📖 Resumen de Cada Documento

### 1. [README.md](./README.md) - Documentación de Usuario
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
- Necesitas ejecutar ingestion histórica
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

### 4. [API_AQICN.md](./API_AQICN.md) - Cliente AQICN
**Audiencia**: Desarrolladores implementando ingestion en tiempo real

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
- Implementando `AqicnAdapter`
- Debugging de llamadas a API
- Entendiendo formato de respuesta AQICN

**Próximo paso**: Implementar `app/providers/aqicn_adapter.py` basado en esta spec

---

### 5. [COPILOT_INGESTION.md](./COPILOT_INGESTION.md) - Guía de Desarrollo
**Audiencia**: GitHub Copilot, desarrolladores contribuyentes

**Contenido**:
- 📋 Tech stack completo
- 📦 Estructura de proyecto recomendada
- ⚙️ Variables de entorno
- 🗄️ Modelo de datos (DBML)
- 🔧 DTOs y normalización requerida
- 🎨 Especificación del Adapter Pattern
- 🔄 Flujo de ingestion (paso a paso)
- 📊 Agregación de stats diarias
- 🐛 Error handling y logging
- ⏱️ Scheduling y ejecución
- 🐳 Dockerfile requirements
- 📜 Reglas generales de código

**Cuándo leerlo**:
- Contribuyendo código nuevo
- Configurando entorno de desarrollo
- Entendiendo convenciones del proyecto
- Usando Copilot para generar código

---

## 🎓 Rutas de Aprendizaje

### 🚀 Ruta "Quick Start" (Usuario)
```
1. README.md (sección "Uso")
   ↓
2. Configurar .env
   ↓
3. Ejecutar: python -m app.main --mode historical
```

### 🏗️ Ruta "Arquitectura" (Desarrollador)
```
1. README.md (descripción general)
   ↓
2. ARCHITECTURE.md (flujos y diagramas)
   ↓
3. Ver código: app/main.py → ingestion_service.py → csv_adapter.py
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

### 🔧 Ruta "Implementar Feature" (Contribuidor)
```
1. COPILOT_INGESTION.md (convenciones)
   ↓
2. DESIGN_PATTERNS.md (ejemplo de extensión)
   ↓
3. API_AQICN.md (si es integración API)
   ↓
4. Implementar siguiendo patrón existente
   ↓
5. Revisar ARCHITECTURE.md para casos de uso
```

---

## 🔍 Buscar por Tema

### Configuración
- [README.md § Configuración](./README.md#⚙️-configuración)
- [README.md § .env variables](./README.md#1-variables-de-entorno)
- [COPILOT_INGESTION.md § Configuration](./COPILOT_INGESTION.md#2-configuration-and-environment)

### Patrones de Diseño
- [DESIGN_PATTERNS.md § Adapter Pattern](./DESIGN_PATTERNS.md#1-adapter-pattern-patrón-adaptador)
- [DESIGN_PATTERNS.md § SOLID Principles](./DESIGN_PATTERNS.md#🎯-principios-solid-aplicados)
- [ARCHITECTURE.md § Adapter Sequence](./ARCHITECTURE.md#🎨-adapter-pattern---secuencia-de-ejecución)

### Datos
- [README.md § Datos de Entrada](./README.md#📊-datos-de-entrada)
- [ARCHITECTURE.md § Data Transformation](./ARCHITECTURE.md#📊-transformación-de-datos)
- [COPILOT_INGESTION.md § DBML Model](./COPILOT_INGESTION.md#3-database-integration-aligned-with-dbml)

### Extensibilidad
- [DESIGN_PATTERNS.md § Agregar Nueva Fuente](./DESIGN_PATTERNS.md#📝-ejemplo-completo-agregar-nueva-fuente-de-datos)
- [ARCHITECTURE.md § Extensibilidad](./ARCHITECTURE.md#🧩-extensibilidad)
- [API_AQICN.md](./API_AQICN.md) (ejemplo de integración API)

### Performance
- [ARCHITECTURE.md § Performance](./ARCHITECTURE.md#📈-performance-considerations)
- Optimizaciones: caching, bulk processing, duplicate detection

### Testing
- [DESIGN_PATTERNS.md § Testing](./DESIGN_PATTERNS.md#🧪-testing-de-patrones)
- [ARCHITECTURE.md § Testing Strategy](./ARCHITECTURE.md#🎯-testing-strategy)

### Deployment
- [README.md § Docker](./README.md#docker)
- [ARCHITECTURE.md § Deployment](./ARCHITECTURE.md#🚀-deployment)

---

## 📊 Matriz de Documentos

| Documento | Usuario | Dev | Arquitecto | Estudiante | Copilot |
|-----------|---------|-----|------------|------------|---------|
| README.md | ✅✅✅ | ✅✅ | ✅ | ✅ | - |
| ARCHITECTURE.md | ✅ | ✅✅✅ | ✅✅✅ | ✅✅✅ | ✅ |
| DESIGN_PATTERNS.md | - | ✅✅ | ✅✅✅ | ✅✅✅ | ✅ |
| API_AQICN.md | - | ✅✅✅ | ✅ | ✅ | ✅✅ |
| COPILOT_INGESTION.md | - | ✅✅ | ✅✅ | ✅ | ✅✅✅ |

**Leyenda**: ✅ = Útil, ✅✅ = Muy útil, ✅✅✅ = Esencial

---

## 🗂️ Archivos del Proyecto

```
ingestion/
│
├── 📘 README.md                 ← Inicio: Instalación y uso
├── 📘 ARCHITECTURE.md           ← Diagramas y flujos visuales
├── 📘 DESIGN_PATTERNS.md        ← Teoría de patrones
├── 📘 API_AQICN.md              ← Spec de cliente AQICN
├── 📘 COPILOT_INGESTION.md      ← Guía de desarrollo
├── 📘 DOCS_INDEX.md             ← Este archivo (índice)
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
│   └── services/
│
└── 📂 data/
    └── station_mapping.yaml    ← Configuración de estaciones
```

---

## ❓ FAQs

### "¿Por dónde empiezo?"
→ [README.md](./README.md)

### "¿Cómo funciona internamente?"
→ [ARCHITECTURE.md](./ARCHITECTURE.md) - Sección "Flujo de Datos Completo"

### "¿Qué patrones de diseño usan?"
→ [DESIGN_PATTERNS.md](./DESIGN_PATTERNS.md) - Sección "Adapter Pattern"

### "¿Cómo agrego una nueva fuente de datos?"
→ [DESIGN_PATTERNS.md § Ejemplo Completo](./DESIGN_PATTERNS.md#📝-ejemplo-completo-agregar-nueva-fuente-de-datos)

### "¿Cómo implemento el cliente AQICN?"
→ [API_AQICN.md](./API_AQICN.md) + [COPILOT_INGESTION.md § Adapter Pattern](./COPILOT_INGESTION.md#5-adapter-pattern-for-external-providers-mandatory-design-pattern)

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
