#! /usr/bin/env sh
set -e

if [ -f /app/app/main.py ]; then
    DEFAULT_MODULE_NAME=app.main
elif [ -f /app/main.py ]; then
    DEFAULT_MODULE_NAME=main
fi

MODULE_NAME=${MODULE_NAME:-$DEFAULT_MODULE_NAME}
VARIABLE_NAME=${VARIABLE_NAME:-app}
export APP_MODULE="${MODULE_NAME}:${VARIABLE_NAME}"

HOST=${HOST:-0.0.0.0}
PORT=${PORT:-80}
LOG_LEVEL=${LOG_LEVEL:-info}

if [ -f /app/gunicorn_conf.py ]; then
    DEFAULT_GUNICORN_CONF=/app/gunicorn_conf.py
elif [ -f /app/app/gunicorn_conf.py ]; then
    DEFAULT_GUNICORN_CONF=/app/app/gunicorn_conf.py
else
    DEFAULT_GUNICORN_CONF=/gunicorn_conf.py
fi

export GUNICORN_CONF=${GUNICORN_CONF:-$DEFAULT_GUNICORN_CONF}
export WORKER_CLASS=${WORKER_CLASS:-"uvicorn.workers.UvicornWorker"}

PRE_START_PATH=${PRE_START_PATH:-/app/prestart.sh}
echo "Checking for script in $PRE_START_PATH"

if [ -f "$PRE_START_PATH" ]; then
    echo "Running script $PRE_START_PATH"
    "$PRE_START_PATH"
else
    echo "There is no script $PRE_START_PATH"
fi

if [ "$DEV_MODE" = 'true' ]; then
    # Start Uvicorn with live reload
    exec uvicorn --reload --host $HOST --port $PORT --log-level $LOG_LEVEL "$APP_MODULE"
else
    # Assume production mode if DEV_MODE isn't 'true'
    # Start Gunicorn
    echo "Starting in normal config"
    exec gunicorn -k "$WORKER_CLASS" -C "$GUNICORN_CONF" "$APP_MODULE"
fi
