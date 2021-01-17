from kcsec.config.settings.common import *

DEBUG = False

SECRET_KEY = "docker-not-so-secret-key"
ALLOWED_HOSTS = ["*"]

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "psqlextra.backend",
        "NAME": os.getenv("POSTGRES_NAME", "kcsec"),
        "USER": os.getenv("POSTGRES_USER", "kcsec"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD", ""),
        "HOST": os.getenv("POSTGRES_HOST", "kcsec-db"),
        "PORT": os.environ.get("POSTGRES_PORT", "5432"),
    }
}
# DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_MPS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = os.environ.get("AWS_MPS_STORAGE_BUCKET_NAME")

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")

EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = "Kcsec team <noreplay@kcsec.com>"
