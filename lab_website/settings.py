MESSAGE_STORAGE = 'django.contrib.messages.storage.cookie.CookieStorage'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'vif6db9fb9s8vb&amp;+j*h520)c+38ahyx5#8=)uo_c&amp;0jk#ei^wr'

MIDDLEWARE = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware'
    #'debug_toolbar.middleware.DebugToolbarMiddleware'
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'lab_website.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'lab_website.wsgi.application'
INTERNAL_IPS = ('127.0.0.1',)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.sitemaps',
    'django.contrib.humanize',
    'lab_website',
    'personnel',
    'communication',
    'papers',
    'projects',
    #'debug_toolbar',
    'tastypie'
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'OPTIONS':{
            'context_processors': [
                "communication.context_processors.social_media_accounts",
				"papers.context_processors.api_keys",
				"django.contrib.auth.context_processors.auth",
				"django.template.context_processors.debug",
				"django.template.context_processors.i18n",
                "django.template.context_processors.request",
				"django.template.context_processors.media",
				"django.template.context_processors.static",
				"django.template.context_processors.tz",
                'django.contrib.messages.context_processors.messages'
                ],
            },
    },
]

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
    },
    'loggers': {
        'django.security.DisallowedHost': {
            'handlers': ['null'],
            'propagate': False,
        },
    },
}

# Django 3.2+ requires explicit primary key type for new models.
# This sets the default to BigAutoField to avoid warnings and future-proof migrations.
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# updated to the new form renderer
FORM_RENDERER = 'django.forms.renderers.DjangoTemplates'

# Starting with Django 6.0, forms.URLField will assume 'https://' as the default scheme
# for URLs without one. This setting enables the new behavior now, silencing the deprecation warning.
FORMS_URLFIELD_ASSUME_HTTPS = True

from .localsettings import *

