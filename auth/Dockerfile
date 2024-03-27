FROM python:3.11 as python-base
RUN mkdir "auth_app"
WORKDIR /auth_app
COPY /pyproject.toml /auth_app
RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install
COPY . .
RUN ["chmod", "775", "/auth_app/docker/start_service.sh"]
#CMD ["gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "app:app", "--bind", "0.0.0.0:8080"]