with open('core/views.py', 'a', encoding='utf-8') as f:
    f.write('''

def force_create_all(request):
    from django.db import connection
    from core.models import BienPatrimonial, LogActividad, ServicioExtra, PasswordResetToken
    from django.http import HttpResponse
    try:
        with connection.schema_editor() as schema_editor:
            try: schema_editor.create_model(BienPatrimonial)
            except Exception as e: print(f"Error BienPatrimonial: {e}")
            
            try: schema_editor.create_model(LogActividad)
            except Exception as e: print(f"Error LogActividad: {e}")
            
            try: schema_editor.create_model(ServicioExtra)
            except Exception as e: print(f"Error ServicioExtra: {e}")
            
            try: schema_editor.create_model(PasswordResetToken)
            except Exception as e: print(f"Error PasswordResetToken: {e}")
            
        return HttpResponse("¡Tablas recreadas con éxito! (BienPatrimonial, LogActividad, ServicioExtra, PasswordResetToken)")
    except Exception as e:
        return HttpResponse(f"Error general: {e}")
''')
