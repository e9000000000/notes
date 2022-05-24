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
- `POSTGRES_USER` - database user name, set to `postgres`
- `POSTGRES_PASSWORD` - database user password
- `NOTES_SECRET_KEY` - django secret key
- `NOTES_DB_NAME` - database name

run
```bash
docker-compose up --build
```

if database is not created: run this
```bash
docker-compose up --build --no-start
docker-compose run -d --name postgres postgres
docker exec -it postgres /bin/bash
psql --user=postgres -c "CREATE DATABASE $POSTGRES_DB"
docker-compose restart
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