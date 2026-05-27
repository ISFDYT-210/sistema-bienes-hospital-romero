import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_bienes.settings.development')
django.setup()

from django.test import RequestFactory
from core.views import reportes_view
from django.contrib.auth import get_user_model

User = get_user_model()
u = User.objects.get(username="cecilia_hospital")

factory = RequestFactory()
request = factory.get('/reportes/')
request.user = u

try:
    response = reportes_view(request)
    print("Response status:", response.status_code)
except Exception as e:
    import traceback
    traceback.print_exc()
