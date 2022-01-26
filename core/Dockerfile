FROM python:3.10

WORKDIR /service

COPY requirements.txt .
RUN pip install -r requirements.txt

CMD ./manage.py makemigrations;\
./manage.py migrate;\
./manage.py runserver 0.0.0.0:8000
