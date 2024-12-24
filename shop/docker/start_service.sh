#!/bin/bash

export PYTHONPATH=/app

alembic upgrade head
python3 app.py
#uvicorn app:app --host 0.0.0.0 --port 8080
