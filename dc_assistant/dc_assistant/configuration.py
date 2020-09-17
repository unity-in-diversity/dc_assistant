#########################
#                       #
#   Required settings   #
#                       #
#########################

BASE_PATH = ''
ALLOWED_HOSTS = ['*']

DATABASE = {
    'ENGINE': 'django.db.backends.postgresql',  # Database engine
    'NAME': 'dcassistant',                         # Database name
    'USER': 'dcassistant',                         # PostgreSQL username
    'PASSWORD': 'postgres',                     # PostgreSQL password
    'HOST': '192.168.99.220',                   # Database server
    'PORT': '6432',                                 # Database port (leave blank for default)
    'CONN_MAX_AGE': 300,                        # Max database connection age
}
SECRET_KEY = '_r^9!7plgkf2u-ri^fga&c^1gohf@8x0=#rzgdq3f(a9gd*h!='

#########################
#                       #
#   Optional settings   #
#                       #
#########################

PAGINATE_COUNT = 5
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True