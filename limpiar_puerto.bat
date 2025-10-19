@echo off
REM Script para liberar el puerto 8000 y matar procesos de Python
REM Creado para facilitar el desarrollo con FastAPI

echo ========================================
echo   Limpiador de Puerto 8000
echo ========================================
echo.

echo Buscando procesos en el puerto 8000...
echo.

REM Buscar el PID del proceso que usa el puerto 8000
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8000') do (
    set PID=%%a
)

REM Verificar si se encontró un proceso
if defined PID (
    echo Proceso encontrado con PID: %PID%
    echo Terminando proceso...
    taskkill /PID %PID% /F
    echo.
    echo [OK] Proceso terminado exitosamente
) else (
    echo [INFO] No se encontraron procesos usando el puerto 8000
)

echo.
echo ========================================
echo   Limpieza Completa
echo ========================================
echo.
echo Puedes ejecutar tu aplicacion ahora
echo.
pause