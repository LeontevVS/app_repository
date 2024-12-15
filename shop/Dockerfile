FROM python:3.12 AS python-base
RUN mkdir "shop"
WORKDIR /shop
COPY /pyproject.toml /shop
RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install
COPY . .
RUN ["chmod", "775", "/shop/docker/start_service.sh"]
WORKDIR /shop/app
CMD ["/shop/docker/start_service.sh"]