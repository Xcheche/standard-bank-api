#=========== Makefile for Docker Compose Management ===========#
# Build and Start Containers

#=======================WEB SERVICE VARIABLE=======
WEB_SERVICE=api

#==========Manual Commands for Docker Compose===========
# Usage: make [target]
# Targets:
#   build           Build and start containers
#   up              Start containers in detached mode
#   upp             Start containers without detached mode
#   down            Stop and remove containers
#   down-v          Stop and remove containers and volumes
#   banker-config    View Docker Compose configuration
#   makemigrations  Create Django migrations
#   migrate         Apply Django migrations
#   collectstatic   Collect static files for Django
#   superuser       Create a Django superuser
#   flush           Flush the Django database
#   network-inspect Inspect Docker network
#   banker-db       Access the Postgres database
build:
	echo "🔨Building containers..."
	docker compose -f local.yml up --build -d --remove-orphans
# Bring Up Containers
up:
	echo "🚀Starting containers in detached mode..."
	docker compose -f local.yml up -d
# Bring Down Containers

# Bring Up Containers without detached mode
upp:
	echo "🚀Starting containers without detached mode..."
	docker compose -f local.yml up
down:
	echo "🛑Stopping and removing containers..."
	docker compose -f local.yml down
# Bring Down Containers and Volumes
down-v:
	echo "🛑Stopping and removing containers and volumes..."
	docker compose -f local.yml down -v
# View Docker Compose Configuration
banker-config:
	echo "🔍Viewing Docker Compose configuration..."
	docker compose -f local.yml config
# Create Django Migrations
makemigrations:
	echo "📦Creating Django migrations..."
	docker compose -f local.yml run --rm ${WEB_SERVICE} python manage.py makemigrations

# Check what to migrate
check-migrate:
	echo "🔍Checking for pending migrations..."
	docker compose -f local.yml run --rm ${WEB_SERVICE} python manage.py showmigrations --plan


# Check  errors in Django Migrations
check-migrations:
	echo "🔍Checking for pending migrations..."
	docker compose -f local.yml run --rm ${WEB_SERVICE} python manage.py makemigrations --check --dry-run

# Apply Django Migrations
migrate:
	echo "🚀Applying Django migrations..."
	docker compose -f local.yml run --rm ${WEB_SERVICE} python manage.py migrate
#
collectstatic:
	echo "📁Collecting static files for Django..."
	docker compose -f local.yml run --rm ${WEB_SERVICE} python manage.py collectstatic --no-input --clear
# Create Django Superuser
superuser:
	echo "👤Creating Django superuser..."
	docker compose -f local.yml run --rm ${WEB_SERVICE} python manage.py createsuperuser

# logs
logs:
	echo "📜Viewing logs for all services..."
	docker compose -f local.yml logs -f
# logs for a specific service
logs-service:
	echo "📜Viewing logs for ${WEB_SERVICE} service..."		
	docker compose -f local.yml logs -f ${WEB_SERVICE}
# Django DB Flush
flush:
	echo "🧹Flushing the Django database..."
	docker compose -f local.yml run --rm ${WEB_SERVICE} python manage.py flush

# Inspect Docker Network
network-inspect:
	echo "🔍Inspecting Docker network..."
	docker network inspect banker_local_nw

# Access Postgres Database
banker-db:
	echo "🔍Accessing the Postgres database..."
	docker compose -f local.yml exec postgres psql --username=cheche --dbname=banker