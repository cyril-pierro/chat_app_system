# Pull base image
FROM python:3.9-slim-bookworm
#
# Create work directory
WORKDIR /usr/src/app

#Install poetry env, project dependecny and model files
COPY poetry.lock pyproject.toml ./

RUN pip install --no-cache-dir poetry==1.4.0 && poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi --no-root

#Copy files
COPY ./ ./

#Expose port and run application
EXPOSE 8084
ENTRYPOINT ["/bin/sh", "-c", "uvicorn main:app --host 0.0.0.0 --port 8084"]
