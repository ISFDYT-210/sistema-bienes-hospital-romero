#!/bin/bash

# Instalar dependencias
pip install -r requirements.txt

# Recolectar archivos estáticos
python manage.py collectstatic --noinput --clear

# Aplicar migraciones a la base de datos (Neon)
python manage.py migrate --noinput
