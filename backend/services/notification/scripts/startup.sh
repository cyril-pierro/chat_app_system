#!/bin/bash

celery -A main worker --loglevel=INFO & celery -A main flower --loglevel=INFO --address=0.0.0.0 --port=8083
