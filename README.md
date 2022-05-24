# notes
- codestyle - black

simple notes.  
users can write something and share with another users if they want.
or make note private, so no one can see it.

## technology stack
- webserver - nginx
- database - postgresql
- backend (finished)
    - python3.10
    - django
    - django rest framework
    - gunicorn
- frontend (in progress)
    - react

## run
set env variables:
- `NOTES_PGDATA_PATH` - path to a directory where postgres will store the data
- `NOTES_DB_NAME` - database name
- `POSTGRES_PASSWORD` - database password
- `NOTES_SECRET_KEY` - django secret key

if postgres data directory is empty or not exists: just run
```bash
docker-compose up --build
```

---
if data is already initialized docker will not create database, so you have to do it manualy
```bash
docker-compose up --build --no-start
docker-compose run -d --name postgres postgres
docker exec -it postgres /bin/bash
psql --user=postgres  # use any user which have rights to create database and another user
```
```sql
CREATE DATABASE yourDatabaseName;
CREATE USER sameUsernameAsDatabase;
GRANT ALL PRIVILEGES ON DATABASE yourDatabaseName TO sameUsernameAsDatabase;
```

## development
install dependencies
```bash
pip install poetry
poetry install
```

---
migrations to dev database (sqlite)
```bash
poetry run python manage.py makemigrations
poetry run python manage.py migrate --settings mysite.dev_settings
```

---
run core tests
```bash
poetry run python manage.py tests --settings mysite.dev_settings
```

---
runing dev server of core microservice
```bash
poetry run python manage.py runserver --settings mysite.dev_settings
```

---
access core api documentation with swagger ui (dev server should be ran)
```bash
docker run --net=host swaggerapi/swagger-ui
```
then explore this url `http://localhost:8000/schema`