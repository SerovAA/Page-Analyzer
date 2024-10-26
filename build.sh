#!/usr/bin/env bash
set -o allexport
source .env
set +o allexport

make install && psql -a -d $DATABASE_URL -f database.sql