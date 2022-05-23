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
    - rest_captcha (captcha on registration)
- frontend (in progress)
    - react

## run
set env variables:
- `POSTGRES_USER` - database user name
- `POSTGRES_PASSWORD` - database password
- `NOTES_SECRET_KEY` - django secret key
- `NOTES_DB_NAME` - database name

`docker-compose up --build`

## development
runing dev server of core microservice
```bash
pip install poetry
poetry update
poetry run python manage.py makemigrations
poetry run python manage.py migrate --settings mysite.dev_settings
poetry run python manage.py runserver --settings mysite.dev_settings
```
-------
access core api documentation with swagger ui (dev server should be ran)
```bash
docker run --net=host swaggerapi/swagger-ui
```
then explore this url `http://localhost:8000/schema`