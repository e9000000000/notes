FROM python:3.10

WORKDIR /service

COPY pyproject.toml ./
RUN pip install --no-cache-dir --upgrade pip \
&& pip install --no-cache-dir poetry \
&& poetry config virtualenvs.create false \
&& poetry install --no-dev \
&& poetry config virtualenvs.create true \
&& pip uninstall --yes poetry
