with open('core/views.py', 'a', encoding='utf-8') as f:
    f.write('''

def fix_passwords(request):
    from django.http import HttpResponse
    from django.contrib.auth import get_user_model
    User = get_user_model()
    try:
        u = User.objects.get(username="cecilia_hospital")
        u.set_password("Cecilia_2026")
        u.save()
        try:
            admin = User.objects.get(username="admin")
            admin.set_password("Hospit@l1")
            admin.save()
            msg_admin = "y admin a Hospit@l1 "
        except:
            msg_admin = ""
        return HttpResponse(f"Exito. Contraseña reseteada. {msg_admin}")
    except Exception as e:
        return HttpResponse(f"Error: {e}")
''')
