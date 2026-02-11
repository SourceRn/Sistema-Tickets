from django.db import models
from django.contrib.auth.models import User # Importamos el sistema de usuarios
from .constants import EstadoTicket

class Ticket(models.Model):

    # CAMPOS FIJOS
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    
    # CAMPOS DE GESTION
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=EstadoTicket.choices, default=EstadoTicket.PENDIENTE)
    asignado_a = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    # CAMPO FLEXIBLE
    # default=dict asegura que si no hay datos, guarde un diccionario vacio {}
    datos_extra = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return f"{self.titulo} ({self.estado})"
    
class Comentario(models.Model):
    ticket = models.ForeignKey(Ticket, related_name='comentarios', on_delete=models.CASCADE)
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    texto = models.TextField()

    imagen = models.ImageField(upload_to='comentarios/', null=True, blank=True)
    fecha = models.DateTimeField(auto_now_add=True)

    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='respuestas')

    class Meta:
        ordering = ["fecha"]