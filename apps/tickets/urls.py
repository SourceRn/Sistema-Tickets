from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_tickets, name='lista_tickets'), # Ruta raiz
    path('importar/', views.subir_tickets, name='subir_tickets'),
    path('tomar/<int:ticket_id>', views.tomar_ticket, name='tomar_ticket'),
    path('finalizar/<int:ticket_id>', views.finalizar_ticket, name='finalizar_ticket'),
    path('detalle/<int:ticket_id>/', views.ver_detalle_ticket, name='detalle_ticket'),
    path('cancelar/<int:ticket_id>/', views.cancelar_ticket, name='cancelar_ticket'),
    path('ticket/<int:ticket_id>/comentar/', views.agregar_comentario, name='agregar_comentario'),
    path('crear/', views.crear_ticket_manual, name='crear_ticket'),
    path('exportar/', views.exportar_tickets_excel, name='exportar_excel'),
]
