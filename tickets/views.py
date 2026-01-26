import pandas as pd
import datetime  # <--- IMPORTANTE: Agregamos esto para manejar fechas
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q # Para busquedas avanzadas (OR)
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import Http404
from django.core.paginator import Paginator
from .models import Ticket

# --- Función auxiliar para limpiar datos ---
def limpiar_celda(valor):
    """
    Recibe un valor de celda y lo convierte a algo seguro para JSON.
    Maneja Fechas, Horas y Nulos.
    """
    if pd.isna(valor):
        return ""
    
    # Si es fecha (Timestamp de pandas, datetime de python o date)
    if isinstance(valor, (pd.Timestamp, datetime.datetime, datetime.date)):
        return valor.strftime('%Y-%m-%d %H:%M:%S')
    
    # Si es solo hora (datetime.time)
    if isinstance(valor, datetime.time):
        return valor.strftime('%H:%M:%S')
        
    return valor

@login_required
def subir_tickets(request):
    if not request.user.is_superuser:
        raise Http404()

    if request.method == 'POST' and request.FILES.get('archivo_excel'):
        excel_file = request.FILES['archivo_excel']
        
        try:
            # 1. Leer el archivo
            df = pd.read_excel(excel_file)
            df.columns = df.columns.str.strip()

            # 2. LIMPIEZA PROFUNDA (Versión Compatible Universal)
            # En lugar de applymap, iteramos columna por columna.
            # Esto funciona en TODAS las versiones de Pandas.
            for col in df.columns:
                df[col] = df[col].apply(limpiar_celda)

            # 3. Validar columnas obligatorias
            if 'Titulo' not in df.columns or 'Detalle' not in df.columns:
                messages.error(request, "El Excel debe tener columnas 'Titulo' y 'Detalle'")
                return redirect('subir_tickets')

            # 4. Preparar objetos
            lista_tickets = []

            for index, row in df.iterrows():
                datos_fila = row.to_dict()

                # Extraemos y removemos los fijos
                titulo_ticket = datos_fila.pop('Titulo')
                desc_ticket = datos_fila.pop('Detalle')

                ticket = Ticket(
                    titulo=titulo_ticket,
                    descripcion=desc_ticket,
                    datos_extra=datos_fila, # El resto ya está limpio y es texto
                    estado='PENDIENTE'
                )
                lista_tickets.append(ticket)
            
            # 5. Guardar
            Ticket.objects.bulk_create(lista_tickets)
            
            messages.success(request, f"Se cargaron {len(lista_tickets)} tickets correctamente.")
            return redirect('lista_tickets')
            
        except Exception as e:
            messages.error(request, f"Error al procesar el archivo: {e}")

    return render(request, 'tickets/subir.html')

def lista_tickets(request):
    # 1. Base: Todos los tickets ordenados
    tickets = Ticket.objects.all().order_by('-fecha_creacion')

    # Capturamos los parámetros
    busqueda = request.GET.get('buscar')
    mostrar_mios = request.GET.get('mis_tickets')

    # --- LÓGICA CORREGIDA ---
    
    if busqueda:
        # PRIORIDAD 1: Si hay búsqueda, es GLOBAL (ignora filtro 'mis_tickets')
        tickets = tickets.filter(
            Q(titulo__icontains=busqueda) | 
            Q(descripcion__icontains=busqueda)
        )
    elif mostrar_mios and request.user.is_authenticated:
        # PRIORIDAD 2: Solo si NO hay búsqueda, aplicamos el filtro de usuario
        tickets = tickets.filter(asignado_a=request.user)

    # --- (El resto de contadores y contexto sigue igual) ---
    total_pendientes = Ticket.objects.filter(estado='PENDIENTE').count()
    mis_pendientes = 0
    if request.user.is_authenticated:
        mis_pendientes = Ticket.objects.filter(asignado_a=request.user, estado='EN_PROCESO').count()

    # Configurar Paginación
    paginator = Paginator(tickets, 10) # 10 tickets por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'tickets': page_obj,
        'total_pendientes': total_pendientes,
        'mis_pendientes': mis_pendientes
    }
    
    return render(request, 'tickets/lista.html', context)

@login_required
def tomar_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)

    if not ticket.asignado_a:
        ticket.asignado_a = request.user
        ticket.estado = 'EN_PROCESO'
        ticket.save()
        messages.success(request, f"¡Ticket #{ticket.id} asignado a ti exitosamente!")
    else: 
        messages.warning(request, "Este ticket ya fue tomado por otro usuario.")

    return redirect('lista_tickets')

@login_required
def finalizar_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)

    if ticket.asignado_a == request.user:
        ticket.estado = 'FINALIZADO'
        ticket.save()
        messages.success(request, "¡Buen trabajo! El ticket ha sido finalizado.")
    else:
        # CORRECCIÓN AQUÍ: Era 'message.error', debe ser 'messages.error'
        messages.error(request, "No puedes finalizar un ticket que no te pertenece.")

    return redirect('lista_tickets')

@login_required
def ver_detalle_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    
    # REGLA DE PRIVACIDAD:
    # Si el ticket tiene dueño Y ese dueño NO soy yo (y tampoco soy admin)...
    if ticket.asignado_a and ticket.asignado_a != request.user and not request.user.is_superuser:
        messages.warning(request, "No puedes ver los detalles de un ticket asignado a otro agente.")
        return redirect('lista_tickets')

    return render(request, 'tickets/detalle.html', {'ticket': ticket})

@login_required
def cancelar_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    
    # Solo permitimos cancelar si soy el dueño y no está finalizado
    if ticket.asignado_a == request.user and ticket.estado != 'FINALIZADO':
        ticket.asignado_a = None        # Quitamos al dueño
        ticket.estado = 'PENDIENTE'     # Vuelve a estar disponible
        ticket.save()
        messages.info(request, f"Has liberado el ticket #{ticket.id}. Ahora está visible para todos.")
    else:
        messages.error(request, "No puedes soltar un ticket que ya cerraste o que no es tuyo.")
    
    return redirect('lista_tickets')