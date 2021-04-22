"""
WSGI config for YTDPython project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

#from whitenoise.django import DjangoWhiteNoise
from whitenoise import WhiteNoise

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'YTDPython.settings')

application = get_wsgi_application()

# # Prod setting add
application = WhiteNoise(application)
