from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from apps.tickets.models import Ticket
from apps.tickets.forms import TicketForm
from apps.tickets import selectors 
from apps.tickets.constants import EstadoTicket

@login_required
def lista_tickets(request):

    tickets = selectors.obtener_tickets_filtrados(
        filtros=request.GET,
        usuario=request.user
    )

    total_pendientes = Ticket.objects.filter(estado=EstadoTicket.PENDIENTE).count()
    mis_pendientes = 0
    if request.user.is_authenticated:
        mis_pendientes = Ticket.objects.filter(asignado_a=request.user, estado=EstadoTicket.EN_PROCESO).count()

    paginator = Paginator(tickets, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'tickets/lista.html', {
        'tickets': page_obj,
        'total_pendientes': total_pendientes,
        'mis_pendientes': mis_pendientes,
    })

@login_required
def ver_detalle_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)

    comentarios_raiz = ticket.comentarios.filter(parent__isnull=True).order_by('fecha')
    
    return render(request, 'tickets/detalle.html', {
        'ticket': ticket,
        'comentarios': comentarios_raiz
    })

@login_required
def crear_ticket_manual(request):
    if not request.user.is_superuser:
        messages.error(request, "Solo administradores pueden crear tickets manualmente.")
        return redirect('lista_tickets')
    
    if request.method == 'POST':
        form = TicketForm(request.POST)

        if form.is_valid():
            ticket = form.save(commit=False)
            
            ticket.id_referencia = ticket.titulo.upper()
            
            ticket.estado = EstadoTicket.PENDIENTE
            
            keys = request.POST.getlist('extra_keys[]')
            values = request.POST.getlist('extra_values[]')

            datos_json = {}

            for k, v in zip(keys, values):
                if k.strip() and v.strip():
                    datos_json[k.strip()] = v.strip()

            ticket.datos_extra = datos_json
            
            ticket.save()
            
            messages.success(request, f"Ticket '{ticket.titulo}' creado exitosamente.")
            return redirect('lista_tickets')
    else:
        form = TicketForm()

    return render(request, 'tickets/crear_ticket.html', {'form': form})

@login_required
def tomar_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)

    if not ticket.asignado_a:
        ticket.asignado_a = request.user
        ticket.estado = EstadoTicket.EN_PROCESO
        ticket.save()
        messages.success(request, f"¡Ticket #{ticket.id} asignado a ti exitosamente!")
    else: 
        messages.warning(request, "Este ticket ya fue tomado por otro usuario.")

    return redirect('lista_tickets')

@login_required
def finalizar_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)

    if ticket.asignado_a == request.user or request.user.is_superuser:
        ticket.estado = EstadoTicket.FINALIZADO
        ticket.save()
        messages.success(request, "¡Buen trabajo! El ticket ha sido finalizado.")
    else:
        messages.error(request, "No puedes finalizar un ticket que no te pertenece.")

    return redirect('lista_tickets')

@login_required
def cancelar_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    
    if (ticket.asignado_a == request.user or request.user.is_superuser) and ticket.estado != 'FINALIZADO':
        ticket.asignado_a = None        
        ticket.estado = EstadoTicket.PENDIENTE    
        ticket.save()
        messages.info(request, f"Has liberado el ticket #{ticket.id}. Ahora está visible para todos.")
    else:
        messages.error(request, "No puedes soltar un ticket que ya cerraste o que no es tuyo.")
    
    return redirect('lista_tickets')