#!/bin/sh

export PGUSER="postgres"

psql -c "CREATE DATABASE flask_crud"

psql flask_crud -c "CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";"