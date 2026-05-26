import os
from django.core.wsgi import get_wsgi_application

if os.environ.get('VERCEL') == '1':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_bienes.settings.production')
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_bienes.settings.development')


application = get_wsgi_application()

# Alias para compatibilidad con el entorno Serverless de Vercel
app = application