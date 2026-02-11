from django import forms
from .models import Ticket

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['titulo', 'descripcion', 'asignado_a']

        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Falla en servidor de correos'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Describe el problema detalladamente...'}),
            'asignado_a': forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {
            'titulo': 'Título del Incidente',
            'descripcion': 'Detalle del Problema',
            'asignado_a': 'Asignar a (Opcional)'
        }