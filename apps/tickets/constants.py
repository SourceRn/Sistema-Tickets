from django.db import models

class EstadoTicket(models.TextChoices):
    PENDIENTE = 'PENDIENTE', 'Pendiente'
    EN_PROCESO = 'EN_PROCESO', 'En Proceso'
    FINALIZADO = 'FINALIZADO', 'Finalizado'