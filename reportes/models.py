from django.db import models
from django.utils import timezone
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
import uuid

from .storage_backend import AzureMediaStorage
from .utils.utils_azure import generate_url_sas


class Categoria(models.Model):
    descripcion = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Categoría de Material'
        verbose_name_plural = 'Categorías de Material'

    def __str__(self):
        return self.descripcion


class CategoriaDano(models.Model):
    motivo = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'Tipo de Daño'
        verbose_name_plural = 'Tipos de Daño'

    def __str__(self):
        return self.motivo


class Rol(models.Model):
    puesto = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'Rol de Usuario'
        verbose_name_plural = 'Roles de Usuario'

    def __str__(self):
        return self.puesto


class Empleado(models.Model):
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=255)
    apellido = models.CharField(max_length=255)
    dni = models.CharField(max_length=20, unique=True)
    telefono = models.CharField(max_length=20)
    mail = models.EmailField(unique=True)

    class Meta:
        verbose_name = 'Empleado'
        verbose_name_plural = 'Empleados'

    def __str__(self):
        return f"{self.nombre} {self.apellido} - {self.rol.puesto}"


class Cliente(models.Model):
    nombre = models.CharField(max_length=255)
    telefono = models.CharField(max_length=20)
    mail = models.EmailField(unique=True)
    domicilio = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'

    def __str__(self):
        return self.nombre


class UsuarioTransportista(models.Model):
    OPCIONES_TRANSPORTE = [
        ('CAMION', 'Camión'),
        ('SEMIREMOLQUE', 'Semirremolque'),
        ('CAMIONETA', 'Camioneta'),
        ('FURGONETA', 'Furgoneta'),
        ('PARTICULAR', 'Particular'),
    ]

    nombre = models.CharField(max_length=255)
    apellido = models.CharField(max_length=255)
    dni = models.CharField(max_length=20, unique=True)
    patente = models.CharField(max_length=20)
    transporte = models.CharField(max_length=20, choices=OPCIONES_TRANSPORTE, default='CAMION')

    class Meta:
        verbose_name = 'Transportista'
        verbose_name_plural = 'Transportistas'

    def __str__(self):
        return f"{self.nombre} {self.apellido} - ({self.patente})"


class Pieza(models.Model):
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    medidas = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Pieza'
        verbose_name_plural = 'Piezas'

    def __str__(self):
        return f"{self.categoria.descripcion} - {self.medidas}"


class ReporteDano(models.Model):
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    transportista = models.ForeignKey(UsuarioTransportista, on_delete=models.CASCADE)
    remito_recepcion = models.CharField(max_length=255, unique=True, editable=False)
    fecha = models.DateField(auto_now_add=True)
    patente_reporte = models.CharField(max_length=20)
    finalizado = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Reporte de Daño'
        verbose_name_plural = 'Reportes de Daño'

    def save(self, *args, **kwargs):
        if not self.remito_recepcion:
            while True:
                nuevo_remito = uuid.uuid4().hex[:12].upper()
                if not ReporteDano.objects.filter(remito_recepcion=nuevo_remito).exists():
                    self.remito_recepcion = nuevo_remito
                    break

        if not self.patente_reporte and self.transportista:
            self.patente_reporte = self.transportista.patente

        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Reporte {self.remito_recepcion}"


class PiezaRechazada(models.Model):
    reporte = models.ForeignKey(ReporteDano, on_delete=models.CASCADE, related_name='piezas_rechazadas')
    pieza = models.ForeignKey(Pieza, on_delete=models.CASCADE)
    categoria_dano = models.ForeignKey(CategoriaDano, on_delete=models.CASCADE)
    observaciones = models.TextField(blank=True, null=True)
    cantidad = models.PositiveIntegerField(default=1)

    imagen = models.ImageField(
        upload_to='images-piezas-rechazadas/',
        storage=AzureMediaStorage(),
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = 'Pieza Rechazada'
        verbose_name_plural = 'Piezas Rechazadas'

    @property
    def url_segura(self):
        if self.imagen:
            return generate_url_sas(self.imagen.name)
        return None

    def save(self, *args, **kwargs):
        procesar = bool(self.imagen and (self.pk is None))

        if self.pk and self.imagen:
            try:
                original = PiezaRechazada.objects.get(pk=self.pk)
                if original.imagen.name != self.imagen.name:
                    procesar = True
            except PiezaRechazada.DoesNotExist:
                procesar = True

        if procesar:
            img = Image.open(self.imagen)
            if img.mode != 'RGB':
                img = img.convert('RGB')
            img.thumbnail((1280, 720), Image.Resampling.LANCZOS)

            output = BytesIO()
            img.save(output, format='JPEG', quality=70, optimize=True)
            output.seek(0)

            nombre_imagen = f"img_{self.reporte.remito_recepcion}_{uuid.uuid4().hex[:8]}.jpg"
            self.imagen.save(nombre_imagen, ContentFile(output.read()), save=False)

        super().save(*args, **kwargs)