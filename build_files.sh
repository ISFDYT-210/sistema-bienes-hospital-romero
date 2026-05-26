#!/bin/bash

# Instalar dependencias
python3 -m pip install -r requirements.txt --break-system-packages

# Recolectar archivos estáticos
python3 manage.py collectstatic --noinput --clear

# Aplicar migraciones a la base de datos (Neon)
python3 manage.py migrate --noinput
