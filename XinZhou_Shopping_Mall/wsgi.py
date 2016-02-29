"""
WSGI config for First project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""

import os
import sys
from django.core.wsgi import get_wsgi_application

sys.path.append('D:/Work/Chinese_Shopping_Mall')
os.environ["DJANGO_SETTINGS_MODULE"] = "XinZhou_Shopping_Mall.settings"

application = get_wsgi_application()
