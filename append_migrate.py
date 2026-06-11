with open('core/views.py', 'a', encoding='utf-8') as f:
    f.write('''

def force_migrate(request):
    from django.core.management import call_command
    from django.http import HttpResponse
    try:
        call_command("migrate", interactive=False)
        return HttpResponse("¡Migración exitosa en Vercel Postgres!")
    except Exception as e:
        return HttpResponse(f"Error al migrar: {e}")
''')
