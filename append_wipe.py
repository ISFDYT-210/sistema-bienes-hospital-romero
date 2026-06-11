with open('core/views.py', 'a', encoding='utf-8') as f:
    f.write('''

def force_wipe(request):
    from core.models import BienPatrimonial, LogActividad, Expediente, Notificacion, ArchivoCargaMasiva
    from django.http import HttpResponse
    
    try:
        bienes_count, _ = BienPatrimonial.objects.all().delete()
        logs_count, _ = LogActividad.objects.all().delete()
        archivos_count, _ = ArchivoCargaMasiva.objects.all().delete()
        expedientes_count, _ = Expediente.objects.all().delete()
        notificaciones_count, _ = Notificacion.objects.all().delete()
        
        return HttpResponse(f"""
            <h3>¡Base de datos limpiada con éxito!</h3>
            <ul>
                <li>Bienes Patrimoniales eliminados: {bienes_count}</li>
                <li>Logs de Actividad eliminados: {logs_count}</li>
                <li>Archivos de Carga Masiva eliminados: {archivos_count}</li>
                <li>Expedientes eliminados: {expedientes_count}</li>
                <li>Notificaciones eliminadas: {notificaciones_count}</li>
            </ul>
            <p><strong>Los usuarios (administradores, supervisores, operadores) se han mantenido intactos.</strong></p>
        """)
    except Exception as e:
        return HttpResponse(f"Error general: {e}")
''')
