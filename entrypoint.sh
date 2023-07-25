#!/bin/bash

set -e

# seed database TODO: fix me
python ./initialize_mongodb.py

# run docker cmd
exec "$@"
