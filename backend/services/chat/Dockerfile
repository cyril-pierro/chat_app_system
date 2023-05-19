# Pull base image
FROM python:3.9

# Create work directory
WORKDIR /usr/src/app

# Install poetry env, project dependecny and model files
COPY poetry.lock pyproject.toml ./

# hadolint ignore=DL3013
RUN pip install --no-cache-dir poetry==1.4.0 && poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi --no-root
# Copy files
COPY ./ ./

# Expose port and run application
EXPOSE 8083
ENTRYPOINT ["/bin/sh", "-c", "python manage.py migrate && python manage.py search_index --create && gunicorn --env DJANGO_SETTINGS_MODULE=core.settings core.wsgi -b :8083"]
