from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('home/', views.home_view, name='home'),
    path('reporte/nuevo/', views.crear_reporte_view, name='crear_reporte'),
    path('reporte/<int:reporte_id>/piezas/', views.agregar_piezas_rechazadas_view, name='agregar_piezas'),
    path('reportes/', views.tabla_reportes_view, name='tabla_reportes'),
]