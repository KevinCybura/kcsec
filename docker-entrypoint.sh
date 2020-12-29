#!/bin/sh
set -e

run_dev() {
  exec poetry run ./manage.py runserver 0.0.0.0:8000
}

run_client() {
  exec poetry run ./manage.py ws_client
}

run_migrate() {
    poetry run ./manage.py migrate
    poetry run ./manage.py crypto_seeds
}

run () {
  if [ "$1" = "dev" ]; then
    run_dev
  elif [ "$1" = "client" ]; then
    run_client
  elif [ "$1" = "migrate" ]; then
    run_migrate
  fi
}

run "$@"