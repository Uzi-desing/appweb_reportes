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
ALLOWED_HOSTS = ['*',]

INSTALLED_APPS = [
    'unfold',
    'unfold.contrib.filters',
    'unfold.contrib.forms',
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