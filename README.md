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
set vars:
- `POSTGRES_USER` - database user name
- `POSTGRES_PASSWORD` - database password
- `NOTES_SECRET_KEY` - django secret key
- `NOTES_DB_NAME` - database name

`docker-compose up --build`
