from django.contrib import admin
from unfold.admin import ModelAdmin as UnfoldModelAdmin
from unfold.contrib.inlines.admin import TabularInline as UnfoldTabularInline
from .models import Categoria, CategoriaDano, Rol, Empleado, Cliente, UsuarioTransportista, Pieza, ReporteDano, PiezaRechazada

admin.site.site_header = "ECVA - Panel de Administración"
admin.site.site_title = "ECVA Reportes"
admin.site.index_title = "Gestión de Reportes de Daño"


@admin.register(Categoria)
class CategoriaAdmin(UnfoldModelAdmin):
    list_display = ['id', 'descripcion']
    search_fields = ['descripcion']
    ordering = ['descripcion']


@admin.register(CategoriaDano)
class CategoriaDanoAdmin(UnfoldModelAdmin):
    list_display = ['id', 'motivo']
    search_fields = ['motivo']
    ordering = ['motivo']


@admin.register(Rol)
class RolAdmin(UnfoldModelAdmin):
    list_display = ['id', 'puesto']
    search_fields = ['puesto']
    ordering = ['puesto']


@admin.register(Empleado)
class EmpleadoAdmin(UnfoldModelAdmin):
    list_display = ['nombre', 'apellido', 'dni', 'telefono', 'mail', 'rol']
    search_fields = ['nombre', 'apellido', 'dni', 'mail']
    list_filter = ['rol']
    ordering = ['apellido', 'nombre']


@admin.register(Cliente)
class ClienteAdmin(UnfoldModelAdmin):
    list_display = ['nombre', 'telefono', 'mail', 'domicilio']
    search_fields = ['nombre', 'telefono', 'mail', 'domicilio']
    ordering = ['nombre']


@admin.register(UsuarioTransportista)
class UsuarioTransportistaAdmin(UnfoldModelAdmin):
    list_display = ['nombre', 'apellido', 'dni', 'patente', 'transporte']
    search_fields = ['nombre', 'apellido', 'dni', 'patente']
    list_filter = ['transporte']
    ordering = ['apellido', 'nombre']


@admin.register(Pieza)
class PiezaAdmin(UnfoldModelAdmin):
    list_display = ['id', 'categoria', 'medidas']
    search_fields = ['medidas', 'categoria__descripcion']
    list_filter = ['categoria']
    ordering = ['categoria__descripcion', 'medidas']


class PiezaRechazadaInline(UnfoldTabularInline):
    model = PiezaRechazada
    extra = 0
    fields = ['pieza', 'categoria_dano', 'cantidad', 'observaciones']
    readonly_fields = ['pieza', 'categoria_dano', 'cantidad', 'observaciones']


@admin.register(ReporteDano)
class ReporteDanoAdmin(UnfoldModelAdmin):
    list_display = ['remito_recepcion', 'fecha', 'cliente', 'empleado', 'finalizado']
    search_fields = ['remito_recepcion', 'cliente__nombre', 'patente_reporte']
    list_filter = ['fecha', 'cliente', 'empleado', 'finalizado']
    ordering = ['-fecha']

    readonly_fields = ['remito_recepcion', 'patente_reporte', 'fecha']
    inlines = [PiezaRechazadaInline]

    fieldsets = (
        ('Información General', {
            'fields': ('remito_recepcion', 'fecha')
        }),
        ('Responsables', {
            'fields': ('empleado', 'cliente', 'transportista', 'patente_reporte')
        }),
        ('Estado', {
            'fields': ('finalizado',)
        }),
    )