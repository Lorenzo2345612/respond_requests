#!/usr/bin/env python
"""
Script para ejecutar las pruebas de aceptación con Behave
"""
import os
import sys
import subprocess

# Configurar el entorno Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'solicitudes.settings')

# Agregar el directorio del proyecto al path
project_dir = os.path.join(os.path.dirname(__file__), 'app', 'solicitudes')
sys.path.insert(0, project_dir)

import django
django.setup()

# Ejecutar Behave
behave_dir = os.path.join(os.path.dirname(__file__), 'pruebas_aceptacion')
os.chdir(behave_dir)

print("=" * 70)
print("EJECUTANDO PRUEBAS DE ACEPTACIÓN")
print("=" * 70)
print(f"Directorio: {behave_dir}")
print()

result = subprocess.run(['behave'], cwd=behave_dir)
sys.exit(result.returncode)
