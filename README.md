# Django StateEdu API with Docker, PostgreSQL, Redis, and Celery

## About
This project is a Django-based API for managing educational content and services, containerized with Docker for easy deployment. It integrates PostgreSQL as the database, Redis for caching and Celery task management, and runs in a production-ready setup with Gunicorn.

## Features
- **Django Framework** for robust backend development.
- **PostgreSQL** for reliable data storage.
- **Redis** for caching and Celery message brokering.
- **Celery** for background task processing.
- **Docker Compose** for container orchestration.
- **Gunicorn** as a production-grade WSGI server.

---

## Prerequisites

Ensure you have the following installed:
- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

---

## Setup Instructions

### Step 1: Clone the Repository
```bash
git clone https://github.com/RahimovIlhom/stat-edu-parsing.git
cd stat-edu-parsing
```

### Step 2: Configure Environment Variables
Create a `.env` file in the root directory with the following content:
```bash
# Server Parameters
SECRET_KEY=<your-secret-key>

# You can generate a Django SECRET_KEY using the following Python command:
# python -c "import secrets; print(secrets.token_urlsafe(50))"
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost,0.0.0.0
CSRF_TRUSTED_ORIGINS=<your-csrf-trusted-origins>

# Docker Container
DATABASE_URL=postgres://<your-postgres-user>:<your-postgres-password>@postgres_statedu:5432/statedu_db
DJANGO_SUPERUSER_USERNAME=ilhomjon
DJANGO_SUPERUSER_EMAIL=ilhomjonpersonal@gmail.com
DJANGO_SUPERUSER_PASSWORD=Ilhomjon3103&

# Redis
REDIS_HOST=redis_statedu
REDIS_URL=redis://redis_statedu:6379/0

# Celery
CELERY_BROKER_URL=redis://redis_statedu:6379/1
CELERY_RESULT_BACKEND=redis://redis_statedu:6379/1

# Database Parameters
POSTGRES_DB=statedu_db
POSTGRES_USER=<your-postgres-user>
POSTGRES_PASSWORD=<your-postgres-password>
POSTGRES_HOST=postgres_statedu
POSTGRES_PORT=5432
```
Replace `<your-secret-key>`, `<your-csrf-trusted-origins>`, `<your-postgres-user>`, and `<your-postgres-password>` with appropriate values.

### Step 3: Build and Run Containers
Run the following command to build and start the application:
```bash
docker-compose up --build
```

### Step 4: Access the Application
- **Web Application**: [http://localhost:8580](http://localhost:8580)
- **Admin Panel**: [http://localhost:8580/admin](http://localhost:8580/admin)

---

## Services Overview

### `web`
Runs the Django application with the following setup:
- Collects static files.
- Applies database migrations.
- Creates a superuser (if not already created).
- Serves the application using Gunicorn.

### `database`
A PostgreSQL 15 container configured with the environment variables defined in `.env`.

### `redis`
Redis 7 container for caching and Celery message brokering.

### `celery`
Executes background tasks using Celery workers.

### `celery_beat`
Handles periodic tasks using Celery Beat.

---

## Troubleshooting

### 1. Static Files Warning
If you see:
```plaintext
(staticfiles.W004) The directory '/app/static' in the STATICFILES_DIRS setting does not exist.
```
Ensure the `STATICFILES_DIRS` in your `settings.py` is correctly set and the folder exists:
```python
STATICFILES_DIRS = [BASE_DIR / "static"]
```

### 2. Superuser Creation Error
If the superuser creation fails with:
```plaintext
CommandError: That username is already taken.
```
Manually create a superuser:
```bash
docker exec -it django_statedu python manage.py createsuperuser
```

### 3. Database Connection Issues
Ensure the PostgreSQL container is running and correctly configured in the `.env` file.

---

## Directory Structure
```plaintext
.
├── core/                 # Main Django application
├── Dockerfile            # Dockerfile for building the web application
├── docker-compose.yml    # Docker Compose configuration
├── .env                  # Environment variables file
├── static/               # Static files (optional)
├── templates/            # HTML templates
└── README.md             # This file
```

---

## Notes
- Celery Beat is pre-configured for periodic tasks. Ensure the `celery_beat` container is running for scheduled tasks to work.
- Gunicorn is used to serve Django in a production environment.

---

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

