#!/usr/bin/env bash
# exit on error
set -o errexit

# Install latest pip and build tools
pip install --upgrade pip setuptools wheel

# Install dependencies from requirements.txt
pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate