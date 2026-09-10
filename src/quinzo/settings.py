from pathlib import Path
import configparser
import os

from .helpers.config import EnvOrParserConfig

BASE_DIR = Path(__file__).resolve().parent.parent

_config = configparser.RawConfigParser()
if 'CONFIG_FILE' in os.environ:
    config_files = [os.environ['CONFIG_FILE']]
else:
    config_files = ['/etc/quinzo.cfg', os.path.expanduser('~/.quinzo.cfg'), 'quinzo.cfg']

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
    "django.contrib.staticfiles",
    'compressor',
    'quinzo'
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

ROOT_URLCONF = "quinzo.urls"

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
DATABASES = {
    "default": {
        "ENGINE": config.get("database", "engine", fallback="django.db.backends.postgresql"),
        "NAME": config.get("database", "name"),
        "USER": config.get("database", "user"),
        "PASSWORD": config.get("database", "password"),
        "HOST": config.get("database", "host"),
        "PORT": config.get("database", "port", fallback="5432"),
        "CONN_MAX_AGE": config.getint("database", "conn_max_age", fallback=60),
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


# Internationalization
# https://docs.djangoproject.com/en/6.1/topics/i18n/

LANGUAGE_CODE = config.get("django", "language_code", fallback="en-us")
TIME_ZONE = config.get("django", "time_zone", fallback="UTC")
USE_I18N = config.getboolean("django", "use_i18n", fallback=True)
USE_TZ = config.getboolean("django", "use_tz", fallback=True)


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/6.1/howto/static-files/

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
STATIC_URL = "static/"
STATIC_ROOT = os.path.join(os.path.dirname(__file__), 'staticfiles')
COMPRESS_ROOT = BASE_DIR / "quinzo" / "static"

COMPRESS_ENABLED = True

STATICFILES_FINDERS = ('compressor.finders.CompressorFinder',)

# Email
# https://docs.djangoproject.com/en/6.1/topics/email/#topic-email-configuration

MAILERS = {
    "default": {
        "BACKEND": "django.core.mail.backends.console.EmailBackend",
    },
}

SESSION_COOKIE_HTTPONLY = os.environ.get("SESSION_COOKIE_HTTPONLY", "True") == "True"
SESSION_COOKIE_SECURE = os.environ.get("SESSION_COOKIE_SECURE", "True") == "True"
CSRF_COOKIE_SECURE = os.environ.get("CSRF_COOKIE_SECURE", "True") == "True"