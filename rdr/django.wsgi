# -*- coding: utf-8 -*-

from django.core.handlers.wsgi import WSGIHandler

import os
import sys


# Put the Django project on sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
os.environ['DJANGO_SETTINGS_MODULE'] = 'rdr.settings'
os.environ['CELERY_LOADER'] = 'django'
application = WSGIHandler()
