#!/bin/bash

celery -A main worker -b $CELERY_BROKER_URL --loglevel=INFO & sleep 4s; celery -A main -b $CELERY_BROKER_URL flower --loglevel=INFO --address=0.0.0.0 --port=8082
