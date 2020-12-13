build:
	poetry install

update:
	poetry update

test:
	poetry run pytest

fmt:
	poetry run isort .
	poetry run black .

serve:
	poetry run ./manage.py runserver

crypto_sockets:
	poetry run ./manage.py ws_client

superuser:
	echo "from django.contrib.auth import get_user_model; \
	from kcsec.core.models import Portfolio; \
	User = get_user_model(); \
	user = User.objects.create_superuser(username='admin', password='admin', email='admin@admin.com'); \
	Portfolio.objects.create(user=user);" | poetry run python manage.py shell

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

db: dropdb createdb migrate seeds superuser
 # docker stuff
dc-build:
	docker-compose build

build-no-cache:
	docker-compose build --no-cache

dc-up:
	docker start kcsec-db
	docker-compose up web redis minio migrate-kcsec pushgateway
