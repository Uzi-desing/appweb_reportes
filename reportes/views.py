from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.db import transaction, IntegrityError
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from .models import UsuarioTransportista, ReporteDano, Empleado, Cliente
from .forms import FlexibleLoginForm, ReporteDanoForm, PiezasFormSet, ClienteForm

# Create your views here.
@never_cache
@require_http_methods(["GET", "POST"])
def login_view(request):
    if request.method == 'POST':
        # Instancia el formulario con los datos recibidos del POST
        form = FlexibleLoginForm(request, data=request.POST)  

        # Verifica si el formulario es válido
        if form.is_valid():
            login(request, form.get_user()) # Inicia sesión al usuario autenticado
           
           # Esto sirve para devolver al usuario a la página que intentaba ver antes del login
            next_url = request.GET.get('next') or request.POST.get('next')
            return redirect(next_url if next_url else 'home')
    else:
        form = FlexibleLoginForm()

    return render(request, 'login.html', {'loginForm': form})

@never_cache
@require_http_methods(["GET"])
@login_required(login_url='login')
def home_view(request):
    return render(request, 'home.html')

@require_http_methods(["POST"])
def logout_view(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
@require_http_methods(["GET", "POST"])
def crear_reporte_view(request):
    if request.method == 'POST':
        # 1. Cargamos el formulario con los datos del POST
        form = ReporteDanoForm(request.POST) 

        if form.is_valid():
            # 2. Obtenemos los datos ya validados y limpios
            dni_limpio = form.cleaned_data['dniConductor']
            patente_limpia = form.cleaned_data['patenteConductor']
            nombre = form.cleaned_data['nombreConductor']
            apellido = form.cleaned_data['apellidoConductor']
            transporte = form.cleaned_data['transporte']

            try:
                with transaction.atomic(): # Guarda todo o nada
                    # 3. Actualiza o crea al transportista basado en el DNI
                    conductor, creado = UsuarioTransportista.objects.update_or_create(
                        dni=dni_limpio,
                        defaults={
                            'nombre': nombre,
                            'apellido': apellido,
                            'transporte': transporte,
                            'patente': patente_limpia
                        }
                    )

                    # 4. Se crea el objeto ReporteDano pero sin guardar en la DB
                    reporte = form.save(commit=False)
                    reporte.transportista = conductor # Vinculamos al transportista y la patente al reporte
                    reporte.patente_reporte = patente_limpia
                    # 5. Guarda el reporte en la DB
                    reporte.save() 
                    messages.success(request, 'Reporte creado con éxito')

                    return redirect ('agregar_piezas', reporte_id=reporte.id)
            
            except Exception as e:
                messages.error(request, 'Error técnico al guardar.')
                print(f"Error en crear_reporte: {e}")
        else:
            messages.error(request, "Por favor, corrija los errores indicados en rojo.")
    else:
        # Petición GET: Formulario Vacio
        form = ReporteDanoForm()
    
    return render(request, 'crear_reporte.html', {'form': form})

@login_required(login_url='login')
@require_http_methods(["GET", "POST"])
def agregar_piezas_rechazadas_view(request, reporte_id):
    reporte = get_object_or_404(ReporteDano, id=reporte_id)

    if request.method == 'POST':
        formset = PiezasFormSet(request.POST, request.FILES, instance=reporte, prefix='piezas')
        if formset.is_valid():
           try:
                with transaction.atomic():
                    formset.save()
                    messages.success(request, "Reporte finalizado y piezas guardadas con éxito.")
                return redirect('home')
           
           except Exception as e:
                messages.error(request, "Error al guardar el reporte. Por favor, reintente.")
        else:
            formset.extra = 0
    else:
        formset = PiezasFormSet(instance=reporte, prefix='piezas')

    return render(request, 'agregar_piezas_rechazadas.html', {
        'formset': formset,
        'reporte': reporte
    })

@login_required(login_url='login')
@require_http_methods(['GET'])
def tabla_reportes_view(request):
    # 1. Obtenemos los datos que necesitamos.
    reportes = ReporteDano.objects.select_related('empleado', 'cliente')
    empleados = Empleado.objects.all().order_by('apellido')

    # 2. Capturamos los parametros que necesitamos para filtrar.
    q = request.GET.get('q', '').strip()
    empleado_id = request.GET.get('empleado', '')
    desde = request.GET.get('desde', '')
    hasta = request.GET.get('hasta', '')

    # 3. Aplicación de los filtros.
    if q:
        reportes = reportes.filter(
            Q(id__icontains=q) |
            Q(remito_recepcion__icontains=q) |
            Q(cliente__nombre__icontains=q)
        )
    
    if empleado_id:
        reportes = reportes.filter(empleado_id=empleado_id)

    if desde:
        reportes = reportes.filter(fecha__gte=desde)
    if hasta:
        reportes = reportes.filter(fecha__lte=hasta)

    # Ordenamiento descendente y ascendente.
    sort = request.GET.get('sort', 'id')
    order = request.GET.get('order', 'desc')
    if order == 'desc':
        sort = f"-{sort}"
    reportes = reportes.order_by(sort)

    # Paginacion: Toma todos los reportes pero los envia en trozos de 15 por página.
    paginator = Paginator(reportes, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'reportes': page_obj, 
        'empleados': empleados, 
        'empleado_seleccionado' : int(empleado_id) if empleado_id.isdigit() else None 
    }

    if request.GET.get('ajax') == 'true':
        return render(request, 'partials/filas_reportes.html', context)

    return render(request, 'tabla_reportes.html', context)
    
@login_required(login_url='login')
@require_http_methods(['GET'])
def detalle_reporte_view(request, reporte_id):
    reporte = get_object_or_404(ReporteDano.objects.select_related('empleado', 'cliente', 'transportista').prefetch_related(
        'piezas_rechazadas__pieza__categoria',
        'piezas_rechazadas__categoria_dano'
    ),id=reporte_id)

    return render(request, 'detalle_reporte.html', {'reporte': reporte})

@login_required(login_url='login')
@require_http_methods(['GET', 'POST'])
def registrar_cliente_view(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            try:
                nuevo_cliente = form.save()
                messages.success(request, f"Cliente {nuevo_cliente.nombre} registrado exitosamente.")
                return redirect('home')
            except IntegrityError:
                messages.error(request, "Error interno: Ya existe un registro con esos datos únicos.")
            except Exception as e:
                messages.error(request, "Ocurrió un error inesperado al intentar guardar el cliente. Intente nuevamente.")
        else:
            messages.error(request, "Error al registrar. Por favor, revise los datos ingresados.")
    else:
        form = ClienteForm()
    return render(request, 'registrar_cliente.html', {'form': form})

@login_required(login_url='login')
@require_http_methods(['GET'])
def tabla_clientes_view(request):
    clientes = Cliente.objects.all()

    q = request.GET.get('q', '').strip()
    if q: 
        clientes = clientes.filter(
            Q(nombre__icontains=q)
        )

    sort = request.GET.get('sort', 'nombre')
    order = request.GET.get('orden', 'asc')
    if order == 'desc':
        sort = f"-{sort}"
    clientes = clientes.order_by(sort)

    paginator = Paginator(clientes, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if request.GET.get('ajax') == 'true':
        return render(request, 'partials/filas_clientes.html', {'clientes': page_obj})
    
    return render(request, 'tabla_clientes.html', {'clientes': page_obj})

