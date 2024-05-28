#! /bin/sh

alembic upgrade HEAD
exec "$@"