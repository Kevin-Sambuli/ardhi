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

exec:
	docker-compose -f docker-compose.yml exec land_app python manage.py

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
container:
	docker up  # showing running containers
	docker up -a
inspect:
	docker inspect 977654323456 # returning container information


# container commands
docker run postgres
docker up 
docker images
docker config
docker pull image
docker logs container name or image
docker inspect container name # check container details
docker exec container name
docker ps #checking running container
docker ps -a # checking all containers
docker stop container id or name # stopping container
docker run i postgres # interactive mode
docker run it postgres # interactive shell and prompt

docker network ls # checking all networks in the docker