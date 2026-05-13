"""
Django settings for core project.
"""

from pathlib import Path
from django.templatetags.static import static
from dotenv import load_dotenv
import os

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
DEBUG = os.getenv('DEBUG', 'False') == 'True'
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

INSTALLED_APPS = [
    'unfold',
    'unfold.contrib.filters',
    'unfold.contrib.forms',
    'axes',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'reportes',
    'django_q',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'axes.middleware.AxesMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('POSTGRES_DB'),
        'USER': os.getenv('POSTGRES_USER'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
        'HOST': os.getenv('POSTGRES_HOST'),
        'PORT': os.getenv('POSTGRES_PORT'),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# --- Seguridad HTTPS ---
SECURE_SSL_REDIRECT = os.getenv('SECURE_SSL_REDIRECT', 'False') == 'True'
SECURE_HSTS_SECONDS = int(os.getenv('SECURE_HSTS_SECONDS', 31536000)) # 1 Año
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# --- Cookies seguras ---
SESSION_COOKIE_SECURE = os.getenv('SESSION_COOKIE_SECURE', 'True') == 'True'
CSRF_COOKIE_SECURE = os.getenv('CSRF_COOKIE_SECURE', 'True') == 'True'

SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'


LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = os.getenv('EMAIL_PORT')
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS')
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')

Q_CLUSTER = {
    'name': 'ecva_cluster',
    'workers': 4,
    'recycle': 500,
    'timeout': 60,
    'compress': True,
    'save_limit': 250,
    'queue_limit': 500,
    'cpu_affinity': 1,
    'label': 'Tareas en Segundo Plano',
    'orm': 'default'
}

# --- Rate Limiting para Login (django-axes) ---
AXES_FAILURE_LIMIT = 5
AXES_LOCK_OUT_AT_FAILURE = True
AXES_COOLOFF_TIME = 0.5
AXES_ONLY_LOGIN_FAILURES = True
AXES_IP_WHITELIST = ['127.0.0.1', '::1']
AXES_LOCKOUT_TEMPLATE = 'locked.html'

AUTHENTICATION_BACKENDS = [
    'axes.backends.AxesBackend',
    'django.contrib.auth.backends.ModelBackend',
]

# --- Estilo del admin site con Unfold ---
UNFOLD = {
    "SITE_TITLE": "ECVA Reportes",
    "SITE_HEADER": "Sistema de Gestión ECVA",
    "SITE_URL": "/",
    
    "SITE_LOGO": {
        "light": lambda request: static("images/logo.png"),
        "dark": lambda request: static("images/logo.png"),
    },
    "SITE_FAVICON": lambda request: static("images/logo.png"),
    "SITE_SYMBOL": "speed",  
    
    "THEME": "light",
    
    "COLORS": {
        "primary": {
            "50": "#ffeaea",
            "100": "#ffc7c7",
            "200": "#ff9e9e",
            "300": "#ff7676",
            "400": "#ff4d4d",
            "500": "#fe2020",
            "600": "#e61c1c",
            "700": "#cc1818",
            "800": "#b31414",
            "900": "#991010"
        },
    },
    
    "SIDEBAR": {
        "show_search": True,
        "show_all_applications": False,
        "navigation": [
            {
                "title": "PRINCIPAL",
                "separator": True,
                "items": [
                    {
                        "title": "Dashboard Admin",
                        "icon": "dashboard",
                        "link": lambda request: "/admin/",
                    },
                    {
                        "title": "Ir al Sitio Web",
                        "icon": "home",
                        "link": lambda request: "/",
                    },
                ],
            },
            {
                "title": "OPERACIONES",
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": "Reportes de Daño",
                        "icon": "report_problem",
                        "link": lambda request: "/admin/reportes/reportedano/",
                    },
                    {
                        "title": "Piezas Rechazadas",
                        "icon": "block",
                        "link": lambda request: "/admin/reportes/piezarechazada/",
                    },
                ],
            },
            {
                "title": "CATÁLOGOS Y MAESTROS",
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": "Clientes",
                        "icon": "people",
                        "link": lambda request: "/admin/reportes/cliente/",
                    },
                    {
                        "title": "Personal (Empleados)",
                        "icon": "badge",
                        "link": lambda request: "/admin/reportes/empleado/",
                    },
                    {
                        "title": "Transporte (Choferes)",
                        "icon": "local_shipping",
                        "link": lambda request: "/admin/reportes/usuariotransportista/",
                    },
                    {
                        "title": "Catálogo de Piezas",
                        "icon": "inventory_2",
                        "link": lambda request: "/admin/reportes/pieza/",
                    },
                ],
            },
            {
                "title": "CONFIGURACIÓN TÉCNICA",
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": "Categorías de Material",
                        "icon": "category",
                        "link": lambda request: "/admin/reportes/categoria/",
                    },
                    {
                        "title": "Tipos de Daño",
                        "icon": "warning",
                        "link": lambda request: "/admin/reportes/categoriadano/",
                    },
                    {
                        "title": "Roles de Usuario",
                        "icon": "admin_panel_settings",
                        "link": lambda request: "/admin/reportes/rol/",
                    },
                ],
            },
        ],
    },
}