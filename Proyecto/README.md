# Proyecto: Air Quality Platform

Este directorio contiene el desarrollo de una plataforma web para la consulta y análisis de datos de calidad del aire.

## 📁 Estructura del Proyecto

### `docs/`
Contiene la documentación global del proyecto:
- **[`COPILOT_GLOBAL.md`](docs/COPILOT_GLOBAL.md)**: Instrucciones principales y arquitectura completa del sistema. Define la estructura del monorepo, modelo de datos, patrones de diseño requeridos, paleta de colores y guías de desarrollo para toda la aplicación.
- **[`GIT_FLOW.md`](docs/GIT_FLOW.md)**: Guía de metodología Git Flow para el proyecto, incluyendo estructura de ramas, flujos de trabajo y convenciones de commits.

### `backend/`
API REST desarrollada en **Python con FastAPI**:
- **`COPILOT_BACKEND.md`**: Prompt específico para el desarrollo del backend, incluyendo endpoints, lógica de negocio y conexión con PostgreSQL/PostGIS.

### `frontend/`
Aplicación web desarrollada en **Vue 3**:
- **`COPILOT_FRONTEND.md`**: Prompt específico para el desarrollo del frontend, componentes, vistas, gestión de estado y sistema de diseño.
- **`ejemplos/`**: Mockups HTML de referencia para las diferentes vistas (login, dashboards de ciudadano e investigador, landing page).

### `database/`
Gestión de la base de datos:
- **`COPILOT_DATABASE.md`**: Prompt para el diseño y configuración de PostgreSQL con PostGIS, esquemas, migraciones y scripts de inicialización.

### `ingestion/`
Servicio de ingesta de datos externos:
- **`COPILOT_INGESTION.md`**: Prompt para el desarrollo del servicio que consume APIs externas de calidad del aire, normaliza datos y los almacena en la base de datos.

## 🚀 Tecnologías Principales

- **Frontend**: Vue 3, TypeScript
- **Backend**: Python, FastAPI
- **Base de datos**: PostgreSQL + PostGIS
- **Configuraciones**: MongoDB (NoSQL)
- **Contenedorización**: Docker

## 📝 Notas

Cada carpeta contiene su propio archivo `COPILOT_*.md` con instrucciones detalladas para el desarrollo de ese componente específico. Consulta `docs/COPILOT_GLOBAL.md` para entender la arquitectura completa y las guías generales del proyecto.
