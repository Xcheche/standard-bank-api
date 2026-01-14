#=========== Makefile for Docker Compose Management ===========#
# Build and Start Containers
build:
	docker compose -f local.yml up --build -d --remove-orphans
# Bring Up Containers
up:
	docker compose -f local.yml up -d
# Bring Down Containers

# Bring Up Containers without detached mode
upp:
	docker compose -f local.yml up 
down:
	docker compose -f local.yml down
# Bring Down Containers and Volumes
down-v:
	docker compose -f local.yml down -v
# View Docker Compose Configuration
banker-config:
	docker compose -f local.yml config
# Create Django Migrations
makemigrations:
	docker compose -f local.yml run --rm api python manage.py makemigrations
# Apply Django Migrations
migrate:
	docker compose -f local.yml run --rm api python manage.py migrate
#
collectstatic:
	docker compose -f local.yml run --rm api python manage.py collectstatic --no-input --clear
# Create Django Superuser
superuser:
	docker compose -f local.yml run --rm api python manage.py createsuperuser
# Django DB Flush
flush:
	docker compose -f local.yml run --rm api python manage.py flush

# Inspect Docker Network
network-inspect:
	docker network inspect banker_local_nw

# Access Postgres Database
banker-db:
	docker compose -f local.yml exec postgres psql --username=cheche --dbname=banker