FROM python:3.13

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code

COPY requirements.txt ./
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

# Für statische Dateien
RUN mkdir -p /code/static/dist

# Symlink für daphne ins PATH (Workaround für PATH-Probleme)
RUN ln -s /code/.venv/bin/daphne /usr/local/bin/daphne || true
