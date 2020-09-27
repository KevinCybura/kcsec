test:
	poetry run pytest

fmt:
	poetry run isort .
	poetry run black .

web:
	poetry run ./manage.py runserver

crypto_sockets:
	poetry run ./manage.py ws_client

superuser:
	poetry run ./manage.py createsuperuser

createdb:
	createuser -s kcsec
	createdb kcsec

dropdb:
	dropdb --if-exists test_kcsec
	dropdb --if-exists kcsec
	dropuser --if-exists kcsec

migrate:
	poetry run ./manage.py migrate

migrations:
	poetry run ./manage.py makemigrations

seeds:
	poetry run ./manage.py crypto_seeds

db: dropdb createdb migrate seeds

dc-build:
	docker-compose

 # docker stuff
build:
	docker-compose build

build-no-cache:
	docker-compose build --no-cache

dc-up:
	docker start kcsec-db
	docker-compose up web redis minio migrate-kcsec pushgateway
