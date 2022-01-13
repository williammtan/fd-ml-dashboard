
set -e

# migrate
if [ -z $MIGRATE ]; then python3 manage.py migrate --noinput

mkdir -p data/models
