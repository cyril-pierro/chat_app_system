# Pull base image
FROM python:3.9-slim-bookworm

# Create work directory
WORKDIR /usr/src/app

# Install poetry env, project dependecny and model files
COPY poetry.lock pyproject.toml ./

# hadolint ignore=DL3013,DL3008,DL3014
RUN apt-get update -y;apt-get install libmariadb-dev-compat libmariadb-dev -y;pip install --no-cache-dir poetry==1.4.0 && poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi --no-root
# Copy files
COPY ./ ./

# Expose port and run application
EXPOSE 8082
ENTRYPOINT ["/bin/sh", "-c", "bash scripts/startup.sh"]
