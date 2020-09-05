import os

import django
from django.conf import settings
from dotenv import load_dotenv


def configure(
    databases=None, s3_storage_backend=False, skip_metrics=False, media_root="media",
):
    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "verbose": {"format": "%(levelname)s %(asctime)s %(pathname)s %(funcName)s \n%(message)s"},
            "simple": {"format": "%(levelname)s %(message)s"},
        },
        "handlers": {"simple_console": {"class": "logging.StreamHandler", "level": "INFO", "formatter": "simple",}},
        "loggers": {
            "django": {"handlers": ["simple_console"], "level": os.getenv("DJANGO_LOG_LEVEL", "INFO"),},
            "django.db.backends": {"handlers": ["simple_console"], "level": os.getenv("DJANGO_LOG_LEVEL", "INFO"),},
            "kcsec": {"handlers": ["simple_console"], "level": os.getenv("DJANGO_LOG_LEVEL", "INFO"),},
        },
    }
    if databases is None:
        databases = {
            "default": {
                "ENGINE": "psqlextra.backend",
                "NAME": os.getenv("POSTGRES_DB", "kcsec"),
                "USER": os.getenv("POSTGRES_USER", "kcsec"),
                "PASSWORD": os.getenv("POSTGRES_PASSWORD", ""),
                "HOST": os.getenv("POSTGRES_HOST", "localhost"),
                "PORT": "5432",
            }
        }
    INSTALLED_APPS = [
        "django.contrib.admin",
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.messages",
        "django.contrib.postgres",
        "psqlextra",
        "kcsec",
        "kcsec.core",
        "kcsec.crypto",
    ]
    TEMPLATES = [
        {
            "BACKEND": "django.template.backends.django.DjangoTemplates",
            "DIRS": [],
            "APP_DIRS": True,
            "OPTIONS": {
                "context_processors": [
                    "django.template.context_processors.debug",
                    "django.template.context_processors.request",
                    "django.contrib.auth.context_processors.auth",
                    "django.contrib.messages.context_processors.messages",
                ]
            },
        }
    ]
    if s3_storage_backend:
        file_backend_kwargs = dict(
            DEFAULT_FILE_STORAGE="storages.backends.s3boto3.S3Boto3Storage",
            AWS_ACCESS_KEY_ID=os.environ["AWS_SDW_ACCESS_KEY"],
            AWS_SECRET_ACCESS_KEY=os.environ["AWS_SDW_SECRET_ACCESS_KEY"],
            AWS_STORAGE_BUCKET_NAME=os.environ["AWS_SDW_STORAGE_BUCKET_NAME"],
        )
    else:
        file_backend_kwargs = dict(
            DEFAULT_FILE_STORAGE="django.core.files.storage.FileSystemStorage", MEDIA_ROOT=media_root,
        )
    MIDDLEWARE = [
        "django_prometheus.middleware.PrometheusBeforeMiddleware",
        "whitenoise.middleware.WhiteNoiseMiddleware",
        "django.middleware.security.SecurityMiddleware",
        "django.contrib.sessions.middleware.SessionMiddleware",
        "django.middleware.common.CommonMiddleware",
        "django.middleware.csrf.CsrfViewMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
        "django.contrib.messages.middleware.MessageMiddleware",
        "django.middleware.clickjacking.XFrameOptionsMiddleware",
        "django_prometheus.middleware.PrometheusAfterMiddleware",
    ]
    settings.configure(
        DEBUG=True,
        LOGGING=LOGGING,
        SECRET_KEY="super-secret-key",
        ROOT_URLCONF="kcsec.config.urls",
        INSTALLED_APPS=INSTALLED_APPS,
        DATABASES=databases,
        TIME_ZONE="UTC",
        USE_TZ=True,
        DEFAULT_NUM_SEEDS=10,
        SKIP_METRICS=skip_metrics,
        ADMIN_URL=os.getenv("ADMIN_URL", "http://localhost:8001"),
        AIRFLOW_URL=os.getenv("AIRFLOW_URL", "http://localhost:8080"),
        PUSHGATEWAY_HOST=os.getenv("PUSHGATEWAY_HOST", "http://pushgateway:9091"),
        PROFILING=False,
        TEMPLATES=TEMPLATES,
        MIDDLEWARE=MIDDLEWARE,
        TEST=False,
        READONLY_CONNECTION=False,
        **file_backend_kwargs,
    )


def init(databases=None, s3_storage_backend=False, media_root="media"):
    configure(
        databases=databases, s3_storage_backend=s3_storage_backend, media_root=media_root,
    )
    django.setup()


def configure_local_settings():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "kcsec.config.settings.local")
    load_dotenv()
    django.setup()
