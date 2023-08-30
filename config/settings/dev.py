import environ
from .base import *


env = environ.Env()
environ.Env.read_env(str(BASE_DIR / ".env"))

SECRET_KEY = env.str("secret_key")

ALLOWED_HOSTS = ["127.0.0.1"]

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": env.str("db_name"),
        "USER": env.str("db_user"),
        "PASSWORD": env.str("db_password"),
        "HOST": env.str("db_host"),
        "PORT": env.int("db_port"),
    }
}
