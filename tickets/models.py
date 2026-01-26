from django.db import models
from django.contrib.auth.models import User # Importamos el sistema de usuarios

class Ticket(models.Model):
    ESTADOS = [
        ('PENDIENTE', 'Pendiente'),
        ('EN_PROCESO', 'En Proceso'),
        ('FINALIZADO', 'Finalizado'),
    ]

    # CAMPOS FIJOS
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    
    # CAMPOS DE GESTION
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='PENDIENTE')
    asignado_a = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    # CAMPO FLEXIBLE
    # default=dict asegura que si no hay datos, guared un diccionario vacio {}
    datos_extra = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return f"{self.titulo} ({self.estado})"