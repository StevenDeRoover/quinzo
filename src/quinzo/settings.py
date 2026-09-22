from pathlib import Path
import configparser
import os
import sys

from .base.config import EnvOrParserConfig

BASE_DIR = Path(__file__).resolve().parent.parent

_config = configparser.RawConfigParser()
if 'CONFIG_FILE' in os.environ:
    config_files = [os.environ['CONFIG_FILE']]
else:
    config_files = ['/etc/quinzo.cfg',
                    os.path.expanduser('~/.quinzo.cfg'), 'quinzo.cfg']

_config.read(config_files)
config = EnvOrParserConfig(_config)


CONFIG_FILE = config


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/6.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config.get("django", "secret_key")
DEBUG = config.getboolean("django", "debug")
DEVELOPMENT = os.getenv("DEVELOPMENT", "false").lower() == "true"
SITE_ID = config.getint("django", "site_id", fallback=1)
ALLOWED_HOSTS = ["*"]

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {"format": "[{levelname}] {name}: {message}", "style": "{"},
    },
    "handlers": {
        "console": {"class": "logging.StreamHandler", "formatter": "verbose"},
    },
    "loggers": {
        "authentication.middleware": {"handlers": ["console"], "level": "DEBUG"},
    },
}


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    'quinzo.base',
    "django.contrib.staticfiles",
    'quinzo.control',
    'quinzo.main',
    'quinzo.multidomain'
]

if DEVELOPMENT:
    INSTALLED_APPS.append("django_npm_dev")

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = 'quinzo.multidomain.configs.main'

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        'DIRS': [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "quinzo.wsgi.application"


# Database
# https://docs.djangoproject.com/en/6.1/ref/settings/#databases

# =====================================================
# Database
# =====================================================
db_backend = config.get('database', 'backend',
                        fallback='sqlite3').removeprefix('django.db.backends.')
if db_backend.endswith('psycopg2'):
    db_backend = 'postgresql'
elif 'mysql' in db_backend:
    print("Quinzo does not support running on MySQL/MariaDB")
    sys.exit(1)

DATABASES = {
    "default": {
        "ENGINE": 'django.db.backends.' + db_backend,
        "NAME": config.get("database", "name"),
        "USER": config.get("database", "user"),
        "PASSWORD": config.get("database", "password"),
        "HOST": config.get("database", "host"),
        "PORT": config.get("database", "port", fallback="5432"),
        'CONN_MAX_AGE': 0 if db_backend == 'sqlite3' else 120,
        'CONN_HEALTH_CHECKS': db_backend != 'sqlite3'
    }
}

# Password validation
# https://docs.djangoproject.com/en/6.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

if DEBUG:
    try:
        import debug_toolbar  # noqa: F401
        import debug_toolbar.settings
    except ImportError:
        DEBUG_TOOLBAR_INSTALLED = False
    else:
        DEBUG_TOOLBAR_INSTALLED = True
        INSTALLED_APPS.append("debug_toolbar")
        MIDDLEWARE.insert(0, "debug_toolbar.middleware.DebugToolbarMiddleware")
        DEBUG_TOOLBAR_CONFIG = {
            'JQUERY_URL': '',
            'DISABLE_PANELS': debug_toolbar.settings.PANELS_DEFAULTS,
        }
else:
    DEBUG_TOOLBAR_INSTALLED = False

INTERNAL_IPS = ('127.0.0.1', '::1')

# Internationalization
# https://docs.djangoproject.com/en/6.1/topics/i18n/

LANGUAGE_CODE = config.get("django", "language_code", fallback="en-us")
TIME_ZONE = config.get("django", "time_zone", fallback="UTC")
USE_I18N = config.getboolean("django", "use_i18n", fallback=True)
USE_TZ = config.getboolean("django", "use_tz", fallback=True)


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/6.1/howto/static-files/

STATIC_URL = "static/"
STATICFILES_DIRS = [
    BASE_DIR / "quinzo" / "static",
    BASE_DIR / "quinzo" / "static.dist",
]

STATIC_ROOT = BASE_DIR / "staticfiles"

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}

# Email
# https://docs.djangoproject.com/en/6.1/topics/email/#topic-email-configuration

MAILERS = {
    "default": {
        "BACKEND": "django.core.mail.backends.console.EmailBackend",
    },
}

SESSION_COOKIE_HTTPONLY = os.environ.get(
    "SESSION_COOKIE_HTTPONLY", "True") == "True"
SESSION_COOKIE_SECURE = os.environ.get(
    "SESSION_COOKIE_SECURE", "True") == "True"
CSRF_COOKIE_SECURE = os.environ.get("CSRF_COOKIE_SECURE", "True") == "True"
