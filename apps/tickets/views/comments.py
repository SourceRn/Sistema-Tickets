from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from apps.tickets.models import Ticket, Comentario

@login_required
def agregar_comentario(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    
    if request.method == 'POST':
        texto = request.POST.get('texto_comentario')
        imagen = request.FILES.get('imagen_comentario')
        parent_id = request.POST.get('parent_id')

        parent_comment = None
        if parent_id:
            parent_comment = Comentario.objects.filter(id=parent_id, ticket=ticket).first()

        if texto or imagen:
            Comentario.objects.create(
                ticket=ticket,
                autor=request.user,
                texto=texto,
                imagen=imagen,
                parent=parent_comment
            )
            messages.success(request, "Comentario agregado.")
        else:
            messages.success(request, "El comentario no puede estar vacio.")

    return redirect('detalle_ticket', ticket_id=ticket.id)

