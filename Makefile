ifneq (,$(wildcard .env))
   include .env
   export
   ENV_FILE_PARAM = --env-file .env
endif

build:
	docker-compose up --build --remove-orphans
	docker-compose -f docker-compose.yml down -v
	docker-compose -f docker-compose.yml up -d --build --remove-orphans
	docker-compose -f docker-compose.yml exec land_app python manage.py migrate --noinput

up:
	docker-compose up

logs:
	docker-compose logs

down:
	docker-compose down

migrate:
	docker-compose exec land_app python manage.py migrate --noinput

makemigrations:
	docker-compose exec land_app python manage.py makemigrations

superuser:
	docker-compose exec land_app python manage.py createsuperuser

down-v:
	docker-compose down -v

volume:
	docker volume inspect land_app_postgres_data

volumecheck:
	docker volume ls

shell:
	docker-compose exec land_app python manage.py shell

database_check:
	docker-compose exec postgres-db psql --username=kevoh --dbname=Ardhi
	docker-compose exec postgres-db psql --username=kevoh --dbname=LIS
	LIS=# \l
	LID=# \c
	LIS=# \dt
	LIS=# \P

create_app:
	docker-compose run land_app sh -c "django-admin startapp core"

start_django_proj:
	docker-compose run land_app sh -c "django-admin startproject ardhi"

#docker-compose -f docker-compose.prod.yml down -v
#docker-compose -f docker-compose.prod.yml up -d --build
#docker-compose -f docker-compose.prod.yml exec land_app python manage.py migrate --noinput