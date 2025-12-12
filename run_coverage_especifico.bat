@echo off
REM Script para ejecutar coverage SOLO de las funcionalidades específicas
REM 1. Crear solicitud
REM 2. Visualizar sus solicitudes
REM 3. Visualizar seguimiento de solicitudes

echo ==========================================
echo Coverage de Funcionalidades Especificas
echo ==========================================
echo.
echo Funcionalidades a medir:
echo 1. Crear solicitud
echo 2. Visualizar sus solicitudes
echo 3. Visualizar seguimiento de solicitudes
echo.

REM Navegar al directorio del proyecto Django
cd app\solicitudes

REM Limpiar datos de coverage anteriores
echo Limpiando datos anteriores...
coverage erase

REM Ejecutar pruebas con coverage solo de tipo_solicitudes
echo.
echo Ejecutando pruebas unitarias...
coverage run --source=tipo_solicitudes manage.py test tipo_solicitudes

REM Generar reporte filtrado solo para los archivos específicos
echo.
echo ==========================================
echo REPORTE DE COVERAGE
echo ==========================================
coverage report --include="*/tipo_solicitudes/views.py,*/tipo_solicitudes/models.py,*/tipo_solicitudes/forms.py" --show-missing

REM Generar reporte HTML
echo.
echo Generando reporte HTML...
coverage html --include="*/tipo_solicitudes/views.py,*/tipo_solicitudes/models.py,*/tipo_solicitudes/forms.py"

echo.
echo ==========================================
echo Reporte HTML generado en: htmlcov\index.html
echo Abre el archivo en tu navegador para ver detalles
echo ==========================================
pause

