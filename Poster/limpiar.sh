#!/bin/bash

echo "=========================================="
echo "Limpiando archivos temporales de LaTeX..."
echo "=========================================="
echo

# Archivos auxiliares de LaTeX
echo "Eliminando archivos auxiliares..."
rm -f *.aux *.fdb_latexmk *.fls *.log *.bbl *.bcf *.blg *.run.xml *.pytxcode *.synctex.gz
rm -f *.nav *.out *.snm *.toc *.vrb *.lof *.lot *.figlist *.makefile *.fignums *.lol
rm -f *.auxlock

# Archivos temporales en subdirectorios
echo "Eliminando archivos auxiliares en subdirectorios..."
find . -name "*.aux" -type f -delete
find . -name "*.log" -type f -delete

# Directorio de minted
echo "Eliminando directorio _minted-*..."
rm -rf _minted-*

# Archivos de respaldo
echo "Eliminando archivos de respaldo..."
rm -f *.bak *.backup *~

# Archivos SVG temporales
echo "Eliminando archivos SVG temporales..."
rm -f *.svg.bak *.svg~

# Archivos temporales del sistema
echo "Eliminando archivos temporales del sistema..."
rm -f .DS_Store Thumbs.db *.tmp

echo "Eliminando PDF..."
rm -f poster.pdf

echo
echo "=========================================="
echo "Limpieza completada exitosamente!"
echo "Archivos mantenidos:"
echo "  - *.tex (archivos fuente)"
echo "  - *.bib (bibliografía)"  
echo "  - imgs/ (imágenes)"
echo "  - formato/ (configuración)"
echo "  - *.pdf (opcional - descomenta línea si quieres eliminar)"
echo "=========================================="
