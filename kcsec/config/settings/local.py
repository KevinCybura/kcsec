from kcsec.config.settings.common import *

SECRET_KEY = "local-not-so-secret-key"

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

INSTALLED_APPS.append("debug_toolbar")
MIDDLEWARE.append("debug_toolbar.middleware.DebugToolbarMiddleware")
INTERNAL_IPS = ["127.0.0.1"]

DATABASES = {
    "default": {
        "ENGINE": "psqlextra.backend",
        "NAME": os.getenv("POSTGRES_NAME", "kcsec"),
        "USER": os.getenv("POSTGRES_USER", "kcsec"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD", ""),
        "HOST": os.getenv("POSTGRES_HOST", "localhost"),
        "PORT": os.environ.get("POSTGRES_PORT", "5432"),
    }
}
