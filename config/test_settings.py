from .base_setttings import *

# SECURITY WARNING: don't run with debug turned on in production!
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'q^j8b&ejnd!09^ni9c08&$yb+mmq!cem((1^u)4y)5d3zu*gu8'
DEBUG = True
ALLOWED_HOSTS = ["*"]

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'testdb.sqlite3',
    }
}

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue'
        },
    },
    'formatters': {
        'verbose': {
            'format': '[{levelname}][{asctime}][{module}/{funcName}:{lineno}]  {message}',
            'style': '{',
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'formatter': 'verbose',
            'filename': os.path.join(BASE_DIR, 'django.log')
        },
    },
    'loggers': {
        'default': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
        }
    }
}
