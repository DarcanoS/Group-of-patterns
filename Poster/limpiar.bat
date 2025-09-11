@echo off
echo ==========================================
echo Limpiando archivos temporales de LaTeX...
echo ==========================================
echo.

echo Eliminando archivos auxiliares...
del /Q *.aux 2>nul
del /Q *.fdb_latexmk 2>nul
del /Q *.fls 2>nul
del /Q *.log 2>nul
del /Q *.bbl 2>nul
del /Q *.bcf 2>nul
del /Q *.blg 2>nul
del /Q *.run.xml 2>nul
del /Q *.pytxcode 2>nul
del /Q *.synctex.gz 2>nul
del /Q *.nav 2>nul
del /Q *.out 2>nul
del /Q *.snm 2>nul
del /Q *.toc 2>nul
del /Q *.vrb 2>nul
del /Q *.lof 2>nul
del /Q *.lot 2>nul
del /Q *.figlist 2>nul
del /Q *.makefile 2>nul
del /Q *.fignums 2>nul
del /Q *.lol 2>nul
del /Q *.auxlock 2>nul

echo Eliminando archivos auxiliares en subdirectorios...
for /R %%i in (*.aux) do del /Q "%%i" 2>nul
for /R %%i in (*.log) do del /Q "%%i" 2>nul

echo Eliminando directorio _minted-*...
for /D %%i in (_minted-*) do rmdir /S /Q "%%i" 2>nul

echo Eliminando archivos de respaldo...
del /Q *.bak 2>nul
del /Q *.backup 2>nul
del /Q *~ 2>nul

echo Eliminando archivos SVG temporales...
del /Q *.svg.bak 2>nul
del /Q *.svg~ 2>nul

echo Eliminando archivos temporales del sistema...
del /Q .DS_Store 2>nul
del /Q Thumbs.db 2>nul
del /Q *.tmp 2>nul

echo.
echo ==========================================
echo Limpieza completada exitosamente!
echo Archivos mantenidos:
echo   - *.tex ^(archivos fuente^)
echo   - *.bib ^(bibliografia^)
echo   - imgs/ ^(imagenes^)
echo   - formato/ ^(configuracion^)
echo   - *.pdf ^(opcional - edita script si quieres eliminar^)
echo ==========================================
pause
