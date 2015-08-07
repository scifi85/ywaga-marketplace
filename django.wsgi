import os
import sys

path = '/var/www'
if path not in sys.path:
    sys.path.insert(0, '/var/www/ywaga')
sys.path.insert(0, '/var/www/apps')

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
