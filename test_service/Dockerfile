FROM python:3.11 as python-base
RUN mkdir "test_service_app"
WORKDIR /test_service_app
COPY /pyproject.toml /test_service_app
RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install
COPY . .
CMD ["gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "app:app", "--bind", "0.0.0.0:8002"]