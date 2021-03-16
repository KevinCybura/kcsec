#!/bin/sh
set -e

run_server() {
  DJANGO_SETTINGS_MODULE=kcsec.config.settings.docker poetry run ./manage.py collectstatic --no-input
  poetry run gunicorn -b 0.0.0.0 -p 8000 --workers 3 kcsec.config.wsgi:application
}

run_channels() {
  poetry run daphne -b 0.0.0.0 -p 8001 kcsec.config.asgi:application
}

run_client() {
  poetry run ./manage.py ws_client
}

run_migrate() {
    poetry run ./manage.py migrate
    poetry run ./manage.py crypto_seeds
}

run () {
  if [ "$1" = "server" ]; then
    run_server
  elif [ "$1" = "channels" ]; then
    run_channels
  elif [ "$1" = "consumer" ]; then
    run_client
  elif [ "$1" = "migrate" ]; then
    run_migrate
  fi
}

run "$@"