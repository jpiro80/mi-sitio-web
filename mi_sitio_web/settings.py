import os
from pathlib import Path

# ... otras configuraciones (BASE_DIR, DEBUG, SECRET_KEY, ALLOWED_HOSTS, etc.) ...

INSTALLED_APPS = [
    # ... tus apps ...
    'django.contrib.staticfiles',
    # ...
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # ¡DEBE IR AQUÍ!
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ... otras configuraciones (ROOT_URLCONF, TEMPLATES, WSGI_APPLICATION, DATABASES, etc.) ...

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'

# MUY IMPORTANTE: STATIC_ROOT debe apuntar al directorio donde collectstatic copia los archivos.
# En Render, el proyecto está en '/opt/render/project/src/'.
# Si collectstatic copió a '/opt/render/project/src/staticfiles',
# entonces os.path.join(BASE_DIR, 'staticfiles') es correcto.
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Si tienes carpetas de estáticos adicionales no dentro de las apps, las pondrías aquí.
# Por defecto para el admin de Django, esto debería estar vacío o no ser la causa.
STATICFILES_DIRS = []

# Configuración de Whitenoise para compresión y caché (agrega esto si no está)
# Asegúrate de que este setting esté presente
STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# ... MEDIA_URL, MEDIA_ROOT, etc. ...