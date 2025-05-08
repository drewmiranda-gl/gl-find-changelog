#!/bin/bash

python3 -m venv venv
source venv/bin/activate

# cp requirements.txt /usr/share/prometheus_rewrite/

python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt --force-reinstall

deactivate
