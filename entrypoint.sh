#!/bin/bash

# Initialisation de la base de données Flask
python runserver.py flask flask db init

# Initialisation de la base de données
python runserver.py flask init_db

exec "$@"
