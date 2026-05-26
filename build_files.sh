#!/bin/bash

# Instalar dependencias
python3 -m pip install -r requirements.txt --break-system-packages

# Recolectar archivos estáticos
python3 manage.py collectstatic --noinput --clear

# (Las migraciones se realizan localmente o fuera de Vercel para evitar errores de DDL con conexiones Pooled)
