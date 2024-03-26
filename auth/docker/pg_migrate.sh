#!/bin/bash

alembic upgrade head
#gunicorn -w 4 -k uvicorn.workers.UvicornWorker app:app --bind 0.0.0.0:8080
uvicorn app:app --host 0.0.0.0 --port 8080