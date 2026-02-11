import pandas as pd
from django.db import transaction
from .models import Ticket, Comentario
from datetime import datetime, date, time
from .constants import EstadoTicket

def limpiar_celda(valor):
    if pd.isna(valor): return ""

    if isinstance(valor, (pd.Timestamp, datetime, date)):
        return valor.strftime('%Y-%m-%d %H:%M:%S')
    
    if isinstance(valor, time):
        return valor.strftime('%H:%M:%S')
    
    return valor

def procesar_carga_masiva(archivo_excel, usuario_editor):
    """
    Procesa el Excel y devuelve un diccionario con los resultados.
    Lanza ValueError si el archivo no es válido.

    """
    try:
        df = pd.read_excel(archivo_excel)
        df.columns = df.columns.str.strip()

        # Archivo valido
        if 'Titulo' not in df.columns or 'Detalle' not in df.columns:
            raise ValueError("El Excel debe tener columnas 'Titulo' y 'Detalle'")

        # Sanitizacion de datos
        for col in df.columns:
            df[col] = df[col].apply(limpiar_celda)
            
        resumen = {
            'creados': 0,
            'actualizados': 0,
            'detalles': [],
        }

        with transaction.atomic():
            for _, row in df.iterrows():
                datos_fila = row.to_dict()
                titulo_ticket = datos_fila.pop('Titulo', 'Sin Titulo').strip()
                desc_ticket = datos_fila.pop('Detalle', 'Sin descripcion')
                
                if not titulo_ticket:
                    continue

                
                ticket_existente = Ticket.objects.select_for_update().filter(titulo=titulo_ticket).first()

                if not ticket_existente:
                    Ticket.objects.create(
                        titulo=titulo_ticket,
                        descripcion=desc_ticket,
                        datos_extra=datos_fila,
                        estado=EstadoTicket.PENDIENTE
                    )
                    resumen['creados'] += 1
                else: 
                    cambios = []
                    if ticket_existente.descripcion != desc_ticket:
                        ticket_existente.descripcion = desc_ticket
                        cambios.append("Descripcion Actualizada")

                    # Podria necesitar futuros cambios segun 
                    # cambie la complejidad del campo JSON
                    if ticket_existente.datos_extra != datos_fila:
                        ticket_existente.datos_extra = datos_fila
                        cambios.append("Datos del excel (columnas extra)")

                    if cambios:
                        ticket_existente.save()
                        resumen['actualizados'] += 1

                        motivos = ", ".join(cambios)

                        # Guardar en el reporte para la vista
                        resumen['detalles'].append({
                            'id': ticket_existente.id,
                            'titulo': ticket_existente.titulo,
                            'motivos': motivos
                        })

                        # Crear comentario de auditoria
                        Comentario.objects.create(
                            ticket=ticket_existente,
                            autor=usuario_editor,
                            texto=f"SISTEMA: Actualización masiva. Cambios: {motivos}."
                        )
            return resumen
        
    except Exception as e:
        raise e