#!/bin/bash

source venv/bin/activate

export BIND_ADDR=0.0.0.0
export BIND_PORT=89

LOG_FILE=web.log \
    CONSOLE_LEVEL=INFO \
    LOG_LEVEL=INFO \
    CONFIG_FILE=config.yml \
    gunicorn -w 1 -b ${BIND_ADDR}:${BIND_PORT} -k gevent 'wsgi:app'

deactivate