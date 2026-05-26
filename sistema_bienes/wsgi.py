import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_bienes.settings.development')


application = get_wsgi_application()

# Alias para compatibilidad con el entorno Serverless de Vercel
app = application