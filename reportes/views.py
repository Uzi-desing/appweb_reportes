from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from .forms import FlexibleLoginForm

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