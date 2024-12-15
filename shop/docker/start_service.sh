#!/bin/bash

export PYTHONPATH=/app

alembic upgrade head
uvicorn app:app --host 0.0.0.0 --port 8080
