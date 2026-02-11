import pandas as pd
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse
from django.utils import timezone
from apps.tickets import services, selectors

@login_required
def subir_tickets(request):
    if not request.user.is_superuser:
        raise Http404()

    if request.method == 'POST' and request.FILES.get('archivo_excel'):
        excel_file = request.FILES['archivo_excel']
        
        try:

            resultados = services.procesar_carga_masiva(
                archivo_excel=excel_file,
                usuario_editor=request.user
            )

            return render(request, 'tickets/resultado_carga.html', resultados)
            
        except ValueError as e:
            messages.error(request, str(e))

        except Exception as e:
            messages.error(request, f"Ocurrió un error al procesar el archivo: {str(e)}")

    return render(request, 'tickets/subir.html')

@login_required
def exportar_tickets_excel(request):
    tickets = selectors.obtener_tickets_filtrados(
        filtros=request.GET,
        usuario=request.user
    )

    data = []

    for t in tickets:
        # A. Datos Fijos
        fecha_fmt = t.fecha_creacion.strftime('%d/%m/%Y %H:%M') if t.fecha_creacion else ''
        asignado = t.asignado_a.username if t.asignado_a else 'Sin asignar'
        
        row = {
            'ID Sistema': t.id,
            'Título': t.titulo,
            'Estado': t.get_estado_display(),
            'Asignado a': asignado,
            'Fecha Creación': fecha_fmt,
            'Descripción': t.descripcion,
        }

        if t.datos_extra and isinstance(t.datos_extra, dict):
            for clave, valor in t.datos_extra.items():
                row[clave.title()] = str(valor)
        
        data.append(row)

    df = pd.DataFrame(data)

    # Limpieza: Rellenar celdas vacías (NaN) con cadena vacía
    df.fillna('', inplace=True)

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    fecha_hoy = timezone.now().strftime('%Y-%m-%d')
    response['Content-Disposition'] = f'attachment; filename="Reporte_Tickets_{fecha_hoy}.xlsx"'

    df.to_excel(response, index=False, engine='openpyxl')

    return response