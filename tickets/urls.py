from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_tickets, name='lista_tickets'), # Ruta raiz
    path('importar/', views.subir_tickets, name='subir_tickets'),
    path('tomar/<int:ticket_id>', views.tomar_ticket, name='tomar_ticket'),
    path('finalizar/<int:ticket_id>', views.finalizar_ticket, name='finalizar_ticket'),
    path('detalle/<int:ticket_id>/', views.ver_detalle_ticket, name='detalle_ticket'),
    path('cancelar/<int:ticket_id>/', views.cancelar_ticket, name='cancelar_ticket'),
]
