#!/bin/bash

echo "Waiting for Postgres..."
until pg_isready -h $POSTGRES_HOST -p $POSTGRES_PORT -U $POSTGRES_USER; do
  sleep 1
done
echo "Postgres is up - executing command"

exec "$@"
