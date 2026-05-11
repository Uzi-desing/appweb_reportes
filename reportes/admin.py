from django.contrib import admin
from .models import Categoria, CategoriaDano, Rol, Empleado, Cliente, UsuarioTransportista, Pieza, ReporteDano, PiezaRechazada
# Register your models here.

# Configuracion básica para las tablas maestras
admin.site.register(Categoria)
admin.site.register(CategoriaDano)
admin.site.register(Rol)

@admin.register(Empleado)
class EmpleadoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido', 'dni', 'telefono', 'mail', 'rol')
    search_fields = ('nombre', 'apellido', 'dni', 'mail')
    list_filter = ('rol',)

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'telefono', 'mail', 'domicilio')
    search_fields = ('nombre', 'telefono', 'mail')
    list_filter = ('nombre',)

@admin.register(UsuarioTransportista)
class UsuarioTransportistaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido', 'dni', 'patente', 'transporte')
    search_fields = ('nombre', 'apellido', 'dni', 'patente')
    list_filter = ('transporte',)

@admin.register(Pieza)
class PiezaAdmin(admin.ModelAdmin):
    list_display = ('categoria', 'medidas')
    search_fields = ('medidas',)
    list_filter = ('categoria',)

# Configuracion para las tablas de reportes
class PiezaRechazadaInline(admin.TabularInline):
    model = PiezaRechazada
    extra = 1
    fields = ('pieza', 'categoria_dano', 'cantidad', 'imagen', 'observaciones')

@admin.register(ReporteDano)
class ReporteDanoAdmin(admin.ModelAdmin):
    list_display = ('remito_recepcion', 'fecha', 'cliente', 'transportista', 'patente_reporte')
    list_filter = ('fecha', 'cliente')
    search_fields = ('remito_recepcion', 'cliente__nombre', 'patente_reporte')

    readonly_fields = ('remito_recepcion', 'patente_reporte', 'fecha')
    inlines = [PiezaRechazadaInline]

    fieldsets = (
        ('Información General', {
            'fields': ('remito_recepcion', 'fecha')
        }),
        ('Responsables', {
            'fields': ('empleado', 'cliente', 'transportista', 'patente_reporte')
        }),
    )