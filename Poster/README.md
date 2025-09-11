# Proyecto de Póster LaTeX - Patrones de Arquitectura

Este proyecto contiene un póster académico desarrollado en LaTeX que presenta patrones de arquitectura empresarial utilizando diferentes puntos de vista y modelos.

## 📋 Estructura del Proyecto

```
Poster/
├── poster.tex              # Documento principal
├── constantes.tex          # Definiciones de constantes y comandos
├── compilar.sh            # Script de compilación para Linux/Mac
├── compilar.bat           # Script de compilación para Windows
├── limpiar.sh             # Script de limpieza para Linux/Mac
├── limpiar.bat            # Script de limpieza para Windows
├── arquitectura/          # Contenido del póster dividido en secciones
│   ├── uno.tex           
│   ├── dos.tex           
│   └── tres.tex          
├── formato/              # Configuración de formato y estilo
│   ├── programa.tex      # Configuraciones principales
│   ├── imgsPython.tex    # Configuración para código Python
│   └── apariencia/       # Estilos visuales
├── referencias/          # Archivos de bibliografía
│   ├── Articulos.bib
│   ├── Libros.bib
│   └── Textos.bib
├── imgs/                 # Imágenes organizadas por categorías
│   ├── caso/            # Casos de uso específicos
│   ├── meta/            # Diagramas meta
│   └── modelo/          # Modelos arquitecturales
└── svg-inkscape/        # Archivos SVG procesados por Inkscape
```

## 🛠️ Requisitos del Sistema

### Dependencias LaTeX
- **XeLaTeX** (recomendado)
- **Biber** para manejo de bibliografía
- **minted** para resaltado de código (requiere Python y Pygments)

### Paquetes LaTeX necesarios
- `geometry` - Para configuración de página
- `biblatex` - Para bibliografía avanzada
- `minted` - Para código con sintaxis resaltada
- `multicol` - Para columnas múltiples
- `amsthm` - Para teoremas matemáticos
- `framed` - Para marcos y cajas

## 🚀 Compilación

### Linux/Mac (Recomendado)

Utiliza el script proporcionado:

```bash
chmod +x compilar.sh
./compilar.sh
```

**O manualmente:**

```bash
xelatex -shell-escape poster.tex
biber poster
xelatex -shell-escape poster.tex
xelatex -shell-escape poster.tex
```

> **Nota:** El flag `-shell-escape` es necesario para el paquete `minted`

### Windows

**Opción 1: Usar el script automático (Recomendado)**

Utiliza el archivo `compilar.bat` incluido en el proyecto:

```cmd
compilar.bat
```

Este script ejecuta automáticamente todo el proceso de compilación con:
- Manejo de errores en cada paso
- Mensajes informativos del progreso
- Pausa al final para revisar los resultados

**Opción 2: Línea de comandos manual**
```cmd
xelatex -shell-escape poster.tex
biber poster
xelatex -shell-escape poster.tex
xelatex -shell-escape poster.tex
```

**Opción 3: PowerShell**
```powershell
xelatex -shell-escape poster.tex; biber poster; xelatex -shell-escape poster.tex; xelatex -shell-escape poster.tex
```

### Con TeXstudio/TeXmaker

1. Configura el compilador principal como **XeLaTeX**
2. Habilita `-shell-escape` en las opciones del compilador
3. Configura **Biber** como procesador de bibliografía
4. Compila usando F5 o el botón de compilación

## 🧹 Limpieza de Archivos Temporales

LaTeX genera muchos archivos auxiliares durante la compilación. Para limpiar el directorio:

### Linux/Mac

```bash
chmod +x limpiar.sh
./limpiar.sh
```

### Windows

```cmd
limpiar.bat
```

### Archivos que se eliminan:
- **Auxiliares**: `*.aux`, `*.log`, `*.fls`, `*.fdb_latexmk`
- **Bibliografía**: `*.bbl`, `*.bcf`, `*.blg`, `*.run.xml`
- **Minted**: `_minted-*/`, `*.pytxcode`
- **Temporales**: `*.synctex.gz`, `*.nav`, `*.out`, `*.toc`
- **Respaldo**: `*.bak`, `*.backup`, `*~`
- **Sistema**: `.DS_Store`, `Thumbs.db`, `*.tmp`

### Archivos que se mantienen:
- ✅ `*.tex` (archivos fuente)
- ✅ `*.bib` (bibliografía)
- ✅ `imgs/` (imágenes)
- ✅ `formato/` (configuración)
- ✅ `*.pdf` (salida final)

> **Nota**: Si quieres eliminar también los PDFs, descomenta la línea correspondiente en el script.

## 📖 Organización del Contenido

### Archivos Principales

- **`poster.tex`**: Documento principal que incluye configuración de página (50cm x 35cm) y estructura general
- **`constantes.tex`**: Define comandos personalizados para puntos de vista arquitecturales y rutas de imágenes
- **`arquitectura/`**: Contiene las tres secciones principales del póster

### Sistema de Constantes

El archivo `constantes.tex` define abbreviaciones para:
- **Puntos de Vista (PV)**: Stakeholder, Motivación, Organización, etc.
- **Rutas de Imágenes**: `\RMe` (meta), `\RM` (modelo), `\RC` (caso)
- **Nombres de Archivos**: Mapeo directo a archivos en `imgs/`

Ejemplo:
```tex
\newcommand{\PVMot}{Motivación}          % Punto de Vista
\newcommand{\Mot}{Motivacion}           % Nombre de archivo
\newcommand{\RM}{imgs/modelo/}           % Ruta base
```

### Gestión de Imágenes

Las imágenes están organizadas en:
- **`caso/`**: Aplicaciones específicas por dominio
- **`meta/`**: Diagramas de metamodelo
- **`modelo/`**: Modelos arquitecturales principales

## 🔧 Personalización

### Cambiar Dimensiones del Póster
Edita en `poster.tex`:
```tex
\usepackage[paperwidth=50cm,paperheight=35cm,margin=1cm]{geometry}
```

### Agregar Nueva Bibliografía
1. Añade entradas en `referencias/*.bib`
2. Incluye el archivo en `poster.tex`:
```tex
\addbibresource{referencias/TuArchivo.bib}
```

### Modificar Formato
- Colores y fuentes: `formato/apariencia/`
- Configuración de código: `formato/imgsPython.tex`
- Configuración general: `formato/programa.tex`

## 📝 Solución de Problemas

### Error: "Package minted not found"
```bash
# Ubuntu/Debian
sudo apt install python3-pygments texlive-latex-extra

# Windows (MiKTeX)
# Instalar desde MiKTeX Console
```

### Error: "shell escape not enabled"
Asegúrate de usar `-shell-escape` en la compilación.

### Bibliografía no aparece
Verifica que los archivos `.bib` estén en la carpeta `referencias/` y ejecuta:
1. XeLaTeX
2. Biber
3. XeLaTeX (2 veces)

## 📄 Salida

El documento final será:
- **`poster.pdf`**: Póster completo listo para impresión
- Formato: 50cm × 35cm (A0 personalizado)
- Orientación: Horizontal

---

*Desarrollado para presentación académica de diseño arquitectural de software y patrones.*