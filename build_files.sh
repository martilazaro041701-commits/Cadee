#!/usr/bin/env bash
set -euo pipefail

python -m pip install --upgrade pip --break-system-packages
python -m pip install -r requirements.txt --break-system-packages

python Cadee/manage.py migrate --noinput
python Cadee/manage.py collectstatic --noinput
