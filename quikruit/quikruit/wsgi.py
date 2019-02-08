"""
WSGI config for quikruit project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/
"""

import os
import sys
from django.core.wsgi import get_wsgi_application

sys.path.append('/opt/bitnami/apps/django/django_projects/PROJECT')
os.environ.setdefault("PYTHON_EGG_CACHE", "/opt/bitnami/apps/django/django_projects/quikruit/egg_cache")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quikruit.settings')
application = get_wsgi_application()
