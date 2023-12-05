#!/bin/bash

echo "Starting entrypoint.sh"

# Initialisation de la base de données Flask
python runserver.py flask flask db init

# Initialisation de la base de données
python runserver.py flask init_db

echo "Entrypoint.sh executed successfully"
exec "$@"
