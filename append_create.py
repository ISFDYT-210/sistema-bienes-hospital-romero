with open('core/views.py', 'a', encoding='utf-8') as f:
    f.write('''

def force_create(request):
    from django.db import connection
    from core.models import BienPatrimonial
    from django.http import HttpResponse
    try:
        with connection.schema_editor() as schema_editor:
            schema_editor.create_model(BienPatrimonial)
        return HttpResponse("¡Tabla BienPatrimonial recreada con éxito!")
    except Exception as e:
        return HttpResponse(f"Error: {e}")
''')
