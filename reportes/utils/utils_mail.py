from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from ..models import ReporteDano
from .utils_pdf import GeneradorReportePDF

def enviar_reporte_cliente(reporte_id):
    try:
        reporte = ReporteDano.objects.select_related('cliente', 'empleado', 'transportista').prefetch_related(
            'piezas_rechazadas__pieza__categoria',
            'piezas_rechazadas__categoria_dano'
        ).get(id=reporte_id)

        generador = GeneradorReportePDF(reporte)
        pdf_content = generador.generar()

        subject = f"Reporte de Rechazo de Materiales - {reporte.cliente.nombre} N°{reporte.remito_recepcion}"
        cliente_texto = reporte.cliente.nombre.title()
        context = {
            'cliente': cliente_texto,
            'remito': reporte.remito_recepcion,
        }

        html_message = render_to_string('mails/reporte_cliente.html', context)
        plain_message = strip_tags(html_message)

        email = EmailMultiAlternatives(
            subject=subject,
            body=plain_message,
            from_email=settings.EMAIL_HOST_USER,
            to=[reporte.cliente.mail]
        )

        email.attach_alternative(html_message, "text/html")
        nombre_archivo = f"Reporte_{reporte.id}_{reporte.cliente.nombre.title()}.pdf"
        email.attach(nombre_archivo, pdf_content, 'application/pdf')
        email.send(fail_silently=False)

        return True
    except Exception as e:
        print(f"Error enviando correo: {e}")
        return False

    


