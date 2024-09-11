#!/bin/sh
set -e

set -a
[ -f "/app/.env" ] && . /app/.env
set +a

if [ ! -d "/app/migrations" ]; then
  echo "Migrations directory not found. Running migrations..."
  flask db init
  flask db migrate -m "Init migration"
  flask db upgrade
  psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" -f /app/init.sql
else
  echo "Migrations directory found. Skipping migration."
fi

exec flask run --host=0.0.0.0 --port=8000