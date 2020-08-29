from .common import *

SECRET_KEY = "local-not-so-secret-key"

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "psqlextra.backend",
        "NAME": os.getenv("DB_NAME", "kcsec"),
        "USER": os.getenv("DB_USER", "kcsec"),
        "PASSWORD": os.getenv("DB_PASSWORD", ""),
        "HOST": "localhost",
        "PORT": "5432",
    }
}
