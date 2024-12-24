#!/bin/bash

if [ -z "$1" ]; then
  echo "Ошибка: Необходимо передать название миграции"
  echo "Использование: $0 <сообщение>"
  exit 1
fi

ENV_FILE="./scripts/.env"

if [ ! -f "$ENV_FILE" ]; then
  echo "Ошибка: Файл с переменными окружения $ENV_FILE не найден."
  exit 1
fi

set -a
source "$ENV_FILE"
set +a

cd ./shop/app && alembic revision --autogenerate -m "$1"

exit 0