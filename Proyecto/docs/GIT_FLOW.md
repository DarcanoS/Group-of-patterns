# Git Flow - Metodología de Trabajo

Este documento describe la metodología **Git Flow** aplicada al proyecto Air Quality Platform para mantener un flujo de trabajo ordenado y colaborativo.

## 🌳 Estructura de Ramas

### Ramas Principales

#### `main`
- Rama de **producción**
- Contiene código estable y probado
- Solo se actualiza mediante merge desde `develop` o `hotfix`
- Cada commit en `main` debe estar etiquetado con una versión (ej: `v1.0.0`, `v1.1.0`)

#### `develop`
- Rama de **integración y desarrollo**
- Contiene las últimas características completadas
- Base para crear nuevas ramas de características (`feature`)
- Se integra a `main` cuando se prepara un release

### Ramas de Soporte

#### `feature/*`
- Para desarrollar **nuevas funcionalidades**
- Se crean desde `develop`
- Se fusionan de vuelta a `develop`
- Nomenclatura: `feature/nombre-descriptivo`
  - Ejemplo: `feature/citizen-dashboard`
  - Ejemplo: `feature/air-quality-endpoints`

#### `release/*`
- Para preparar una **nueva versión de producción**
- Se crean desde `develop`
- Permiten correcciones menores y preparación de metadatos
- Se fusionan a `main` y `develop`
- Nomenclatura: `release/v1.x.x`
  - Ejemplo: `release/v1.0.0`

#### `hotfix/*`
- Para **correcciones urgentes** en producción
- Se crean desde `main`
- Se fusionan a `main` y `develop`
- Nomenclatura: `hotfix/descripcion-breve`
  - Ejemplo: `hotfix/fix-login-error`

## 🔄 Flujos de Trabajo

### 1. Desarrollar una Nueva Funcionalidad

```bash
# Asegúrate de estar en develop actualizado
git checkout develop
git pull origin develop

# Crea una nueva rama feature
git checkout -b feature/nombre-funcionalidad

# Desarrolla tu funcionalidad
# Realiza commits descriptivos
git add .
git commit -m "feat: descripción clara del cambio"

# Al finalizar, actualiza develop y fusiona
git checkout develop
git pull origin develop
git merge feature/nombre-funcionalidad

# Sube los cambios
git push origin develop

# Elimina la rama feature (opcional)
git branch -d feature/nombre-funcionalidad
```

### 2. Preparar un Release

```bash
# Desde develop, crea una rama release
git checkout develop
git checkout -b release/v1.0.0

# Realiza ajustes finales (versiones, changelog, etc.)
git commit -m "chore: prepare release v1.0.0"

# Fusiona a main
git checkout main
git merge release/v1.0.0
git tag -a v1.0.0 -m "Release version 1.0.0"

# Fusiona de vuelta a develop
git checkout develop
git merge release/v1.0.0

# Sube cambios y tags
git push origin main
git push origin develop
git push origin v1.0.0

# Elimina la rama release
git branch -d release/v1.0.0
```

### 3. Aplicar un Hotfix

```bash
# Desde main, crea una rama hotfix
git checkout main
git checkout -b hotfix/fix-critical-bug

# Corrige el problema
git commit -m "fix: corrige error crítico en producción"

# Fusiona a main
git checkout main
git merge hotfix/fix-critical-bug
git tag -a v1.0.1 -m "Hotfix version 1.0.1"

# Fusiona a develop
git checkout develop
git merge hotfix/fix-critical-bug

# Sube cambios
git push origin main
git push origin develop
git push origin v1.0.1

# Elimina la rama hotfix
git branch -d hotfix/fix-critical-bug
```

## 📝 Convenciones de Commits

Utiliza el formato **Conventional Commits** para mensajes claros:

```
<tipo>(<alcance>): <descripción breve>

[cuerpo opcional]

[footer opcional]
```

### Tipos de Commits

- **feat**: Nueva funcionalidad
- **fix**: Corrección de errores
- **docs**: Cambios en documentación
- **style**: Cambios de formato (sin afectar lógica)
- **refactor**: Refactorización de código
- **test**: Agregar o modificar tests
- **chore**: Tareas de mantenimiento (dependencias, configs)
- **perf**: Mejoras de rendimiento

### Ejemplos

```bash
git commit -m "feat(backend): add air quality endpoints for citizen dashboard"
git commit -m "fix(frontend): resolve login validation error"
git commit -m "docs: update README with installation instructions"
git commit -m "refactor(ingestion): apply adapter pattern for external APIs"
```

## 🎯 Buenas Prácticas

1. **Nunca trabajes directamente en `main` o `develop`**
   - Siempre crea una rama de soporte

2. **Mantén las ramas actualizadas**
   - Haz `git pull` regularmente desde `develop`

3. **Commits pequeños y frecuentes**
   - Facilita la revisión y reversión de cambios

4. **Describe claramente tus cambios**
   - Usa mensajes de commit descriptivos

5. **Revisa antes de fusionar**
   - Verifica que no haya conflictos
   - Asegúrate de que el código funciona

6. **Elimina ramas obsoletas**
   - Mantén el repositorio limpio

7. **Etiqueta las versiones**
   - Usa semantic versioning (`MAJOR.MINOR.PATCH`)

## 🔍 Comandos Útiles

```bash
# Ver todas las ramas
git branch -a

# Ver el estado actual
git status

# Ver historial de commits
git log --oneline --graph --all

# Cambiar entre ramas
git checkout nombre-rama

# Crear y cambiar a nueva rama
git checkout -b nombre-nueva-rama

# Actualizar rama actual
git pull origin nombre-rama

# Ver diferencias
git diff

# Ver ramas fusionadas
git branch --merged
```

## 📚 Referencias

- [Git Flow Original](https://nvie.com/posts/a-successful-git-branching-model/)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [Semantic Versioning](https://semver.org/)
