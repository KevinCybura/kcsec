from kcsec.config.settings.common import *

SECRET_KEY = "test-not-so-secret-key"

DATABASES = {
    "default": {
        "ENGINE": "psqlextra.backend",
        "NAME": "kcsec",
        "USER": "kcsec",
        "PASSWORD": "",
        "HOST": os.environ.get("POSTGRES_HOST", "localhost"),
        "PORT": os.environ.get("POSTGRES_PORT", "5432"),
        "TEST": {"NAME": "test_kcsec"},
    }
}
