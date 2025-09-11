import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# Es recomendable usar una variable de entorno para esto en producción real,
# pero para PythonAnywhere gratuito, puedes mantenerla aquí por simplicidad si no es sensible.
SECRET_KEY = 'django-insecure-tu_secret_key_aqui' # <-- ¡Cambia esto por tu clave actual!


# SECURITY WARNING: don't run with debug turned on in production!
# ¡MUY IMPORTANTE! En PythonAnywhere (producción), DEBUG debe ser False.
DEBUG = False

# Añade el dominio de tu aplicación en PythonAnywhere.
# Reemplaza 'tu_nombre_de_usuario' con el nombre de usuario que elegiste en PythonAnywhere.
ALLOWED_HOSTS = ['127.0.0.1', 'localhost', 'tu_nombre_de_usuario.pythonanywhere.com']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework', # Si usas Django REST Framework
    'corsheaders',    # Si usas django-cors-headers
    'blog',           # Tu aplicación de blog
    # 'sentry_sdk',   # Si lo tenías y no lo necesitas en PA simple, puedes comentarlo
    # 'rest_framework_simplejwt', # Si lo tenías y no lo necesitas en PA simple, puedes comentarlo
]

MIDDLEWARE = [
    # WhiteNoise debe ser el primer middleware después de SecurityMiddleware para servir estáticos eficientemente
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # <-- AÑADIDO / MOVIDO AQUÍ
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware', # Si lo usas
]

ROOT_URLCONF = 'mi_sitio_web.urls' # <-- Reemplaza 'mi_sitio_web' si tu proyecto principal tiene otro nombre

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'mi_sitio_web.wsgi.application' # <-- Reemplaza 'mi_sitio_web' si tu proyecto principal tiene otro nombre


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases
# En PythonAnywhere gratuito, la opción más sencilla es SQLite.
# Ignoramos la configuración de Redis/PostgreSQL para este despliegue.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'es-ar' # Puedes ajustar esto si ya lo tienes diferente

TIME_ZONE = 'America/Argentina/Buenos_Aires' # <-- ¡Ajustado para Buenos Aires!
USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles') # <-- Aquí se recolectarán los estáticos

# Configuración para que WhiteNoise comprima y cachee los archivos estáticos
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# Media files (archivos subidos por usuarios)
# Si tu blog permite subir imágenes, necesitarás estas líneas
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media') # <-- Aquí se guardarán los archivos subidos


# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Configuración de CORS si la usas
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000", # Por ejemplo, si tienes un frontend React/Vue
    "http://tu_nombre_de_usuario.pythonanywhere.com",
    # ... otras URLs permitidas para CORS
]

# Si usas Django REST Framework, puede que tengas alguna configuración aquí
# REST_FRAMEWORK = {
#     'DEFAULT_AUTHENTICATION_CLASSES': (
#         'rest_framework_simplejwt.authentication.JWTAuthentication',
#     ),
#     'DEFAULT_PERMISSION_CLASSES': (
#         'rest_framework.permissions.IsAuthenticated', # O IsAuthenticatedOrReadOnly
#     ),
# }