#!/bin/bash

set -euxo pipefail

BUCKET="${BUCKET:-drs-crypt4gh}"

# Read in environment variables from .env file
export $(grep -v '^#' .env | xargs)

# Create local alias for Minio
mc alias set local http://127.0.0.1:9000 $MINIO_ROOT_USER $MINIO_ROOT_PASSWORD

# Create bucket for anonymous download
mc mb $BUCKET
mc anonymous set download $BUCKET

# Add local user with Minio upload privileges. Note: if the user already has
# the upload policy attached, the second command will print an error. This can
# be ignored.
mc admin user add local $ACCESS_KEY $SECRET_KEY
mc admin policy attach local readwrite --user $ACCESS_KEY || true
