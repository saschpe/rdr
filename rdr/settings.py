# -*- coding: utf-8 -*-
# Django settings

import djcelery
import os


DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Sascha Peilicke', 'saschpe@gmx.de'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',  # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'rdr',          # Or path to database file if using sqlite3.
        'USER': 'rdr',          # Not used with sqlite3.
        'PASSWORD': 'rdr',  # Not used with sqlite3.
        'HOST': '',             # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',             # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Berlin'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.abspath(os.path.join(os.path.curdir, 'media'))

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = ''

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
ADMIN_MEDIA_PREFIX = STATIC_URL + 'grappelli/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.abspath('{0}/{1}'.format(os.path.curdir, 'static')),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '7vww19!x1a=(jsmod@pp&#c+4sn65p-f)y(pm$iy%1p^$u_qs%'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Debug Toolbar middleware must come after any other middleware that
    # encodes the response's content (such as GZipMiddleware).
    # Note: Be aware of middleware ordering and other middleware that may
    # intercept requests and return responses. Putting the debug toolbar
    # middleware after the Flatpage middleware, for example, means the toolbar
    # will not show up on flatpages.
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.abspath(os.path.join(os.path.curdir, 'templates'))
)

INSTALLED_APPS = (
    # Third party apps:
    'debug_toolbar',
    'djcelery',
    'grappelli',
    #'gunicorn',
    'kombu.transport.django', #Only used in DEBUG celery settings
    'south',

    # Django core apps:
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Local apps:
    #'apps.accounts',
    'apps.feeds',
)

AUTH_PROFILE_MODULE = 'accounts.UserProfile'

if DEBUG is True:
    LOG_FILE_NAME = 'debug.log'
else:
    LOG_FILE_NAME = 'production.log'

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '[%(asctime)s] %(levelname)s %(module)s %(process)d %(thread)d: %(message)s',
        },
        'simple': {
            'format': '[%(asctime)s] %(levelname)s: %(message)s',
        },
    },
   #'filters': {
   #    'sensitive': {
   #        '()': 'project.logging.SpecialFilter',
   #        'foo': 'bar',
   #    }
   #},
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'django.utils.log.NullHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.WatchedFileHandler',
            'formatter': 'simple',
            'filename': os.path.join(os.path.curdir, 'log', LOG_FILE_NAME),
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
        }
    },
    'loggers': {
        'django': {
            'handlers': ['null'],
            'propagate': True,
            'level': 'INFO',
        },
        'django.request': {
            'handlers': ['mail_admins', 'file'],
            'level': 'ERROR',
            'propagate': False,
        },
        # For performance reasons, SQL logging is only enabled when
        # settings.DEBUG is set to True, regardless of the logging level
        # or handlers that are installed.
        'django.db.backends': {
            'handlers': ['file'],
            'level': 'DEBUG',
        },
        'apps.feeds.models': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
        },
    }
}


# Celery settings:
djcelery.setup_loader()

if DEBUG is True:
    BROKER_URL = 'django://'
    CELERY_RESULT_BACKEND = 'database'
    CELERY_RESULT_DBURI = 'sqlite:///development.sqlite'
else:
    # http://docs.celeryq.org/en/latest/getting-started/brokers/rabbitmq.html
    BROKER_URL = 'amqp://rdruser:rdrpass@localhost:5672/rdr'
    CELERY_RESULT_BACKEND = 'database'
    CELERY_RESULT_DBURI = 'postgresql://user:pass@localhost:1234/database'


# Debug toolbar settings:
INTERNAL_IPS = ('127.0.0.1',)

#def custom_show_toolbar(request):
#    return True # Always show toolbar, for example purposes only.

DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
#    'SHOW_TOOLBAR_CALLBACK': custom_show_toolbar,
#    'EXTRA_SIGNALS': ['myproject.signals.MySignal'],
#    'HIDE_DJANGO_SQL': False,
#    'TAG': 'div',
#    'ENABLE_STACKTRACES' : True,
}


# Grappelli theme settings:
GRAPPELLI_ADMIN_TITLE = 'rdr'
