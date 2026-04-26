from django.db import models
from django.utils import timezone
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
import uuid

# Integración con Azure Blob Storage
from .storage_backend import AzureMediaStorage
from .utils.utils_azure import generate_url_sas

# Create your models here.
class Categoria(models.Model):
    descripcion = models.CharField(max_length=100)

    def __str__(self):
        return self.descripcion

class CategoriaDano(models.Model):
    motivo = models.CharField(max_length=255)

    def __str__(self):
        return self.motivo

class Rol(models.Model):
    puesto = models.CharField(max_length=255)

    def __str__(self):
        return self.puesto

class Empleado(models.Model):
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=255)
    apellido = models.CharField(max_length=255)
    dni = models.CharField(max_length=20, unique=True)
    telefono = models.CharField(max_length=20)
    mail = models.EmailField(unique=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido} - {self.rol.puesto}"

class Cliente(models.Model):
    nombre = models.CharField(max_length=255)
    telefono = models.CharField(max_length=20)
    mail = models.EmailField(unique=True)
    domicilio = models.CharField(max_length=255)

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

    def __str__(self):
        return f"{self.nombre} {self.apellido} - ({self.patente})"

class Pieza(models.Model):
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    medidas = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.categoria.descripcion} - {self.medidas}"

class ReporteDano(models.Model):
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    transportista = models.ForeignKey(UsuarioTransportista, on_delete=models.CASCADE)
    remito_recepcion = models.CharField(max_length=255, unique=True, editable=False)
    fecha = models.DateField(auto_now_add=True)
    patente_reporte = models.CharField(max_length=20)

    def save(self, *args, **kwargs):
        if not self.remito_recepcion:
            # Genera una cadena única de 32 caracteres, toma los primeros 8 caracteres y los convierte a mayúsculas
            nuevo_remito = uuid.uuid4().hex[:8].upper() # Ejemplo: 4F2D8A1B
            self.remito_recepcion = nuevo_remito

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

    @property
    def url_segura(self):
        if self.imagen:
            return generate_url_sas(self.imagen.name)
        return None

    def save(self, *args, **kwargs):
        if self.imagen:
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