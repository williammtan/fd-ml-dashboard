#!/usr/bin/env


echo "entrypoint"
# migrate
if [ -z $MIGRATE ]; then python3 manage.py migrate --database ml --noinput && python3 collectstatic --database ml --noinput ; fi

mkdir -p data/models

exec "$@"
