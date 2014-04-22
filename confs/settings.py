"""
Django settings for ws_scalable project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import environ
root = environ.Path(__file__) -1
env = environ.Env(DEBUG=(bool, False), DATABASE_URL=(str, "sqlite:////"+root("../")+"/ws_scalable.db"))
env.read_env(root('../.env'))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env("DEBUG")
TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = []

SITE_ID=1

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
	'south',
#	'vanilla',
	'django_extensions',
#	'sphinxdoc',	
	'apps.campaign',
	'apps.archives',
	'apps.dataviewer',
	'apps.researchobjects',
	'apps.wsusers',
	#'apps.workflow',
	'apps.jobs',
	'provider',
    'provider.oauth2',
    'tastypie_swagger',
    #'object_permissions',
    'tastypie',
#	'apps.apiv1',
#	'vendor.rest_framework_swagger',
#	'debug_toolbar',
#	'rest_framework',
	'rdflib_django',
	'apps.wsadmin',
	'django_statsd',
	
)

TASTYPIE_SWAGGER_API_MODULE = 'confs.urls.v1_api'

AUTHENTICATION_BACKENDS = ("django.contrib.auth.backends.ModelBackend",)
AUTH_USER_MODEL = "wsusers.WSUser"

MIDDLEWARE_CLASSES = (
	'django_statsd.middleware.GraphiteRequestTimingMiddleware',
    'django_statsd.middleware.GraphiteMiddleware',
    'django_statsd.middleware.TastyPieRequestTimingMiddleware',
    #'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

#STATSD_PATCHES = [
#        'django_statsd.patches.db',
#]

STATSD_CLIENT = 'django_statsd.clients.normal'

STATSD_HOST = '10.0.3.150'
STATSD_PORT = 8125
STATSD_PREFIX = None
STATSD_MAXUDPSIZE = 512


ROOT_URLCONF = 'confs.urls'

WSGI_APPLICATION = 'confs.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases


DATABASE_ROUTERS = ["confs.database_router.TripleRouter","confs.database_router.DefaultRouter",]

DATABASES = {   
	'default': env.db('DATABASE_URL'),
	'triple': env.db('TRIPLE_DB_URL'),
}


# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = "en-uk"

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

MEDIA_ROOT = env("STATIC_MEDIA_PATH")+"media"
#DEV_MEDIA_ROOT = root('../dev_media')

MEDIA_URL = '/media/'

STATIC_ROOT = env("STATIC_MEDIA_PATH")+"static"
STATIC_URL = '/static/'

TEMPLATE_DIRS = (
    root("../templates/"),
    #root("../../env/lib/python2.7/site-packages/object_permissions/templates/object_permissions/"),
    #root("../vendor/rest_framework_swagger/templates"),
)









