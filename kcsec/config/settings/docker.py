from kcsec.config.settings.common import *

SECRET_KEY = "docker-not-so-secret-key"

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "psqlextra.backend",
        "NAME": os.getenv("POSTGRES_NAME", "kcsec"),
        "USER": os.getenv("POSTGRES_USER", "kcsec"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD", ""),
        "HOST": os.getenv("POSTGRES_HOST", "kcsec"),
        "PORT": os.environ.get("POSTGRES_PORT", "5432"),
    }
}
DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"

AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_MPS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = os.environ.get("AWS_MPS_STORAGE_BUCKET_NAME")
