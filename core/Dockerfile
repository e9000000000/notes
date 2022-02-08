FROM python:latest

WORKDIR /service

COPY pyproject.toml ./
RUN pip install --no-cache-dir --upgrade pip \
&& pip install --no-cache-dir poetry \
&& poetry config virtualenvs.create false \
&& poetry install --no-dev \
&& pip uninstall --yes poetry

CMD ./manage.py makemigrations && \
./manage.py migrate && \
gunicorn --reload -b 0.0.0.0:80 -w 4 mysite.wsgi
