from django.db.models import Q, QuerySet
from django.contrib.auth.models import User
from .models import Ticket

def obtener_tickets_filtrados(*, filtros: dict, usuario: User) -> QuerySet[Ticket]:
    """
    Retorna un QuerySet de tickets aplicando filtros de búsqueda y propiedad.
    
    Args:
        filtros: Diccionario con parámetros (usualmente request.GET)
        usuario: El usuario que hace la petición (request.user)

    """
    # Optimizacion de data
    qs = Ticket.objects.select_related('asignado_a').all().order_by('-fecha_creacion')

    busqueda = filtros.get('buscar', '').strip()
    mis_tickets = filtros.get('mis_tickets')

    if mis_tickets == 'true' and usuario.is_authenticated:
        qs = qs.filter(asignado_a=usuario)

    if busqueda:
        query_filter = (
            Q(titulo__icontains=busqueda) | 
            Q(descripcion__icontains=busqueda) |
            Q(estado__icontains=busqueda) | 
            Q(asignado_a__username__icontains=busqueda)
        )

        if busqueda.isdigit():
            query_filter = query_filter | Q(id=busqueda)

        qs = qs.filter(query_filter)

    return qs