@echo off
echo ====================================
echo Compilando poster LaTeX...
echo ====================================
echo.

echo [1/4] Primera compilacion con XeLaTeX...
xelatex -shell-escape poster.tex
if %errorlevel% neq 0 (
    echo ERROR: Fallo en la primera compilacion
    pause
    exit /b 1
)

echo.
echo [2/4] Procesando bibliografia con Biber...
biber poster
if %errorlevel% neq 0 (
    echo ERROR: Fallo en el procesamiento de bibliografia
    pause
    exit /b 1
)

echo.
echo [3/4] Segunda compilacion con XeLaTeX...
xelatex -shell-escape poster.tex
if %errorlevel% neq 0 (
    echo ERROR: Fallo en la segunda compilacion
    pause
    exit /b 1
)

echo.
echo [4/4] Tercera compilacion con XeLaTeX...
xelatex -shell-escape poster.tex
if %errorlevel% neq 0 (
    echo ERROR: Fallo en la tercera compilacion
    pause
    exit /b 1
)

echo.
echo ====================================
echo Compilacion completada exitosamente!
echo Archivo generado: poster.pdf
echo ====================================
pause
